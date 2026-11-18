"""12 生肖 2027 财运指南 PDF（A4）：每个生肖一份 HTML → Playwright 印成 PDF。内容用白话版 data-plain.json。"""
import json, re, sys, html, os
S, OUT = sys.argv[1], sys.argv[2]
data = json.load(open(os.path.join(S, 'ref/data-plain.json'), encoding='utf8'))
site = open(os.path.join(S, 'ref/page.html'), encoding='utf8').read()
sc = re.findall(r'<script[^>]*>([\s\S]*?)</script>', site)[0]
paths = re.findall(r"'([^']*)'", re.search(r'const animalPaths=\[([\s\S]*?)\];', sc).group(1))
EN = ['RAT','OX','TIGER','RABBIT','DRAGON','SNAKE','HORSE','GOAT','MONKEY','ROOSTER','DOG','PIG']
TAG = ['人缘里找机会。','变动中留余地。','把机会接稳。','让成果留下来。','走出去，看机会。','为收入多找条路。','把好运做成事。','先稳住，再出发。','让实力被看见。','把专业用出来。','把合作说清楚。','让人脉走近一步。']
FILE = ['rat','ox','tiger','rabbit','dragon','snake','horse','goat','monkey','rooster','dog','pig']
stems, branches = '甲乙丙丁戊己庚辛壬癸', '子丑寅卯辰巳午未申酉戌亥'
e = lambda s: html.escape(s, quote=False)

CSS = '''
@page{size:A4;margin:0}
*{box-sizing:border-box}
body{margin:0;font-family:"Noto Sans SC","PingFang SC",sans-serif;color:#2A1418;background:#FAF5E6;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:210mm;min-height:297mm;padding:18mm 17mm 16mm;position:relative;page-break-after:always;background:#FAF5E6}
.page:last-child{page-break-after:auto}
.cover{background:radial-gradient(60% 50% at 85% 20%,#DC4D65 0%,rgba(220,77,101,0) 70%),radial-gradient(60% 60% at 0% 100%,#8E2438 0%,rgba(142,36,56,0) 60%),#B83349;color:#fff;display:flex;flex-direction:column}
.cover .brand{font:900 13px/1 "Inter",sans-serif;letter-spacing:4px;color:#EFDFB3}
.cover .animal{width:150px;height:150px;color:#EFDFB3;margin:26mm 0 8mm}
.cover h1{font-size:44px;font-weight:900;line-height:1.25;margin:0}
.cover h1 em{font-style:normal;color:#EFDFB3}
.cover .sub{font-size:20px;font-weight:700;margin-top:8px;color:#FFFAEB}
.cover .rank{margin-top:14mm;padding-top:8mm;border-top:1px solid rgba(255,250,235,.3)}
.cover .rank .rl{font-size:16px;font-weight:900;letter-spacing:1px}
.cover .rank b{font:900 120px/1 "Inter",sans-serif;color:#EFDFB3;letter-spacing:-5px}
.cover .rank span{font-size:24px;font-weight:900;color:rgba(255,250,235,.85);margin-left:10px}
.cover .kw{display:flex;gap:8px;margin-top:8mm}
.cover .kw span{background:#EFDFB3;color:#3B0F18;font-weight:800;font-size:14px;padding:6px 14px;border-radius:999px}
.cover .by{margin-top:auto;font-size:14px;line-height:1.7;color:rgba(255,250,235,.85)}
.cover .by b{color:#fff;font-size:18px}
.sl{display:flex;align-items:center;gap:10px;font-size:13px;font-weight:700;letter-spacing:1px;color:#B83349}
.sl i{font:900 12px/1 "Inter",sans-serif;font-style:normal;width:28px;height:28px;border-radius:50%;display:grid;place-items:center;background:#F6E3E6}
h2{font-size:30px;font-weight:900;line-height:1.3;margin:8px 0 10px}
h2 em{font-style:normal;color:#D03F58}
.desc{font-size:14px;line-height:1.85;color:#5E4A4C;margin:0 0 6mm}
.pt{background:#fff;border-radius:14px;border-top:3px solid #D03F58;padding:12px 16px;margin:0 0 4mm;break-inside:avoid}
.pt.cau{border-top-color:#3B0F18}
.pt h3{font-size:17px;font-weight:900;margin:0}
.pt p{font-size:13.5px;line-height:1.8;color:#5E4A4C;margin:4px 0 0}
.note{font-size:12px;line-height:1.7;color:#5E4A4C;margin:0 0 4mm}
.note b{color:#2A1418}
.stars{font-size:14px;font-weight:700;margin:0 0 4mm}.stars b{color:#D03F58;letter-spacing:2px;margin-left:4px}
.sec{margin-bottom:8mm}
.yr{background:#fff;border-radius:14px;padding:12px 16px;margin:0 0 4mm;break-inside:avoid;border-left:4px solid #EFDFB3}
.yr .yt{font-size:12px;font-weight:700;letter-spacing:1px;color:#B83349}
.yr h3{font-size:18px;font-weight:900;margin:3px 0 4px}
.yr p{font-size:13px;line-height:1.75;color:#5E4A4C;margin:4px 0 0}
.yr .act{background:#F6E3E6;border-radius:10px;padding:8px 12px;margin-top:6px;font-size:13px;font-weight:700;color:#2A1418}
.yr .act b{display:block;font-size:11px;color:#B83349;letter-spacing:1px}
.q{display:flex;gap:12px;background:#fff;border:1.5px solid #E6D9B8;border-radius:12px;padding:10px 14px;margin:0 0 3mm;break-inside:avoid}
.q .n{flex:0 0 26px;height:26px;border-radius:50%;background:#F6E3E6;color:#B83349;font:900 13px/26px "Inter",sans-serif;text-align:center}
.q b{display:block;font-size:15px}.q small{display:block;font-size:12.5px;color:#5E4A4C;margin-top:2px}
.card{background:#FFFAEB;border:1.5px solid #D9C08E;border-radius:16px;padding:16px 18px;break-inside:avoid}
.card .k{font:900 11px/1 "Inter",sans-serif;letter-spacing:3px;color:#B83349}
.card h3{font-size:19px;font-weight:900;margin:6px 0 8px}
.card .r{padding:8px 0;border-top:1px dashed #D9C08E}.card .r:first-of-type{border-top:0}
.card .r b{display:block;font-size:12px;letter-spacing:1px;color:#B83349}.card .r p{font-size:13.5px;line-height:1.7;margin:2px 0 0}
.card .kw{display:flex;gap:6px}.card .kw span{background:#EFDFB3;font-size:12px;font-weight:800;padding:3px 10px;border-radius:999px}
.conf{background:#3B0F18;color:#FFFAEB;border-radius:18px;padding:16px 20px;margin-top:6mm;break-inside:avoid}
.conf .k{font:900 11px/1 "Inter",sans-serif;letter-spacing:3px;color:#EFDFB3}
.conf h3{font-size:22px;font-weight:900;margin:6px 0}
.conf p{font-size:13px;line-height:1.75;margin:4px 0;color:rgba(255,250,235,.88)}
.conf .d{font-weight:700;color:#EFDFB3}
.foot{position:absolute;left:17mm;right:17mm;bottom:8mm;display:flex;justify-content:space-between;font-size:10px;color:#9A8A8C}
'''

def stars(s):
    return ''.join(f'<span>{a}<b>{b}</b></span>　' for a, b in re.findall(r'(\S+运)｜([★☆]+)', s))

def build(i, d):
    z = d['z']
    tags = ''.join(f'<span>{e(k)}</span>' for k in d['keywords'].split('・'))
    years = [(y, stems[(y-4) % 10] + branches[i]) for y in range(2027, 1929, -1) if (y-4) % 12 == i]
    bypl = {}
    for y, pl in years: bypl.setdefault(pl, []).append(y)
    routes = []
    for pl, ys in bypl.items():
        c = d['cards'].get(pl)
        if not c: continue
        paras = ''.join(f'<div class="act"><b>现在可以做的一步</b>{e(p[4:])}</div>' if p.startswith('马上做：') else f'<p>{e(p)}</p>' for p in c['paragraphs'])
        routes.append(f'<div class="yr"><div class="yt">{" / ".join(str(y) for y in ys)} 年出生（{pl}年）</div><h3>{e(c["title"])}</h3>{paras}</div>')
    L = [len(re.sub(r'<[^>]+>', '', r)) for r in routes]
    cut = min(range(1, len(routes)), key=lambda k: max(sum(L[:k]) + 120, sum(L[k:])))  # 第一页还有标题和说明，多算一点
    qs = ''.join(f'<div class="q"><span class="n">{k+1}</span><span><b>{e(a)}</b><small>{e(b)}</small></span></div>' for k, (a, b) in enumerate(d['checks']))
    foot = f'<div class="foot"><span>林舒苑 · 2027 生肖财运指南 · 属{z}</span><span>解读供参考，行动需核实</span></div>'
    return f'''<!doctype html><html lang="zh-Hans"><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@700;900&family=Noto+Sans+SC:wght@400;700;900&display=swap">
<style>{CSS}</style></head><body>
<section class="page cover">
  <div class="brand">MASTER SUYEN LIM · 2027</div>
  <svg class="animal" viewBox="0 0 96 96" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">{paths[i]}</svg>
  <h1>属{z}的你，<br><em>{TAG[i]}</em></h1>
  <div class="sub">{e(d["headline"])}</div>
  <div class="kw">{tags}</div>
  <div class="rank"><div class="rl">《运势大破解》2027 年度排名</div><b>{d["rank"]:02d}</b><span>/ 12 生肖</span></div>
  <div class="by"><b>2027 生肖财运指南</b><br>林舒苑 · 人生战略导师<br>依据《2027年运势大破解》整理</div>
</section>
<section class="page">
  <div class="sec"><div class="sl"><i>01</i>你的年度财运</div><h2>今年的财，<em>别找错地方</em></h2>
    <p class="desc">{e(d["intro"])}</p><p class="stars">{stars(d["stars"])}</p>
    <div class="pt"><h3>你的正财，从这里来</h3><p>{e(d["facts"][0][1])}</p></div>
    <div class="pt"><h3>你的钱，最容易漏在这里</h3><p>{e(d["facts"][1][1])}</p></div>
    <p class="note"><b>简单说：</b>{e(d["reading"])}</p></div>
  <div class="sec"><div class="sl"><i>02</i>你的贵人</div><h2>跟错人，<em>一年白做</em></h2>
    <div class="pt"><h3>你的贵人，是这样的人</h3><p>{e(d["facts"][2][1])}</p></div>
    <div class="pt"><h3>想到谁，就主动一点</h3><p>读到这里，你脑中有没有浮现一个人？主动联系他，请他帮你推进一件具体的事。</p></div></div>
  {foot}
</section>
<section class="page">
  <div class="sec"><div class="sl"><i>03</i>你的出生年份</div><h2>同样属{z}，<em>财路不一样</em></h2>
    <p class="desc">找到你出生的那一年，看属于你的求财路线。1 月到 2 月初（立春之前）出生的朋友，生肖算前一年。</p>{"".join(routes[:cut])}</div>
  {foot}
</section>
<section class="page">
  <div class="sec"><div class="sl"><i>03</i>你的出生年份（续）</div>{"".join(routes[cut:])}</div>
  {foot}
</section>
<section class="page">
  <div class="sec"><div class="sl"><i>04</i>你的时机</div><h2>时机不对，<em>再努力也白费</em></h2>
    <div class="pt"><h3>这些时段，主动出手</h3><p>{e(d["facts"][3][1])}</p></div>
    <div class="pt cau"><h3>这些时段，先看清楚</h3><p>{e(d["facts"][4][1])}</p></div></div>
  <div class="sec"><div class="sl"><i>05</i>答应之前</div><h2>很多亏损，都来自一句<em>「好啊」</em></h2>
    <p class="desc">{e(d["checkIntro"])} 答应之前，先拿这 5 个问题问清楚。</p>{qs}</div>
  {foot}
</section>
<section class="page">
  <div class="sec"><div class="sl"><i>06</i>你的行动卡</div><h2>看完不做，<em>等于没看</em></h2>
    <div class="card"><div class="k">2027 · MY ACTION CARD</div><h3>属{z}的我，先落实这一步。</h3>
      <div class="r"><b>我的 2027 关键词</b><div class="kw">{tags}</div></div>
      <div class="r"><b>今年的财，往这里找</b><p>{e(d["facts"][0][1])}</p></div>
      <div class="r"><b>我要主动接近的人</b><p>{e(d["facts"][2][1])}</p></div>
      <div class="r"><b>主动出手的时段</b><p>{e(d["facts"][3][1])}</p></div>
      <div class="r"><b>要仔细的地方</b><p>{e(d["facts"][4][1])}</p></div></div></div>
  <div class="conf"><div class="k">MASTER SUYEN LIM · 2027</div><h3>生肖只是第一步：来 2027 奇门遁甲战略大会</h3>
    <p>带着你正在考虑的那件事来，和林舒苑一起看全年方向与时机，把下一步想得更清楚。</p>
    <p class="d">2027 年 1 月 8–10 日（五、六、日）· 1 月 8 日 8:30pm ｜ 1 月 9–10 日 1pm–6pm · Zoom 线上直播 · 免费</p>
    <p>报名：2027qimenconference.suyenlim.com</p></div>
  <p class="note" style="margin-top:6mm">本指南依据《2027年运势大破解》整理。生肖解读与方向供传统文化参考和自我梳理；真正推进合作，仍需核实需求、资源与条件。© Supreme Fortunity Sdn Bhd</p>
  {foot}
</section>
</body></html>'''

os.makedirs(OUT, exist_ok=True)
for i, d in enumerate(data):
    open(os.path.join(OUT, f'guide_{FILE[i]}.html'), 'w', encoding='utf8').write(build(i, d))
print('html done', len(data))
