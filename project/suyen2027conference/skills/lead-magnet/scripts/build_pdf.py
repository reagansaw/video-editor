#!/usr/bin/env python3
"""把写好的 lead magnet 内容（一份 .md）做成可以直接发给客人的 PDF，顺便出一张封面图给落地页用。

用法:
    python3 build_pdf.py <内容.md>                 # 出在内容.md 旁边
    python3 build_pdf.py <内容.md> --out <文件夹>
    python3 build_pdf.py <内容.md> --html-only     # 只出 HTML（没有 Chrome / Edge 时）

出来的档案:
    <档名>.pdf     手机看的直版（A5），第一页是封面，最后一页是「下一步」
    <档名>.html    同样内容的网页版，可以自己用浏览器打开「打印 → 存成 PDF」
    <档名>-cover.png  封面图 1200×1600，落地页的封面就用这张

小红书版（拿掉联络方式和链接）：加 --no-contact，档名会多「-小红书版」，不会盖掉原来那份。

内容.md 的写法见 references/content-format.md。
只用 Python 标准库；出 PDF 和封面图要本机有 Chrome、Edge、Brave 或 Chromium 其中一个。
"""
import argparse
import html
import os
import re
import shutil
import subprocess
import sys
import tempfile

FIELDS = ("title", "subtitle", "tag", "brand", "author", "color", "contact", "note",
          "next_title", "next_text", "next_button", "next_link")


def parse_front(text):
    meta, body = {}, text
    if text.lstrip().startswith("---"):
        parts = text.lstrip().split("---", 2)
        if len(parts) == 3:
            body = parts[2]
            for line in parts[1].splitlines():
                if ":" in line or "：" in line:
                    k, v = re.split(r"[:：]", line, maxsplit=1)
                    meta[k.strip().lower()] = v.strip()
    return meta, body.strip("\n")


def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"【(?:填|确认|待补)(?:[:：][^】]*)?】", lambda m: "<mark>" + m.group(0) + "</mark>", s)
    s = re.sub(r"(?<![\w#])(\+?\d[\d\- ]{6,}\d)", r'<span class="nw">\1</span>', s)
    return s


def render_body(body):
    """很小的一套 markdown：# 章（另起一页）、## 小标、- [ ] 打勾、- 点、1. 步骤、> 提醒、| 表格 |、--- 换页。"""
    out, lines, i, first_h1 = [], body.splitlines(), 0, True
    while i < len(lines):
        ln = lines[i].rstrip()
        if not ln.strip():
            i += 1
            continue
        if ln.strip() == "---":
            out.append('<div class="pb"></div>')
            i += 1
        elif ln.startswith("# "):
            out.append(f'<h1 class="{"" if first_h1 else "pbb"}">{inline(ln[2:].strip())}</h1>')
            first_h1 = False
            i += 1
        elif ln.startswith("## "):
            out.append(f"<h2>{inline(ln[3:].strip())}</h2>")
            i += 1
        elif re.match(r"^\s*[-*] \[[ xX]?\] ", ln):
            items = []
            while i < len(lines) and re.match(r"^\s*[-*] \[[ xX]?\] ", lines[i]):
                items.append(re.sub(r"^\s*[-*] \[[ xX]?\] ", "", lines[i]).strip())
                i += 1
            out.append('<ul class="check">' + "".join(f"<li><i></i><span>{inline(x)}</span></li>" for x in items) + "</ul>")
        elif re.match(r"^\s*[-*] ", ln):
            items = []
            while i < len(lines) and re.match(r"^\s*[-*] ", lines[i]) and not re.match(r"^\s*[-*] \[", lines[i]):
                items.append(re.sub(r"^\s*[-*] ", "", lines[i]).strip())
                i += 1
            out.append("<ul>" + "".join(f"<li>{inline(x)}</li>" for x in items) + "</ul>")
        elif re.match(r"^\s*\d+[.、] ", ln):
            items = []
            while i < len(lines) and re.match(r"^\s*\d+[.、] ", lines[i]):
                items.append(re.sub(r"^\s*\d+[.、] ", "", lines[i]).strip())
                i += 1
            out.append('<ol class="steps">' + "".join(f"<li><span>{inline(x)}</span></li>" for x in items) + "</ol>")
        elif ln.startswith(">"):
            items = []
            while i < len(lines) and lines[i].startswith(">"):
                items.append(lines[i][1:].strip())
                i += 1
            out.append('<div class="tip">' + "<br>".join(inline(x) for x in items if x) + "</div>")
        elif ln.lstrip().startswith("|"):
            rows = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
                    rows.append(cells)
                i += 1
            if rows:
                head = "".join(f"<th>{inline(c)}</th>" for c in rows[0])
                rest = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in rows[1:])
                out.append(f"<table><thead><tr>{head}</tr></thead><tbody>{rest}</tbody></table>")
        else:
            para = []
            while i < len(lines) and lines[i].strip() and not re.match(r"^(#{1,2} |\s*[-*] |\s*\d+[.、] |>|\s*\||---\s*$)", lines[i]):
                para.append(lines[i].strip())
                i += 1
            out.append("<p>" + "<br>".join(inline(x) for x in para) + "</p>")
    return "\n".join(out)


def shade(hexcolor, f):
    """f < 1 调深，f > 1 往白色调亮。"""
    h = hexcolor.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    r, g, b = (int(h[k:k + 2], 16) for k in (0, 2, 4))
    if f <= 1:
        r, g, b = (int(c * f) for c in (r, g, b))
    else:
        r, g, b = (int(c + (255 - c) * (f - 1)) for c in (r, g, b))
    return f"#{r:02X}{g:02X}{b:02X}"


COLORS = {"深蓝": "#1F3A6E", "蓝": "#2F6FE0", "墨绿": "#1F7A5C", "绿": "#2E9B5F", "红": "#C8372D", "玫红": "#D03F58",
          "橙": "#E0752F", "金": "#B8862B", "紫": "#6B3FA0", "青": "#14808A", "咖啡": "#7A5230", "黑": "#222222"}


def title_html(title):
    """标题里用「/」分短语，换行只会落在短语之间。"""
    parts = [p.strip() for p in title.split("/") if p.strip()]
    return "".join(f'<span class="g">{inline(p)}</span>' for p in parts)


CSS = """
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;700;900&display=swap');
:root{--brand:%(brand)s;--deep:%(deep)s;--dark:%(dark)s;--soft:%(soft)s;--ink:#22201D;--muted:#5F5A53;--line:#E4DED3;--paper:#FFFFFF}
@page{size:148mm 210mm;margin:16mm 13mm 17mm}
@page:first{margin:0}
@page{@bottom-center{content:counter(page);font:400 8pt "Noto Sans SC",sans-serif;color:#9A948A}}
@page:first{@bottom-center{content:""}}
*{box-sizing:border-box}
html{-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{margin:0;font-family:"Noto Sans SC","PingFang SC","Microsoft YaHei",system-ui,sans-serif;color:var(--ink);font-size:11.5pt;line-height:1.75;background:var(--paper)}
.g{display:inline-block}
.nw{white-space:nowrap}
.cover{height:210mm;width:148mm;background:linear-gradient(155deg,var(--deep),var(--dark));color:#fff;padding:18mm 13mm 14mm;display:flex;flex-direction:column;break-after:page;position:relative;overflow:hidden}
.cover:before{content:"";position:absolute;right:-30mm;top:-30mm;width:95mm;height:95mm;border-radius:50%%;background:var(--brand);opacity:.55}
.cover>*{position:relative}
.cover .brand{font-weight:700;font-size:11pt;letter-spacing:.06em}
.cover .tag{display:inline-block;align-self:flex-start;margin-top:auto;background:#fff;color:var(--deep);font-weight:900;font-size:9.5pt;letter-spacing:.08em;padding:1.6mm 4mm;border-radius:99px}
.cover h1.t{font-size:34pt;line-height:1.22;font-weight:900;margin:6mm 0 5mm;padding:0;border:0;letter-spacing:-.01em}
.cover .sub{font-size:12pt;line-height:1.7;opacity:.92;margin:0 0 14mm}
.cover .by{border-top:1px solid rgba(255,255,255,.35);padding-top:5mm;font-size:10pt;line-height:1.6}
main{padding:0}
h1{font-size:19pt;line-height:1.3;font-weight:900;margin:0 0 5mm;padding-bottom:3mm;border-bottom:2.5pt solid var(--brand)}
h1.pbb{break-before:page}
h2{font-size:13pt;line-height:1.4;font-weight:900;margin:7mm 0 2.5mm;color:var(--deep);break-after:avoid}
p{margin:0 0 3.5mm}
strong{font-weight:900}
mark{background:#FFE9A8;color:#6B4A00;padding:0 .2em;border-radius:3px}
ul,ol{margin:0 0 4mm;padding-left:5.5mm}
li{margin-bottom:1.8mm;break-inside:avoid}
ul.check{list-style:none;padding:0}
ul.check li{display:flex;gap:3mm;align-items:flex-start;padding:2.6mm 0;border-bottom:1px solid var(--line);margin:0}
ul.check i{flex:0 0 5mm;height:5mm;border:1.6pt solid var(--brand);border-radius:1.2mm;margin-top:1.1mm}
ol.steps{list-style:none;padding:0;counter-reset:s}
ol.steps li{counter-increment:s;display:flex;gap:3.5mm;align-items:flex-start;margin-bottom:3mm}
ol.steps li:before{content:counter(s);flex:0 0 7mm;height:7mm;border-radius:50%%;background:var(--brand);color:#fff;font-weight:900;font-size:10pt;display:flex;align-items:center;justify-content:center;margin-top:.6mm}
.tip{background:var(--soft);border-left:3pt solid var(--brand);border-radius:0 3mm 3mm 0;padding:3.5mm 4.5mm;margin:0 0 4.5mm;font-size:10.8pt;break-inside:avoid}
table{width:100%%;border-collapse:collapse;margin:0 0 5mm;font-size:10pt;line-height:1.55;break-inside:avoid}
th{background:var(--deep);color:#fff;text-align:left;font-weight:700;padding:2.2mm 2.6mm}
td{padding:2.2mm 2.6mm;border-bottom:1px solid var(--line);vertical-align:top}
tbody tr:nth-child(even) td{background:#F7F3EC}
td:empty{height:12mm}
.pb{break-after:page}
.next{break-before:page;background:var(--soft);border-radius:5mm;padding:9mm 8mm;margin-top:4mm}
.next h1{border:0;padding:0;margin-bottom:4mm}
.next .btn{display:inline-block;background:var(--brand);color:#fff;font-weight:700;text-decoration:none;padding:3.2mm 8mm;border-radius:99px;margin-top:3mm;font-size:12pt}
.next .link{display:block;font-size:9pt;color:var(--muted);margin-top:3mm;word-break:break-all}
.foot{margin-top:9mm;font-size:8.8pt;line-height:1.7;color:var(--muted);border-top:1px solid var(--line);padding-top:4mm}
"""

COVER_ONLY_CSS = """
html,body{width:1200px;height:1600px;overflow:hidden}
.cover{width:1200px;height:1600px;padding:150px 110px 120px;break-after:auto}
.cover:before{right:-240px;top:-240px;width:780px;height:780px}
.cover .brand{font-size:36px}
.cover .tag{font-size:32px;padding:14px 34px}
.cover h1.t{font-size:112px;margin:50px 0 40px}
.cover .sub{font-size:42px;margin-bottom:110px}
.cover .by{font-size:34px;padding-top:40px}
"""


def cover_block(m):
    by = " · ".join(x for x in (m.get("author", ""), m.get("contact", "")) if x)
    return (f'<section class="cover"><div class="brand">{inline(m.get("brand", ""))}</div>'
            f'<div class="tag">{inline(m.get("tag", "免费指南"))}</div>'
            f'<h1 class="t">{title_html(m["title"])}</h1>'
            f'<p class="sub">{inline(m.get("subtitle", ""))}</p>'
            + (f'<div class="by">{inline(by)}</div>' if by else "") + "</section>")


def page(m, inner, extra_css=""):
    c = (m.get("color") or "深蓝").strip()
    c = COLORS.get(c, c)
    if not re.fullmatch(r"#?[0-9a-fA-F]{3}([0-9a-fA-F]{3})?", c):
        sys.exit(f"color 看不懂：「{c}」。写色号（例如 #1F3A6E），或这些名字之一：" + "、".join(COLORS))
    c = "#" + c.lstrip("#")
    css = CSS % {"brand": c, "deep": shade(c, .78), "dark": shade(c, .42), "soft": shade(c, 1.9)}
    return (f'<!doctype html><html lang="zh-Hans"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(m["title"].replace("/", ""))}</title>'
            f"<style>{css}{extra_css}</style></head><body>{inner}</body></html>")


def find_browser():
    env = os.environ.get("CHROME_PATH")
    if env and os.path.exists(env):
        return env
    cands = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
        "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
    ]
    for base in (os.environ.get("PROGRAMFILES"), os.environ.get("PROGRAMFILES(X86)"), os.environ.get("LOCALAPPDATA")):
        if base:
            cands += [os.path.join(base, r"Google\Chrome\Application\chrome.exe"),
                      os.path.join(base, r"Microsoft\Edge\Application\msedge.exe"),
                      os.path.join(base, r"BraveSoftware\Brave-Browser\Application\brave.exe")]
    for c in cands:
        if os.path.exists(c):
            return c
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "microsoft-edge", "msedge", "chrome"):
        p = shutil.which(name)
        if p:
            return p
    return None


def chrome(browser, args, url):
    with tempfile.TemporaryDirectory() as prof:
        cmd = [browser, "--headless=new", "--disable-gpu", "--no-first-run", "--hide-scrollbars",
               f"--user-data-dir={prof}", "--virtual-time-budget=8000"] + args + [url]
        try:
            return subprocess.run(cmd, capture_output=True, text=True, timeout=120).returncode == 0
        except (subprocess.TimeoutExpired, OSError):
            return False


def file_url(path):
    from pathlib import Path
    return Path(path).resolve().as_uri()


def main():
    ap = argparse.ArgumentParser(description="lead magnet 内容 → PDF + 封面图")
    ap.add_argument("content")
    ap.add_argument("--out", help="输出文件夹，默认和内容.md 同一个")
    ap.add_argument("--html-only", action="store_true")
    ap.add_argument("--no-contact", action="store_true",
                    help="小红书版：拿掉联络方式、按钮和链接，档名加「-小红书版」")
    a = ap.parse_args()

    src = os.path.abspath(os.path.expanduser(a.content))
    if not os.path.isfile(src):
        sys.exit(f"找不到内容档：{src}")
    meta, body = parse_front(open(src, encoding="utf-8").read())
    unknown = [k for k in meta if k not in FIELDS]
    if unknown:
        print("  看不懂这些栏位，先跳过：" + "、".join(unknown))
    if not meta.get("title"):
        sys.exit("内容档最上面要有 title。写法见 references/content-format.md")
    if not body.strip():
        sys.exit("内容是空的。")
    found = re.findall(r"【(?:填|确认|待补)(?:[:：][^】]*)?】", open(src, encoding="utf-8").read())
    left = sorted(set(found))
    if a.no_contact:
        for k in ("contact", "next_button", "next_link"):
            meta.pop(k, None)

    out = os.path.abspath(os.path.expanduser(a.out)) if a.out else os.path.dirname(src)
    os.makedirs(out, exist_ok=True)
    stem = os.path.splitext(os.path.basename(src))[0] + ("-小红书版" if a.no_contact else "")

    nxt = ""
    if meta.get("next_title") or meta.get("next_text"):
        link = meta.get("next_link", "")
        btn = (f'<a class="btn" href="{html.escape(link)}">{inline(meta.get("next_button", "联络我们"))}</a>'
               f'<span class="link">{html.escape(link)}</span>') if link else ""
        nxt = (f'<section class="next"><h1>{inline(meta.get("next_title", "下一步"))}</h1>'
               f'<p>{inline(meta.get("next_text", ""))}</p>{btn}</section>')
    foot_bits = [x for x in (meta.get("brand"), meta.get("contact")) if x]
    foot = '<div class="foot">' + inline(" · ".join(foot_bits)) + (("<br>" + inline(meta["note"])) if meta.get("note") else "") + "</div>"

    full = page(meta, cover_block(meta) + "<main>" + render_body(body) + nxt + foot + "</main>")
    html_path = os.path.join(out, stem + ".html")
    open(html_path, "w", encoding="utf-8").write(full)
    print(f"  网页版：{html_path}")

    if a.html_only:
        print("  只出 HTML。要 PDF：用浏览器打开它 → 打印 → 存成 PDF（纸张 A5，边距默认，勾「背景图形」）。")
    else:
        browser = find_browser()
        if not browser:
            print("  找不到 Chrome / Edge / Brave，所以没出 PDF 和封面图。")
            print("  用任何浏览器打开上面的网页版 → 打印 → 存成 PDF（纸张 A5，勾「背景图形」）；封面图就截第一页。")
        else:
            pdf_path = os.path.join(out, stem + ".pdf")
            ok = chrome(browser, ["--no-pdf-header-footer", f"--print-to-pdf={pdf_path}"], file_url(html_path))
            if ok and os.path.exists(pdf_path):
                print(f"  PDF：{pdf_path}（{os.path.getsize(pdf_path) / 1e6:.1f} MB）")
            else:
                print("  PDF 没出成功。用浏览器打开网页版 → 打印 → 存成 PDF。")
            cov_html = os.path.join(out, "." + stem + "-cover.html")
            open(cov_html, "w", encoding="utf-8").write(page(meta, cover_block(meta), COVER_ONLY_CSS))
            cov = os.path.join(out, stem + "-cover.png")
            ok = chrome(browser, ["--window-size=1200,1600", "--force-device-scale-factor=1", f"--screenshot={cov}"], file_url(cov_html))
            os.remove(cov_html)
            print(f"  封面图：{cov}" if ok and os.path.exists(cov) else "  封面图没出成功，截 PDF 第一页来用。")

    if left:
        print(f"\n还有 {len(found)} 处没填，发给客人之前要补完（PDF 里标了黄色）：")
        for x in left:
            print("  - " + x + (f" ×{found.count(x)}" if found.count(x) > 1 else ""))


if __name__ == "__main__":
    main()
