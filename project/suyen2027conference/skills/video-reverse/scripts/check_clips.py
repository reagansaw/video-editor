#!/usr/bin/env python3
"""出片后检查：台词有没有念对、画面有没有走样。

用法:
    python3 check_clips.py <反推结果.md>                    # 从 studio 画布拿每段选中的出片（要钥匙）
    python3 check_clips.py <反推结果.md> --clips <文件夹>    # 用你自己下载好的出片（档名带段号：第1段.mp4）

产出（放在 <md 文件夹>/检查/）:
    检查报告.md          每段：台词对照（听写 vs 稿子）、品牌名、要人工听的地方、要看的图
    第N段-画面.jpg       每段每秒一格的画面条，拿来跟人物照、产品照对比

听写要本机装了 whisper（uv tool install openai-whisper）；没装就只出画面条。
画面有没有变脸、多了眼镜、logo 走样，要由 Claude 打开画面条和素材图一起看（脚本不会判断）。
只用 Python 标准库 + ffmpeg。
"""
import argparse
import difflib
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import clips as c  # noqa: E402

NUM = re.compile(r"\b(?:zero|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand|million|percent)(?:-\w+)?\b|\d[\d,.]*%?", re.I)
PUNCT = re.compile(r"[\s，。！？、；：,.!?;:「」『』“”\"'()（）…—\-~～]+")


def norm(s):
    return PUNCT.sub("", s).lower()


def expected_lines(prompt):
    """从提示词「声音」那一块拿出每句台词和说话的人。"""
    lines = []
    for m in re.finditer(r"^(?:[\d.]+\s*[–-]\s*[\d.]+\s*s?\s*)?(.{0,60}?)说[：:]\s*「(.+?)」", prompt, re.M):
        raw, text = m.group(1).strip(), m.group(2).strip()
        raw = re.split(r"[。；]", raw)[-1]  # 「声音：街道环境声。画外音用…说」只留最后一句
        who = re.split(r"[（(用在]", raw)[0].strip() or raw[:12]
        lines.append({"who": who, "text": text, "own_voice": "@audio" in raw})
    # 画外音逐句列的写法：「1–4s：「…」」
    for m in re.finditer(r"^[\d.]+\s*[–-]\s*[\d.]+\s*s?\s*[：:]\s*「(.+?)」\s*$", prompt, re.M):
        lines.append({"who": "画外音", "text": m.group(1).strip(), "own_voice": "@audio" in prompt})
    return lines


def language(lines):
    """台词大多是英文字母就用英文听写，不然用中文。"""
    s = "".join(ln["text"] for ln in lines)
    latin = len(re.findall(r"[A-Za-z]", s))
    return "en" if latin > len(re.sub(r"\s", "", s)) * 0.5 else "zh"


def best_match(line, heard):
    """在听写里找最像这句台词的一段，回传相似度 0–1。"""
    a, h = norm(line), norm(heard)
    if not a:
        return 1.0
    if not h:
        return 0.0
    n, best = len(a), 0.0
    for i in range(0, max(1, len(h) - n + 1)):
        for w in (n - 2, n, n + 2):
            if w <= 0:
                continue
            r = difflib.SequenceMatcher(None, a, h[i:i + w]).ratio()
            best = max(best, r)
    return best


def contact_sheet(src, out, cols=6):
    L = c.duration(src)
    n = max(1, int(L))
    rows = (n + cols - 1) // cols
    vf = f"fps=1,scale=240:-2,tile={cols}x{rows}:padding=4:color=black"
    r = c.run(["ffmpeg", "-v", "error", "-y", "-ss", "0.5", "-i", src, "-frames:v", "1", "-vf", vf, out])
    return r.returncode == 0


def main():
    ap = argparse.ArgumentParser(description="出片后检查：台词和画面")
    ap.add_argument("md")
    ap.add_argument("--clips", help="出片所在的文件夹；不给就从 studio 画布下载")
    a = ap.parse_args()

    c.need_ffmpeg()
    plan = c.b.parse(a.md)
    found = c.get_clips(plan, a.clips)
    out_dir = os.path.join(plan["base"], "检查")
    os.makedirs(out_dir, exist_ok=True)

    report = [f"# 出片检查：{plan['title']}", ""]
    heard_any, flags = False, 0
    for s in plan["segments"]:
        n = s["n"]
        report.append(f"## 第 {n} 段")
        src = found.get(n)
        if not src:
            report += ["还没有出片，跳过。", ""]
            continue
        sheet = os.path.join(out_dir, f"第{n}段-画面.jpg")
        contact_sheet(src, sheet)
        refs = []
        for i, k in s["refs"]:
            asset = plan["assets"].get(k) or {}
            f = asset.get("file")
            where = (f"（`{os.path.relpath(f, plan['base'])}`）" if f
                     else "（用图片模型生成的，在 studio 画布上看）" if asset.get("prompt") else "（素材清单里没有档案）")
            refs.append(f"@image{i} = {k}" + where)
        report.append(f"- 画面条：`{os.path.relpath(sheet, plan['base'])}`（每秒一格，从 0.5 秒开始）")
        if refs:
            report.append("- 要对照的素材：" + "；".join(refs))
        report.append("- 要看：脸和发型有没有变、有没有多出眼镜或配件、衣服对不对、产品和 logo 有没有走样、多余手指、画面里有没有字")

        lines = expected_lines(s["prompt"])
        heard = c.transcribe(src, os.path.join(out_dir, f".tmp{n}"), language(lines)) if lines else None
        if lines and heard is None:
            report.append("- 台词：本机没有 whisper，没有听写。请自己听一遍，或装 whisper 后重跑（uv tool install openai-whisper）。")
        elif lines:
            heard_any = True
            report += ["", f"听写：{heard or '（听不到人声）'}", "",
                       "| 台词（稿子） | 谁说 | 对得上 | 要注意 |", "|---|---|---|---|"]
            for ln in lines:
                score = best_match(ln["text"], heard or "")
                num_only = False
                if score < 0.75 and NUM.search(ln["text"]):  # 听写把数字写成 2800、100%，跟稿子的拼法对不上
                    s2 = best_match(NUM.sub(" ", ln["text"]), NUM.sub(" ", heard or ""))
                    if s2 >= 0.75:
                        score, num_only = s2, True
                mark = "✅" if score >= 0.75 else ("⚠️" if score >= 0.5 else "❌")
                notes = []
                latin = re.findall(r"[A-Za-z][A-Za-z\-]+", ln["text"])
                missing = [w for w in latin if w.lower().replace("-", "") not in (heard or "").lower().replace("-", "").replace(" ", "")]
                missing = [w for w in missing if not NUM.fullmatch(w)]
                if num_only:
                    notes.append("数字被听写成阿拉伯数字，对稿时略过；听一下数字念得对不对")
                if missing:
                    notes.append("英文 / 品牌名要人工听：" + "、".join(missing))
                if score < 0.75:
                    notes.append("念错、漏讲或被吞掉，听一遍")
                    flags += 1
                report.append(f"| {ln['text']} | {ln['who'] or '—'} | {mark} {score:.0%} | {'；'.join(notes) or '—'} |")
            voiced = [ln for ln in lines if ln["own_voice"]]
            others = [ln for ln in lines if not ln["own_voice"]]
            if voiced and others:
                report.append("")
                report.append("- 这段接了真声（@audio）：听一下没接真声的人（" + "、".join(sorted({o['who'] for o in others if o['who']})) +
                              "）是不是被换成同一把声音。听写分不出声音是谁的。")
        report.append("")
        tmpd = os.path.join(out_dir, f".tmp{n}")
        if os.path.isdir(tmpd):
            for f in os.listdir(tmpd):
                os.remove(os.path.join(tmpd, f))
            os.rmdir(tmpd)

    report.append("## 怎么处理")
    report.append("- 台词念错：品牌名、英文缩写最容易错。写法改成嘴巴讲的样子重跑那一段，或那一句用真声 / AI 配音后制换掉（见 seedance-rules「念错字」）。")
    report.append("- 画面走样：只重跑那一段；走样只有一两秒的，粗剪时用剪辑表把那几秒剪掉，或盖一段 B-roll。")
    path = os.path.join(out_dir, "检查报告.md")
    open(path, "w", encoding="utf-8").write("\n".join(report) + "\n")
    print(f"检查报告：{path}")
    print(f"画面条：{out_dir}/第N段-画面.jpg")
    if heard_any:
        print(f"台词对不上的句子：{flags} 句" if flags else "台词都对得上（英文、品牌名还是要人工听）")
    else:
        print("没有听写（没台词或本机没装 whisper）。")


if __name__ == "__main__":
    main()
