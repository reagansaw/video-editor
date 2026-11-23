#!/usr/bin/env python3
"""把每段出片照「剪辑表」接成一支粗剪。

用法:
    python3 assemble.py <反推结果.md>                     # 从 studio 画布拿每段选中的出片（要钥匙）
    python3 assemble.py <反推结果.md> --clips <文件夹>     # 用你自己下载好的出片（档名带段号：第1段.mp4）
    python3 assemble.py <反推结果.md> --trim 0.4           # 「头」「尾」剪掉几秒（默认 0.5）

剪辑表写在反推结果的「六、后制清单」里（格式见 references/output-template.md）。
没有剪辑表就照段号顺序接，每段剪掉头尾。
出来的是粗剪：只有画面和原声，字幕、花字、配乐、logo 还要后制。
只用 Python 标准库 + ffmpeg，不需要 API key（从画布下载才要 studio 钥匙）。
"""
import argparse
import os
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import clips as c  # noqa: E402

SIZES = {"9:16": (720, 1280), "16:9": (1280, 720), "1:1": (1080, 1080),
         "3:4": (960, 1280), "4:3": (1280, 960), "21:9": (1680, 720)}
FPS = 24


def main():
    ap = argparse.ArgumentParser(description="照剪辑表把每段出片接成粗剪")
    ap.add_argument("md")
    ap.add_argument("--clips", help="出片所在的文件夹；不给就从 studio 画布下载")
    ap.add_argument("--trim", type=float, default=c.TRIM, help="「头」「尾」各剪掉几秒，默认 0.5")
    ap.add_argument("--out", help="输出档名，默认 <md 文件夹>/成片/粗剪.mp4")
    a = ap.parse_args()

    c.need_ffmpeg()
    plan = c.b.parse(a.md)
    found = c.get_clips(plan, a.clips)
    rows, had_table = c.edit_table(a.md, plan)
    W, H = SIZES.get(plan["ratio"], (720, 1280))
    out = a.out or os.path.join(plan["base"], "成片", "粗剪.mp4")
    os.makedirs(os.path.dirname(out), exist_ok=True)

    if not had_table:
        print("反推结果里没有「剪辑表」，先照段号顺序接，每段剪掉头尾。")
    tmp = tempfile.mkdtemp(prefix="assemble_")
    pieces, total, missing = [], 0.0, []
    try:
        for k, r in enumerate(rows, 1):
            src = found.get(r["seg"])
            if not src:
                missing.append(r["seg"])
                continue
            L = c.duration(src)
            s, e = c.to_sec(r["start"], L, a.trim), c.to_sec(r["end"], L, a.trim)
            e = min(e, L)
            if e - s < 0.2:
                print(f"  第 {k} 行（第 {r['seg']} 段 {r['start']}–{r['end']}）太短或起止颠倒，跳过")
                continue
            piece = os.path.join(tmp, f"{k:03d}.mp4")
            vf = (f"scale={W}:{H}:force_original_aspect_ratio=decrease,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2,"
                  f"setsar=1,fps={FPS},format=yuv420p")
            cmd = ["ffmpeg", "-v", "error", "-y", "-ss", f"{s:.3f}", "-t", f"{e - s:.3f}", "-i", src]
            if c.has_audio(src):
                cmd += ["-map", "0:v:0", "-map", "0:a:0"]
            else:
                cmd += ["-f", "lavfi", "-t", f"{e - s:.3f}", "-i", "anullsrc=r=48000:cl=stereo", "-map", "0:v:0", "-map", "1:a:0"]
            cmd += ["-vf", vf, "-af", "aresample=48000", "-ac", "2", "-c:v", "libx264", "-preset", "veryfast",
                    "-crf", "18", "-c:a", "aac", "-b:a", "160k", "-shortest", piece]
            res = c.run(cmd)
            if res.returncode != 0:
                sys.exit(f"剪第 {r['seg']} 段时出错：\n{res.stderr[-800:]}")
            pieces.append(piece)
            total += e - s
            print(f"  {k:>2}. 第 {r['seg']} 段 {s:5.2f}–{e:5.2f} 秒 （{e - s:4.1f} 秒）{('· ' + r['note']) if r['note'] else ''}")
        if not pieces:
            sys.exit("没有可以接的片段。")
        lst = os.path.join(tmp, "list.txt")
        with open(lst, "w", encoding="utf-8") as f:
            for p in pieces:
                f.write(f"file '{p}'\n")
        res = c.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy",
                     "-movflags", "+faststart", out])
        if res.returncode != 0:
            sys.exit(f"接片时出错：\n{res.stderr[-800:]}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print(f"\n粗剪：{out}（{c.duration(out):.1f} 秒）")
    orig = c.original_length(a.md)
    if orig:
        diff = total - orig
        note = "节奏跟原片差不多" if abs(diff) <= max(1.5, orig * 0.05) else ("比原片长，节奏会变慢，看哪段可以再剪" if diff > 0 else "比原片短，检查有没有剪掉台词")
        print(f"原片 {orig:.1f} 秒 → 粗剪 {total:.1f} 秒（{diff:+.1f} 秒），{note}")
    if missing:
        print(f"还没有出片、先跳过的段：{sorted(set(missing))}")
    print("下一步：字幕、花字、配乐、logo 照后制清单做（剪辑 skill 可以接手）。")


if __name__ == "__main__":
    main()
