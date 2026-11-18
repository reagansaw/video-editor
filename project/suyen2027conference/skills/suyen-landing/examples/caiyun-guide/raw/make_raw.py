"""把 asis 版落地页（optin.html）变成 raw 版：加「输入出生日期 → 年柱地支」、自己处理报名弹窗和报名送出（raw 页没有平台钩子）。
用法：python3 make_raw.py <optin.html> <lichun.json> <out.html> <funnel 页 slug> <报名成功网址>"""
import json, sys

src, lcf, out, FUNNEL_SLUG, NEXT, OWN_SLUG = sys.argv[1:7]
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
var OWN_SLUG=%(own)s, FUNNEL_SLUG=%(slug)s, NEXT=%(next)s, LICHUN=%(lc)s;
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
    +'<small>下面已经帮你打开属'+ZOD[zi]+'的 2027 求财指南。如果你是 1 月到 2 月初（立春前）出生，生肖算前一年，可以回上面改选。</small>';
  $('dobres').className='on';
  var eid='dob.'+Date.now().toString(36)+'.'+Math.random().toString(36).slice(2,8);
  try{post({event:'register',source:'landing:'+OWN_SLUG,name:v.nm,email:v.em,phone:v.ph,event_id:eid,
    fields:[{k:'birth_year',l:'出生年份',v:String(y)},{k:'dob_pillar',l:'生肖',v:'属'+ZOD[zi]+'（'+pill+'年）'}],
    note:'出生年份: '+y+'\\n生肖: 属'+ZOD[zi]+'（'+pill+'年）'});}catch(e){}
  try{if(window.fbq)fbq('track','Lead',{content_name:'zodiac_'+ZOD[zi]},{eventID:eid});}catch(e){}
  if($('name')&&!$('name').value)$('name').value=v.nm; if($('email')&&!$('email').value)$('email').value=v.em; if($('wa')&&!$('wa').value)$('wa').value=v.ph;
  try{if(window.fbq)fbq('track','ViewContent',{content_name:'zodiac_'+ZOD[zi]});}catch(e){}
  window.scrollTo({top:0,behavior:'smooth'});
}
$('dobform').addEventListener('submit',go);

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
JS = JS % {'own': json.dumps(OWN_SLUG), 'slug': json.dumps(FUNNEL_SLUG), 'next': json.dumps(NEXT), 'lc': json.dumps({y: v for y, v in lc.items()})}
assert h.count('</body>') == 1
h = h.replace('</body>', JS + '\n</body>', 1)
open(out, 'w', encoding='utf8').write(h)
print('raw page', len(h))
