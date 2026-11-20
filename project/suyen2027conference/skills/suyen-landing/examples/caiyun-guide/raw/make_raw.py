"""把 asis 版落地页（optin.html）变成 raw 版：加「输入出生日期 → 年柱地支」、自己处理报名弹窗和报名送出（raw 页没有平台钩子）。
用法：python3 make_raw.py <optin.html> <lichun.json> <out.html> <funnel 页 slug> <报名成功网址>"""
import json, sys, os as _os_

src, lcf, out, FUNNEL_SLUG, NEXT, OWN_SLUG = sys.argv[1:7]
PDF_URLS = json.load(open(sys.argv[7])) if len(sys.argv) > 7 else {}
PDFZ = json.load(open(_os_.environ['PDFZ'])) if _os_.environ.get('PDFZ') else {}
h = open(src, encoding='utf8').read()
lc = {int(k): v for k, v in json.load(open(lcf)).items() if 1929 <= int(k) <= 2028}

CSS = '''
/* ===== 出生日期 → 年柱地支（raw 版） ===== */
.dob{margin:0 0 16px;padding:0 0 16px;border-bottom:1.5px dashed var(--line)}
.dob b{display:block;font-size:20px;font-weight:900;margin-bottom:4px}
.dob p{font-size:14px;line-height:1.6;color:var(--muted)}
.dob-row{display:grid;grid-template-columns:1fr;gap:10px;margin-top:12px}
.dob label{display:block;font-size:14px;font-weight:700;color:var(--ink)}
.dob label[hidden]{display:none}
.dob label small{font-weight:400;color:var(--muted);margin-left:6px}
.dob input{display:block;width:100%;margin-top:6px;min-height:52px;border:2px solid var(--line);border-radius:var(--radius-sm);padding:0 14px;font:400 17px var(--sans);color:var(--ink);background:#fff}
.dob input:focus{outline:none;border-color:var(--crimson);box-shadow:0 0 0 4px rgba(208,63,88,.18)}
.dob .btn{width:100%;margin-top:4px;font-size:18px}
.dob .err{min-height:20px;margin-top:6px;font-size:14px;font-weight:700;color:var(--crimson-600)}
.dob{border-bottom:0;margin:0;padding:0}
.dob fieldset{border:0;margin:0;padding:0;min-width:0}
.dob legend{font-size:14px;font-weight:700;color:var(--ink);padding:0}
.sel3{display:grid;grid-template-columns:1.3fr 1fr 1fr;gap:8px;margin-top:6px}
.dob select{width:100%;min-height:52px;border:2px solid var(--line);border-radius:var(--radius-sm);padding:0 34px 0 14px;font:400 17px var(--sans);color:var(--ink);background:#fff url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='8' viewBox='0 0 12 8'%3E%3Cpath d='M1 1l5 5 5-5' fill='none' stroke='%23B83349' stroke-width='2'/%3E%3C/svg%3E") no-repeat right 12px center;-webkit-appearance:none;appearance:none}
.dob select:focus{outline:none;border-color:var(--crimson);box-shadow:0 0 0 4px rgba(208,63,88,.18)}
.dob input::placeholder{color:#9A8A8C}
.dob select{margin-top:6px}
.yhint{font-size:13px!important;line-height:1.6;color:var(--muted);margin:-2px 0 0}
.dob .btn:disabled{background:#D9C9CB;box-shadow:none;cursor:not-allowed;color:#fff}
html.pdfmode body>*:not(#pdfmode){display:none!important}#pdfmode{position:fixed;inset:0;z-index:9999;display:grid;place-items:center;background:#FBF4E8;padding:20px}#pdfmode .pm-card{max-width:420px;width:100%;background:#fff;border-radius:22px;padding:30px 24px;text-align:center;box-shadow:0 18px 40px rgba(59,15,24,.12)}#pdfmode .pm-k{color:#B8324A;font-weight:700;font-size:13px;letter-spacing:2px;margin:0 0 8px}#pdfmode h1{font-size:28px;margin:0 0 12px;color:#3B0F18}#pdfmode p{color:#5E4A4C;line-height:1.7}#pdfmode .pm-btn{margin:16px 0 6px;width:100%;min-height:54px;background:#D03F58!important;color:#fff!important;border:0!important;font-size:18px}#pdfmode .pm-s{font-size:13px;color:#9a8487;margin:14px 0 0}
.pdfwrap{margin:28px 0 8px;text-align:center}.pdfwrap p{margin:10px 0 0;font-size:14px;color:#7A5A60}.pdfwrap .pdfbtn{width:100%;max-width:420px;margin:0;background:#fff;border:2px solid #B8324A!important;color:#B8324A}.pdfbtn:disabled{opacity:.7;cursor:wait}
.pdfbtn{border:0;cursor:pointer;font-family:inherit;display:inline-flex;align-items:center;justify-content:center;min-height:48px;margin-top:12px;padding:0 22px;border-radius:999px;background:#EFDFB3;color:#3B0F18;font-weight:900;font-size:16px;text-decoration:none}
.fine2{font-size:12px!important;color:var(--muted);text-align:center;margin-top:8px}
#dobres{display:none}
.zr:checked~#dobres.on{display:block}
#dobres .box{margin:16px var(--pad) 0;max-width:1180px;background:var(--crimson-900);color:#FFFAEB;border-radius:var(--radius-md);padding:16px 20px;font-size:16px;line-height:1.7}
@media(min-width:900px){#dobres .box{margin:20px auto 0}}
#dobres b{color:var(--beige)}
#dobres small{display:block;font-size:13px;color:rgba(255,250,235,.75);margin-top:4px}
'''

YEARS = ''.join(f'<option value="{y}">{y}</option>' for y in range(2027, 1929, -1))
DOB = f'''<form class="dob" id="dobform" novalidate>
      <b>输入你的资料，马上看</b>
      <p>用你的出生年份找出你的生肖，直接打开你的 2027 求财指南。</p>
      <div class="dob-row">
        <label for="dob-name">称呼<input id="dob-name" name="name" autocomplete="given-name" placeholder="例如：Amy"></label>
        <label for="dob-email">Email<input id="dob-email" name="email" type="email" inputmode="email" autocomplete="email" placeholder="you@email.com"></label>
        <label for="dob-phone">WhatsApp 号码<input id="dob-phone" name="phone" type="tel" inputmode="numeric" autocomplete="tel-national" placeholder="例如 0123456789"></label>
        <label for="dob-y">出生年份
          <select id="dob-y" autocomplete="bday-year"><option value="" disabled selected hidden>选你的出生年份</option>{YEARS}</select>
        </label>
        <button type="submit" class="btn" id="dob-go" disabled>看我的 2027 财运 →</button>
      </div>
      <p class="err" id="dob-err" role="alert"></p>
      <p class="fine2">免费 · 资料只用来发送你的指南和大会资讯。</p>
    </form>
    '''

a = '<div class="picker-h"><b>你属什么？</b><small>01 / 选择你的生肖</small></div>'
assert h.count(a) == 1
h = h.replace(a, '<div class="picker-h"><b>你属什么？</b><small>免费 · 30 秒</small></div>\n    ' + DOB, 1)
import re as _re
h, n = _re.subn(r'<div class="zgrid">[\s\S]*?</label></div>\s*', '', h, count=1); assert n == 1
h = h.replace('<p class="hint">点你的生肖，马上看你的 2027 求财指南 · 免费阅读</p>', '', 1)
a = '<div id="read">'
assert h.count(a) == 1
h = h.replace(a, '<div id="dobres" aria-live="polite"><div class="box" id="dobres-t"></div></div>\n' + a, 1)
h = h.replace('</style>', CSS + '</style>', 1)
# 立即报名 → 直接开 WhatsApp 给 Suyen（017-637 4934），讯息写好「我要出席奇门战略大会」；不再开报名弹窗
WA_SUYEN = '60176374934'
from urllib.parse import quote as _q
_wa = f'https://wa.me/{WA_SUYEN}?text=' + _q('我要出席奇门战略大会')
_n = h.count('href="#signup" data-modal-open="lead"'); assert _n >= 2, _n
CONF_PAGE = 'https://2027shengxiaocaifu.suyenlim.com/suyen2027-caiyun-vip'   # 2026-11-19：立即报名 → 大会页（复制自 suyen2027，按钮直接去 VIP OTO）
h = h.replace('href="#signup" data-modal-open="lead"', f'href="{CONF_PAGE}" data-cta="whatsapp-attend"')
# 03 出生年份：年份已经从表单知道，不用再按 → 藏起年份按钮、问题和立春说明，直接显示他的那张求财卡
h = h.replace('</style>', '.ypanel>b,.ychips,.ypanel>p.note{display:none}.yres{margin-top:0;border-top:0;padding-top:0}.yd0,.yd1,.yd2,.yd3,.yd4,.yd5,.yd6,.yd7,.yd8,.yd9,.yd10,.yd11{display:none}</style>', 1)
_n = h.count('点你的出生年份，看属于你的那条路。'); assert _n == 12, _n
h = h.replace('点你的出生年份，看属于你的那条路。', '下面是你出生那一年的求财路线。')
assert h.count('<span class="g">先选择</span>') == 1
h = h.replace('<span class="g">先选择</span>', '<span class="g">先看清</span>', 1)

# raw 页没有平台钩子：见证影片直接嵌（顺序跟 funnel 页的影片格一样）
VIDS = ['beb2a5be-9104-4064-912d-65ce38fc355a', '1aff4376-3c5e-42fe-a2b3-d66341cc43f7', '0ec31e4a-7077-4ffb-b23c-6492695dec85',
        '27c8ae58-4ed2-4fa2-b3b9-e846d8bdc147', 'c9807791-112a-4df3-a8af-e34d28511494', '154545e8-b207-4653-86e6-8d09d86459f8']
ph = '<div data-aigoal-video style="position:absolute;inset:0"></div>'
assert h.count(ph) == len(VIDS), h.count(ph)
for v in VIDS:
    h = h.replace(ph, f'<iframe src="https://iframe.mediadelivery.net/embed/790175/{v}?autoplay=false&muted=false&loop=false&preload=false&responsive=true" loading="lazy" title="学员见证影片" style="position:absolute;inset:0;width:100%;height:100%;border:0" allow="accelerometer;gyroscope;autoplay;encrypted-media;picture-in-picture;fullscreen" allowfullscreen></iframe>', 1)

# aigoal 通用下拉（ag-sel）：raw 页没有平台钩子，照搬平台的 agSelect + 它的样式，再加品牌外观
import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
AG_JS = open(_os.path.join(_HERE, 'agselect.js'), encoding='utf8').read().replace('%', '%%')
AG_CSS = open(_os.path.join(_HERE, 'agselect.css'), encoding='utf8').read() + '''
.dob .ag-sel{margin-top:6px}
.dob .ag-sel-btn{min-height:52px;padding:0 14px;border:2px solid var(--line);border-radius:var(--radius-sm);background:#fff;color:var(--ink);font:400 17px var(--sans)}
.dob .ag-sel-btn:focus{outline:none;border-color:var(--crimson);box-shadow:0 0 0 4px rgba(208,63,88,.18)}
.dob .ag-sel-ph .ag-sel-label{color:#9A8A8C;opacity:1}
.dob .ag-sel-arrow{color:var(--crimson-600);opacity:1}
.dob .ag-sel-list{border-radius:var(--radius-sm);border:1px solid var(--line);box-shadow:var(--shadow-2);color:var(--ink)}
.dob .ag-sel-opt{font-size:16px}
.dob .ag-sel-opt:hover,.dob .ag-sel-opt.ag-act{background:var(--pill-bg)}
.dob .ag-sel-opt[aria-selected="true"]{background:var(--crimson);color:#fff}
'''
h = h.replace('</style>', AG_CSS + '</style>', 1)

JS = '''<script>
/* aigoal 通用下拉 agSelect（照搬平台） */
(function(){var $=function(q){return [].slice.call(document.querySelectorAll(q));};
'''+AG_JS+'''
$('.dob select').forEach(agSelect);})();
/* raw 版：没有平台钩子，这里自己做 ① 出生日期 → 年柱地支 ② 报名弹窗 ③ 报名送出（跟平台一样送去 /api/track，算在 funnel 那一页） */
(function(){
var PDFZ=%(pdfz)s; var PDF=%(pdf)s, OWN_SLUG=%(own)s, FUNNEL_SLUG=%(slug)s, NEXT=%(next)s, LICHUN=%(lc)s;
var STEMS='甲乙丙丁戊己庚辛壬癸', BRANCH='子丑寅卯辰巳午未申酉戌亥', ZOD='鼠牛虎兔龙蛇马羊猴鸡狗猪';
function $(id){return document.getElementById(id);}
/* ① 出生日期 → 年柱（立春为界，马来西亚时间） */
function pillarYear(dateStr){
  var y=+dateStr.slice(0,4), lc=LICHUN[y]; if(!lc) return {y:y};
  var lcDay=lc.slice(0,10);
  if(dateStr<lcDay) return {y:y-1};
  return {y:y, onLichun:dateStr===lcDay};
}
function pad(n){return (n<10?'0':'')+n;}
function vals(){return {nm:$('dob-name').value.trim(), em:$('dob-email').value.trim(), ph:$('dob-phone').value.replace(/[\\s-]/g,''), Y:+$('dob-y').value};}
function ready(){var v=vals();return !!(v.nm&&v.em&&v.ph&&v.Y);}
function sync(){$('dob-go').disabled=!ready();}
['dob-name','dob-email','dob-phone','dob-y'].forEach(function(id){$(id).addEventListener('input',sync);$(id).addEventListener('change',sync);});
function go(ev){
  if(ev)ev.preventDefault();
  var err=$('dob-err'), v=vals();
  if(!ready()){err.textContent='请填好称呼、Email、WhatsApp 号码和出生年份。';return;}
  if(!/^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(v.em)){err.textContent='请填写正确的 Email。';$('dob-email').focus();return;}
  if(!/^\\+?[0-9]{9,15}$/.test(v.ph)){err.textContent='请填写可以收到 WhatsApp 的号码，至少 9 位数字。';$('dob-phone').focus();return;}
  err.textContent='';
  var y=v.Y, zi=((y-4)%%12+12)%%12, si=((y-4)%%10+10)%%10, pill=STEMS[si]+BRANCH[zi];
  var z=$('z'+zi); if(!z) return; z.checked=true;
  var yr=$('y'+zi+'_'+y); if(yr) yr.checked=true;
  $('dobres-t').innerHTML='你是 <b>'+y+' 年</b>出生，生肖 <b>属'+ZOD[zi]+'</b>（'+pill+'年）。'
    +'<small>下面已经帮你打开属'+ZOD[zi]+'的 2027 求财指南。</small>'
;
  $('dobres').className='on';
  setTimeout(function(){prewarm(zi);},1200);
  var eid='dob.'+Date.now().toString(36)+'.'+Math.random().toString(36).slice(2,8);
  try{post({event:'register',source:'landing:'+FUNNEL_SLUG,name:v.nm,email:v.em,phone:v.ph,event_id:eid,tags:['registered','lead_magnet_2027_十二生肖'],
    fields:[{k:'birth_year',l:'出生年份',v:String(y)},{k:'dob_pillar',l:'生肖',v:'属'+ZOD[zi]+'（'+pill+'年）'}],
    note:'出生年份: '+y+'\\n生肖: 属'+ZOD[zi]+'（'+pill+'年）'}).then(function(r){return r&&r.json?r.json():null;}).then(function(j){if(j&&j.ft)setFt(j.ft);}).catch(function(){});}catch(e){}
  try{if(window.fbq)fbq('track','Lead',{content_name:'zodiac_'+ZOD[zi]},{eventID:eid});}catch(e){}
  if($('name')&&!$('name').value)$('name').value=v.nm; if($('email')&&!$('email').value)$('email').value=v.em; if($('wa')&&!$('wa').value)$('wa').value=v.ph;
  try{if(window.fbq)fbq('track','ViewContent',{content_name:'zodiac_'+ZOD[zi]});}catch(e){}
  window.scrollTo({top:0,behavior:'smooth'});
}
/* 大会 funnel 的报名码 ft：带去大会页 → 大会页按钮再带去 VIP OTO（付款才认得是谁） */
function setFt(ft){try{sessionStorage.setItem('ag_ft',ft);}catch(e){}
  document.querySelectorAll('a[data-cta="whatsapp-attend"]').forEach(function(a){var u=a.getAttribute('href').split('?')[0];a.setAttribute('href',u+'?ft='+encodeURIComponent(ft));});}
try{var _ft=new URLSearchParams(location.search).get('ft')||sessionStorage.getItem('ag_ft');if(_ft)setFt(_ft);}catch(e){}
$('dobform').addEventListener('submit',go);
/* 下载 PDF：把这位访客自己那一份指南（.rdN）在浏览器里转成 PDF，不用另外放档案 */
/* aigoal 页面只准跑页面里的 script（CSP），所以 html2canvas 放在页底 type=text/plain 不执行，按下载才装进来 */
function loadH2C(){if(window.html2canvas)return Promise.resolve();var src=document.getElementById('h2c-src');if(!src)return Promise.reject(new Error('no h2c'));
  var s=document.createElement('script');s.textContent=src.textContent;document.head.appendChild(s);return window.html2canvas?Promise.resolve():Promise.reject(new Error('h2c load'));}
/* 一页长 PDF：一张 JPEG + 可以点的链接（报名 WhatsApp） */
function b64bytes(d){var bin=atob(d.split(',')[1]),u=new Uint8Array(bin.length);for(var i=0;i<bin.length;i++)u[i]=bin.charCodeAt(i);return u;}
function makePdf(jpg,iw,ih,W,H,links,body,im2,pg2){
  var parts=[],len=0,offs=[];function add(x){if(typeof x==='string'){var u=new Uint8Array(x.length);for(var i=0;i<x.length;i++)u[i]=x.charCodeAt(i)&255;x=u;}parts.push(x);len+=x.length;}
  function obj(n,body,stream){offs[n]=len;add(n+' 0 obj\\n'+body);if(stream){add('\\nstream\\n');add(stream);add('\\nendstream');}add('\\nendobj\\n');}
  var A0=im2?7:6,nA=links.length,an=[];for(var k=0;k<nA;k++)an.push((A0+k)+' 0 R');
  var P2=A0+nA; /* page 2 objects: P2 page, P2+1 content, P2+2 image */
  add('%%PDF-1.4\\n');
  obj(1,'<< /Type /Catalog /Pages 2 0 R >>');
  obj(2,'<< /Type /Pages /Kids [3 0 R'+(pg2?' '+P2+' 0 R':'')+'] /Count '+(pg2?2:1)+' >>');
  obj(3,'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 '+W+' '+H+'] /Resources << /XObject << /Im0 5 0 R'+(im2?' /Im1 6 0 R':'')+' >> >> /Contents 4 0 R'+(nA?' /Annots ['+an.join(' ')+']':'')+' >>');
  var cs=body||('q '+W+' 0 0 '+H+' 0 0 cm /Im0 Do Q');obj(4,'<< /Length '+cs.length+' >>',cs);
  obj(5,'<< /Type /XObject /Subtype /Image /Width '+iw+' /Height '+ih+' /ColorSpace /DeviceRGB /BitsPerComponent 8 /Filter /DCTDecode /Length '+jpg.length+' >>',jpg);
  if(im2)obj(6,'<< /Type /XObject /Subtype /Image /Width '+im2.iw+' /Height '+im2.ih+' /ColorSpace /DeviceRGB /BitsPerComponent 8 /Filter /DCTDecode /Length '+im2.jpg.length+' >>',im2.jpg);
  links.forEach(function(l,k){obj(A0+k,'<< /Type /Annot /Subtype /Link /Border [0 0 0] /Rect ['+l.r.join(' ')+'] /A << /S /URI /URI ('+l.u.replace(/[()\\\\]/g,'\\\\$&')+') >> >>');});
  var n=P2;
  if(pg2){var c2='q '+pg2.W+' 0 0 '+pg2.H+' 0 0 cm /Im2 Do Q';
    obj(P2,'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 '+pg2.W+' '+pg2.H+'] /Resources << /XObject << /Im2 '+(P2+2)+' 0 R >> >> /Contents '+(P2+1)+' 0 R >>');
    obj(P2+1,'<< /Length '+c2.length+' >>',c2);
    obj(P2+2,'<< /Type /XObject /Subtype /Image /Width '+pg2.iw+' /Height '+pg2.ih+' /ColorSpace /DeviceRGB /BitsPerComponent 8 /Filter /DCTDecode /Length '+pg2.jpg.length+' >>',pg2.jpg);n=P2+3;}
  var x=len,xr='xref\\n0 '+n+'\\n0000000000 65535 f \\n';for(var i=1;i<n;i++)xr+=('000000000'+offs[i]).slice(-10)+' 00000 n \\n';
  add(xr+'trailer\\n<< /Size '+n+' /Root 1 0 R >>\\nstartxref\\n'+x+'\\n%%%%EOF');
  return new Blob(parts,{type:'application/pdf'});}
/* 指南是靠页面上的 radio 显示的，复制出去规则就失效 → 把每一格当下的显示状态写死在复制品上 */
function snap(rd){var c=rd.cloneNode(true),a=[rd].concat([].slice.call(rd.querySelectorAll('*'))),b=[c].concat([].slice.call(c.querySelectorAll('*')));
  a.forEach(function(el,i){var cs=getComputedStyle(el),t=b[i],bg=cs.backgroundImage,cn=typeof el.className==='string'?el.className:'';if(i===0||/(^|\\s)y[cd]\\d/.test(cn))t.style.display=cs.display;if(bg!=='none'&&/none/.test(bg))t.style.backgroundImage=bg.replace(/,\\s*none/g,'');
    if(el.tagName==='SMALL'&&el.parentNode.tagName==='LABEL')t.style.color=cs.color;
    if(el.tagName==='LABEL'){t.style.background=cs.backgroundImage!=='none'?cs.backgroundImage:cs.backgroundColor;t.style.color=cs.color;t.style.borderColor=cs.borderColor;}
    if(el.tagName==='INPUT'&&el.checked)t.setAttribute('checked','');
    if(el.tagName==='IMG')t.removeAttribute('loading');});
  c.style.width='100%%';c.style.maxWidth='none';c.style.margin='0';c.style.background='#FBF4E8';return c;}
function waitImgs(rd,ms){var ps=[].slice.call(rd.querySelectorAll('img')).map(function(i){i.loading='eager';return i.complete&&i.naturalWidth?null:new Promise(function(ok){i.addEventListener('load',ok,{once:true});i.addEventListener('error',ok,{once:true});});});
  return Promise.race([Promise.all(ps),new Promise(function(ok){setTimeout(ok,ms);})]);}
function prewarm(zi){var g=PDFZ[zi];try{if(g)fetch(g.u);if(PDFZ.conf)fetch(PDFZ.conf.u);if(PDFZ.sponsor)fetch(PDFZ.sponsor.u);}catch(e){}}
/* 下载按钮放在每一份指南最后（大会卡下面） */
document.querySelectorAll('.rd').forEach(function(rd){var m=/\\brd(\\d+)\\b/.exec(rd.className);if(!m)return;var zi=+m[1],cf=rd.querySelectorAll('.conf');cf=cf[cf.length-1];if(!cf)return;
  cf.insertAdjacentHTML('afterend','<div class="pdfwrap"><button type="button" class="pdfbtn" data-zi="'+zi+'">下载属'+ZOD[zi]+'的 2027 求财指南 PDF ↓</button><p>存进手机，做决定前拿出来看一眼。</p></div>');});
function pdfYear(zi){var ys=document.querySelector('input[id^="y'+zi+'_"]:checked');return ys?ys.id.split('_')[1]:'';}
function savePdf(btn){
  var zi=+btn.getAttribute('data-zi'),g=PDFZ[zi]; if(!g){alert('PDF 暂时打不开，可以直接截图保存。');return;}
  var yr=pdfYear(zi),card=g.cards[yr]||g.cards[Object.keys(g.cards)[0]];
  var t=btn.textContent; btn.disabled=true; btn.textContent='正在下载 PDF…';
  try{if(window.fbq)fbq('track','ViewContent',{content_name:'pdf_'+ZOD[zi]});}catch(e){}
  try{post({event:'cta',cta:'pdf-download',source:'landing:'+OWN_SLUG});}catch(e){}
  var C=PDFZ.conf;function get(u){return fetch(u).then(function(r){if(!r.ok)throw new Error('img '+r.status);return r.arrayBuffer();});}
  var SP=PDFZ.sponsor;Promise.all([get(g.u),C?get(C.u):null,SP?get(SP.u):null]).then(function(bs){var buf=bs[0];
    var k=0.75,sl=[[0,g.top],card,[g.bottom,g.H]],W=g.W*k,Hi=g.H*k,Ht=0,yd=0,body='';
    sl.forEach(function(x){Ht+=(x[1]-x[0])*k;});var Hc=C?C.H*k:0,Hp=Ht+Hc,links=[];
    sl.forEach(function(x){var hs=(x[1]-x[0])*k,yb=Hp-(yd+hs),ty=yb-Hi+x[1]*k;
      body+='q 0 '+yb.toFixed(2)+' '+W.toFixed(2)+' '+hs.toFixed(2)+' re W n '+W.toFixed(2)+' 0 0 '+Hi.toFixed(2)+' 0 '+ty.toFixed(2)+' cm /Im0 Do Q ';yd+=hs;});
    if(C){body+='q '+(C.W*k).toFixed(2)+' 0 0 '+Hc.toFixed(2)+' 0 0 cm /Im1 Do Q';var b=C.btn;links.push({u:C.href,r:[b[0]*k,Hc-(b[1]+b[3])*k,(b[0]+b[2])*k,Hc-b[1]*k].map(function(v){return v.toFixed(1);})});if(C.qr){var q=C.qr;links.push({u:C.href,r:[q[0]*k,Hc-(q[1]+q[3])*k,(q[0]+q[2])*k,Hc-q[1]*k].map(function(v){return v.toFixed(1);})});}}
    var blob=makePdf(new Uint8Array(buf),g.w,g.h,W.toFixed(2),Hp.toFixed(2),links,body,C?{jpg:new Uint8Array(bs[1]),iw:C.w,ih:C.h}:null,SP?{jpg:new Uint8Array(bs[2]),iw:SP.w,ih:SP.h,W:W.toFixed(2),H:(W*SP.h/SP.w).toFixed(2)}:null);
    var u=URL.createObjectURL(blob),a=document.createElement('a');a.href=u;a.download='2027生肖求财指南-属'+ZOD[zi]+'-林舒苑.pdf';document.body.appendChild(a);a.click();
    setTimeout(function(){URL.revokeObjectURL(u);a.remove();},4000);
  }).then(function(){btn.disabled=false;btn.textContent=t;if(document.documentElement.classList.contains('pdfmode')&&history.length>1){var bk=document.getElementById('pm-back');if(bk)bk.style.display='block';setTimeout(function(){history.back();},1800);}},function(er){try{console.log('PDFERR',er&&(er.stack||er.message||er))}catch(_){}btn.disabled=false;btn.textContent=t;alert('PDF 没下载成功，请稍后再试一次。');});
}
document.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('.pdfbtn[data-zi]');if(b){e.preventDefault();savePdf(b);}});
/* ?pdf=年份：漏斗第 2 页的「下载 PDF」连过来 → 只显示下载画面（他们已在漏斗报名） */
(function(){var y=0;try{y=+(new URLSearchParams(location.search).get('pdf')||0);}catch(e){}if(!y)return;
  var zi=((y-4)%%12+12)%%12,yr=document.getElementById('y'+zi+'_'+y);if(yr)yr.checked=true;
  var z=document.getElementById('z'+zi);if(z)z.checked=true;
  var ov=document.createElement('div');ov.id='pdfmode';
  ov.innerHTML='<div class="pm-card"><p class="pm-k">2027 · 你的生肖求财指南</p><h1>属'+ZOD[zi]+' · '+y+' 年出生</h1><p>你的《2027 生肖财运指南》PDF 正在下载…<br>如果没有自动开始，请按下面的按钮。</p><button type="button" class="pdfbtn pm-btn" data-zi="'+zi+'">下载 PDF ↓</button><p id="pm-back" style="display:none;color:#2E7D4F;font-weight:700">下载好了 ✓ 正在回到你的指南…</p><p class="pm-s">林舒苑 · 2027 奇门遁甲战略导师</p></div>';
  document.body.appendChild(ov);document.documentElement.classList.add('pdfmode');try{prewarm(zi);}catch(e){}
  setTimeout(function(){var b=ov.querySelector('.pdfbtn');if(b)savePdf(b);},400);
})();


/* 立即报名 → WhatsApp：记一下点击（Meta Contact 事件 + aigoal 统计） */
document.querySelectorAll('a[data-cta="whatsapp-attend"]').forEach(function(a){a.addEventListener('click',function(){try{if(window.fbq)fbq('track','Contact');}catch(e){}try{post({event:'cta',cta:'conference-page'});}catch(e){}});});
/* ② 报名弹窗 */
var modal=document.querySelector('[data-aigoal-modal="lead"]'), lastBtn=null;
function openM(e){if(e)e.preventDefault();lastBtn=e&&e.currentTarget;modal.classList.add('ag-open');document.body.style.overflow='hidden';var f=modal.querySelector('input:not([type=hidden])');if(f)setTimeout(function(){f.focus();},50);}
function closeM(){modal.classList.remove('ag-open');document.body.style.overflow='';if(lastBtn)lastBtn.focus();}
document.querySelectorAll('[data-modal-open="lead"]').forEach(function(b){b.addEventListener('click',openM);});
modal.querySelectorAll('[data-modal-close]').forEach(function(b){b.addEventListener('click',function(e){e.preventDefault();closeM();});});
modal.addEventListener('click',function(e){if(e.target===modal)closeM();});
document.addEventListener('keydown',function(e){if(e.key==='Escape'&&modal.classList.contains('ag-open'))closeM();});

/* ③ 报名送出：跟平台钩子同一个格式，source 算在 funnel 那一页（自动化照常） */
function utm(){var o={};try{var q=new URLSearchParams(location.search);['utm_source','utm_medium','utm_campaign','utm_content','utm_term'].forEach(function(k){var v=q.get(k);if(v)o[k]=v;});}catch(e){}return o;}
var FT='';try{FT=new URLSearchParams(location.search).get('ft')||'';}catch(e){}
function post(body){var payload=Object.assign({source:'landing:'+FUNNEL_SLUG},utm(),body);var blob=JSON.stringify(payload);
  if(body.event==='landing'&&navigator.sendBeacon){navigator.sendBeacon('/api/track',new Blob([blob],{type:'application/json'}));return Promise.resolve();}
  return fetch('/api/track',{method:'POST',headers:{'content-type':'application/json'},body:blob});}
try{post({event:'landing',source:'landing:'+OWN_SLUG,ref:document.referrer||'',bot:navigator.webdriver?1:0});}catch(e){}
document.querySelectorAll('form[data-aigoal-lead]').forEach(function(f){f.addEventListener('submit',function(ev){ev.preventDefault();
  var d={},fields=[];f.querySelectorAll('input,select,textarea').forEach(function(el){var t=(el.type||'').toLowerCase();if(t==='submit'||t==='button'||t==='hidden'||t==='reset')return;if((t==='radio'||t==='checkbox')&&!el.checked)return;var v=(el.value||'').trim();if(!v)return;var nm=el.name||'';if(nm==='name'||nm==='phone'||nm==='email'){d[nm]=v;return;}var label=(el.getAttribute('data-label')||el.getAttribute('aria-label')||nm||'').trim();if(!label)return;fields.push({k:nm||label,l:label,v:v});});
  var dz=$('dobres').className==='on'?$('dobres-t').textContent.split('。')[0]:'';if(dz)fields.push({k:'dob_pillar',l:'出生年柱',v:dz});if($('dob-y').value)fields.push({k:'birth_year',l:'出生年份',v:$('dob-y').value});
  if(!d.phone&&!d.email){alert('请留电话或 email，不然联系不到你哦');return;}
  if(fields.length){d.fields=fields;d.note=fields.map(function(x){return x.l+': '+x.v;}).join('\\n');}
  d.event='register';var eid='ld.'+Date.now().toString(36)+'.'+Math.random().toString(36).slice(2,8);d.event_id=eid;
  try{if(window.fbq)fbq('track','CompleteRegistration',{},{eventID:eid});}catch(e){}
  var btn=f.querySelector('[type="submit"]');if(btn){btn.disabled=true;btn.setAttribute('data-t',btn.textContent);btn.textContent='发送中…';}
  function done(ft){var u=NEXT;ft=ft||FT;if(ft)u+=(u.indexOf('?')<0?'?':'&')+'ft='+encodeURIComponent(ft);location.href=u;}
  post(d).then(function(r){if(!r||!r.ok)throw new Error('http');return r.json().then(function(j){done(j&&j.ft);}).catch(function(){done();});})
    .catch(function(){if(btn){btn.disabled=false;btn.textContent=btn.getAttribute('data-t');}alert('没发出去，再试一次或直接 WhatsApp 我们');});
});});
})();
</script>'''
JS = JS % {'pdfz': json.dumps(PDFZ), 'pdf': json.dumps(PDF_URLS), 'own': json.dumps(OWN_SLUG), 'slug': json.dumps(FUNNEL_SLUG), 'next': json.dumps(NEXT), 'lc': json.dumps({y: v for y, v in lc.items()})}
assert h.count('</body>') == 1
h = h.replace('</body>', JS + '\n</body>', 1)
_H2C = open(_os.path.join(_HERE, 'html2canvas.min.js'), encoding='utf8').read()
assert '</script' not in _H2C
# html2canvas no longer embedded: PDFs are pre-rendered images
import re as _re
def _vid(m):
    vid = m.group(1); b = 'https://vz-1500311e-90c.b-cdn.net/' + vid
    return ('<video controls playsinline preload="none" poster="%s/thumbnail.jpg" title="学员见证影片" '
            'style="position:absolute;inset:0;width:100%%;height:100%%;border:0;background:#000;object-fit:cover">'
            '<source src="%s/playlist.m3u8" type="application/vnd.apple.mpegurl"><source src="%s/original" type="video/mp4"></video>') % (b, b, b)
h, _nv = _re.subn(r'<iframe src="https://iframe\.mediadelivery\.net/embed/790175/([0-9a-f-]+)[^"]*"[^>]*>\s*</iframe>', _vid, h)
print('videos ->', _nv)
open(out, 'w', encoding='utf8').write(h)
print('raw page', len(h))
