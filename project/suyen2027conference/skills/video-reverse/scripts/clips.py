#!/usr/bin/env python3
"""粗剪和出片检查共用的小工具：找到每一段的出片、读剪辑表、听写。

只用 Python 标准库 + ffmpeg。被 assemble.py 和 check_clips.py 引用，不用单独跑。
"""
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_studio_canvas as b  # noqa: E402

TRIM = 0.5  # 「头」「尾」各剪掉的秒数：AI 片段开头结尾最不稳


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def need_ffmpeg():
    for tool in ("ffmpeg", "ffprobe"):
        if not shutil.which(tool):
            sys.exit(f"找不到 {tool}。请先安装 ffmpeg：\n  Mac:     brew install ffmpeg\n  Windows: winget install Gyan.FFmpeg")


def duration(path):
    r = run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path])
    try:
        return float(r.stdout.strip())
    except ValueError:
        sys.exit(f"读不到影片长度：{path}")


def has_audio(path):
    r = run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=index", "-of", "csv=p=0", path])
    return bool(r.stdout.strip())


# ---------- 找每一段的出片 ----------

def clips_from_folder(folder):
    """文件夹里的 第1段.mp4 / seg1.mp4 / 1.mp4 …… → {段号: 路径}"""
    found = {}
    for f in sorted(os.listdir(folder)):
        if not f.lower().endswith((".mp4", ".mov", ".m4v", ".webm")):
            continue
        m = re.search(r"第\s*(\d+)\s*段", f) or re.search(r"seg(?:ment)?[\s_-]*(\d+)", f, re.I) or re.match(r"(\d+)\D", f)
        if m:
            found.setdefault(int(m.group(1)), os.path.join(folder, f))
    return found


def clips_from_canvas(plan, dest):
    """从 studio 画布拿每段「选中的那一个」出片，下载到 dest。只读，不会按 Run。"""
    cache = os.path.join(plan["base"], ".studio_canvas.json")
    if not os.path.isfile(cache):
        sys.exit("没有 .studio_canvas.json（还没用 build_studio_canvas.py 搭过画布）。\n"
                 "请把每段出片下载到一个文件夹，档名带段号（例：第1段.mp4），再加 --clips <文件夹>。")
    k = b.key(plan["base"])
    wid = json.load(open(cache, encoding="utf-8"))["workflow_id"]
    w = b.call(k, "get_workflow", workflow_id=wid)
    if "error" in w:
        sys.exit(f"读画布失败：{w}")
    w = w.get("workflow", w)
    by_id = {n["id"]: n["data"].get("config", {}) for n in w.get("nodes", [])}
    os.makedirs(dest, exist_ok=True)
    found = {}
    for s in plan["segments"]:
        urls = []
        for nid in (f"seg{s['n']}_edit", f"seg{s['n']}_vid"):  # 加过字卡的用加了字卡的那一版
            c = by_id.get(nid) or {}
            urls = c.get("resultUrls") or ([c["resultUrl"]] if c.get("resultUrl") else [])
            if urls:
                break
        if not urls:
            print(f"  第 {s['n']} 段：画布上还没有出片，先跳过")
            continue
        i = c.get("selectedResultIndex") or 0
        url = urls[i] if 0 <= i < len(urls) else urls[-1]
        out = os.path.join(dest, f"第{s['n']}段.mp4")
        mark = out + ".url"
        if not (os.path.exists(out) and os.path.exists(mark) and open(mark).read() == url):
            print(f"  第 {s['n']} 段：下载中…")
            urllib.request.urlretrieve(url, out)
            open(mark, "w").write(url)
        found[s["n"]] = out
    return found


def get_clips(plan, folder=None):
    if folder:
        if not os.path.isdir(folder):
            sys.exit(f"找不到文件夹：{folder}")
        found = clips_from_folder(folder)
    else:
        found = clips_from_canvas(plan, os.path.join(plan["base"], "成片", "分段"))
    if not found:
        sys.exit("一段出片都没找到。档名要带段号，例：第1段.mp4")
    return found


# ---------- 剪辑表 ----------

def edit_table(md_path, plan):
    """读「剪辑表」：| # | 段 | 起 | 止 | 说明 |。没有表就照段号顺序，每段剪头尾。"""
    text = open(md_path, encoding="utf-8").read()
    m = re.search(r"^#{2,4}\s*剪辑表.*?$(.*?)(?=^#{1,4}\s|\Z)", text, re.M | re.S)
    rows = []
    if m:
        for line in m.group(1).splitlines():
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) < 4 or not cells[1].strip().isdigit():
                continue
            rows.append({"seg": int(cells[1]), "start": cells[2], "end": cells[3],
                         "note": cells[4] if len(cells) > 4 else ""})
    if not rows:
        rows = [{"seg": s["n"], "start": "头", "end": "尾", "note": ""} for s in plan["segments"]]
    return rows, bool(m)


def to_sec(v, clip_len, trim):
    v = v.strip()
    if v in ("头", "开头", ""):
        return trim
    if v in ("尾", "结尾", "end"):
        return max(trim, clip_len - trim)
    try:
        return float(v.rstrip("s秒"))
    except ValueError:
        sys.exit(f"剪辑表里看不懂这个时间：「{v}」（写秒数，或写「头」「尾」）")


def original_length(md_path):
    text = open(md_path, encoding="utf-8").read()
    m = re.search(r"^原片[：:].*?([\d.]+)\s*秒", text, re.M)
    return float(m.group(1)) if m else None


# ---------- 听写 ----------

def _real_ggml_models():
    out = []
    for d in (os.environ.get("WHISPER_MODEL_DIR", ""), os.path.expanduser("~/.cache/whisper"),
              os.path.expanduser("~/whisper-models"), "/opt/homebrew/share/whisper-cpp", "/usr/local/share/whisper-cpp"):
        if d and os.path.isdir(d):
            # for-tests-* 是 whisper.cpp 自带的测试用假模型，听写出来是乱码，不能用
            out += [os.path.join(d, f) for f in sorted(os.listdir(d))
                    if f.startswith("ggml-") and f.endswith(".bin")]
    return out


def transcribe(media, work_dir, lang="zh"):
    """有 whisper 就听写，回传文字；没有就回传 None。lang：台词是中文给 "zh"，英文给 "en"。"""
    os.makedirs(work_dir, exist_ok=True)
    wav = os.path.join(work_dir, "audio.wav")
    r = run(["ffmpeg", "-v", "error", "-y", "-i", media, "-vn", "-ac", "1", "-ar", "16000", wav])
    if r.returncode != 0:
        return None
    # 中文给提示，不然常出繁体；英文台词不能给中文提示，会被带偏成中文或别的语言
    hint = "以下是普通话的句子，用简体中文。" if lang == "zh" else ""
    if shutil.which("whisper"):
        r = run(["whisper", wav, "--model", "small", "--output_format", "txt", "--output_dir", work_dir,
                 "--language", lang] + (["--initial_prompt", hint] if hint else []))
        p = os.path.join(work_dir, "audio.txt")
        if r.returncode == 0 and os.path.exists(p):
            return open(p, encoding="utf-8").read().strip()
    if shutil.which("mlx_whisper"):
        r = run(["mlx_whisper", wav, "--model", "mlx-community/whisper-small-mlx", "--language", lang,
                 "--output-format", "txt", "--output-dir", work_dir] + (["--initial-prompt", hint] if hint else []))
        p = os.path.join(work_dir, "audio.txt")
        if r.returncode == 0 and os.path.exists(p):
            return open(p, encoding="utf-8").read().strip()
    models = _real_ggml_models()
    if shutil.which("whisper-cli") and models:
        base = os.path.join(work_dir, "audio")
        r = run(["whisper-cli", "-m", models[-1], "-f", wav, "-l", lang, "-otxt", "-of", base] + (["--prompt", hint] if hint else []))
        if r.returncode == 0 and os.path.exists(base + ".txt"):
            return open(base + ".txt", encoding="utf-8").read().strip()
    return None
