"""把 asis 版落地页（optin.html）变成 raw 版：加「输入出生日期 → 年柱地支」、自己处理报名弹窗和报名送出（raw 页没有平台钩子）。
用法：python3 make_raw.py <optin.html> <lichun.json> <out.html> <funnel 页 slug> <报名成功网址>"""
import json, sys

src, lcf, out, FUNNEL_SLUG, NEXT = sys.argv[1:6]
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
.or{font-size:14px;font-weight:700;color:var(--muted);margin:0 0 10px}
#dobres{display:none}
.zr:checked~#dobres.on{display:block}
#dobres .box{margin:16px var(--pad) 0;max-width:1180px;background:var(--crimson-900);color:#FFFAEB;border-radius:var(--radius-md);padding:16px 20px;font-size:16px;line-height:1.7}
@media(min-width:900px){#dobres .box{margin:20px auto 0}}
#dobres b{color:var(--beige)}
#dobres small{display:block;font-size:13px;color:rgba(255,250,235,.75);margin-top:4px}
'''

DOB = '''<div class="dob">
      <b>输入你的出生日期</b>
      <p>帮你找出你的年柱和生肖（以立春为界，不是 1 月 1 日），直接打开你的 2027 求财指南。</p>
      <div class="dob-row">
        <label for="dob-date">出生日期<input id="dob-date" type="date" min="1930-01-01" max="2027-12-31" autocomplete="bday"></label>
        <button type="button" class="btn" id="dob-go">看我的 2027 财运 →</button>
      </div>
      <p class="err" id="dob-err" role="alert"></p>
    </div>
    <p class="or">或直接点你的生肖：</p>
    '''

a = '<div class="picker-h"><b>你属什么？</b><small>01 / 选择你的生肖</small></div>'
assert h.count(a) == 1
h = h.replace(a, '<div class="picker-h"><b>你属什么？</b><small>免费 · 30 秒</small></div>\n    ' + DOB, 1)
a = '<div id="read">'
assert h.count(a) == 1
h = h.replace(a, '<div id="dobres" aria-live="polite"><div class="box" id="dobres-t"></div></div>\n' + a, 1)
h = h.replace('</style>', CSS + '</style>', 1)

# raw 页没有平台钩子：见证影片直接嵌（顺序跟 funnel 页的影片格一样）
VIDS = ['beb2a5be-9104-4064-912d-65ce38fc355a', '1aff4376-3c5e-42fe-a2b3-d66341cc43f7', '0ec31e4a-7077-4ffb-b23c-6492695dec85',
        '27c8ae58-4ed2-4fa2-b3b9-e846d8bdc147', 'c9807791-112a-4df3-a8af-e34d28511494', '154545e8-b207-4653-86e6-8d09d86459f8']
ph = '<div data-aigoal-video style="position:absolute;inset:0"></div>'
assert h.count(ph) == len(VIDS), h.count(ph)
for v in VIDS:
    h = h.replace(ph, f'<iframe src="https://iframe.mediadelivery.net/embed/790175/{v}?autoplay=false&muted=false&loop=false&preload=false&responsive=true" loading="lazy" title="学员见证影片" style="position:absolute;inset:0;width:100%;height:100%;border:0" allow="accelerometer;gyroscope;autoplay;encrypted-media;picture-in-picture;fullscreen" allowfullscreen></iframe>', 1)

JS = '''<script>
/* raw 版：没有平台钩子，这里自己做 ① 出生日期 → 年柱地支 ② 报名弹窗 ③ 报名送出（跟平台一样送去 /api/track，算在 funnel 那一页） */
(function(){
var FUNNEL_SLUG=%(slug)s, NEXT=%(next)s, LICHUN=%(lc)s;
var STEMS='甲乙丙丁戊己庚辛壬癸', BRANCH='子丑寅卯辰巳午未申酉戌亥', ZOD='鼠牛虎兔龙蛇马羊猴鸡狗猪';
function $(id){return document.getElementById(id);}
/* ① 出生日期 → 年柱（立春为界，马来西亚时间） */
function pillarYear(dateStr){
  var y=+dateStr.slice(0,4), lc=LICHUN[y]; if(!lc) return {y:y};
  var lcDay=lc.slice(0,10);
  if(dateStr<lcDay) return {y:y-1};
  return {y:y, onLichun:dateStr===lcDay};
}
function go(){
  var d=$('dob-date').value, err=$('dob-err');
  if(!d){err.textContent='先选一下你的出生日期～';return;}
  var yy=+d.slice(0,4); if(yy<1930||yy>2027){err.textContent='请输入 1930 到 2027 年之间的出生日期。';return;}
  var r=pillarYear(d), y=r.y, zi=((y-4)%%12+12)%%12, si=((y-4)%%10+10)%%10;
  err.textContent='';
  var z=$('z'+zi); if(!z) return; z.checked=true;
  var yr=$('y'+zi+'_'+y); if(yr) yr.checked=true;
  var p=d.split('-'), pill=STEMS[si]+BRANCH[zi];
  $('dobres-t').innerHTML='按你的出生日期 <b>'+(+p[0])+' 年 '+(+p[1])+' 月 '+(+p[2])+' 日</b>，你的年柱是 <b>'+pill+'年</b>，生肖 <b>属'+ZOD[zi]+'</b>。'
    +'<small>生肖以立春为界，不是 1 月 1 日'+(y!==yy?'：你在立春之前出生，所以算前一年。':(r.onLichun?'：你刚好在立春当天出生，按新的一年算。':'。'))+'下面已经帮你打开你那一年的求财路线。</small>';
  $('dobres').className='on';
  try{if(window.fbq)fbq('track','ViewContent',{content_name:'zodiac_'+ZOD[zi]});}catch(e){}
  window.scrollTo({top:0,behavior:'smooth'});
}
$('dob-go').addEventListener('click',go);
$('dob-date').addEventListener('keydown',function(e){if(e.key==='Enter'){e.preventDefault();go();}});
document.querySelectorAll('.zgrid label').forEach(function(l){l.addEventListener('click',function(){$('dobres').className='';});});

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
try{post({event:'landing',ref:document.referrer||'',bot:navigator.webdriver?1:0});}catch(e){}
document.querySelectorAll('form[data-aigoal-lead]').forEach(function(f){f.addEventListener('submit',function(ev){ev.preventDefault();
  var d={},fields=[];f.querySelectorAll('input,select,textarea').forEach(function(el){var t=(el.type||'').toLowerCase();if(t==='submit'||t==='button'||t==='hidden'||t==='reset')return;if((t==='radio'||t==='checkbox')&&!el.checked)return;var v=(el.value||'').trim();if(!v)return;var nm=el.name||'';if(nm==='name'||nm==='phone'||nm==='email'){d[nm]=v;return;}var label=(el.getAttribute('data-label')||el.getAttribute('aria-label')||nm||'').trim();if(!label)return;fields.push({k:nm||label,l:label,v:v});});
  var dz=$('dobres').className==='on'?$('dobres-t').textContent.split('。')[0]:'';if(dz)fields.push({k:'dob_pillar',l:'出生年柱',v:dz});
  if(!d.phone&&!d.email){alert('请留电话或 email，不然联系不到你哦');return;}
  if(fields.length){d.fields=fields;d.note=fields.map(function(x){return x.l+': '+x.v;}).join('\\n');}
  d.event='register';var eid='ld.'+Date.now().toString(36)+'.'+Math.random().toString(36).slice(2,8);d.event_id=eid;
  try{if(window.fbq)fbq('track','Lead',{},{eventID:eid});}catch(e){}
  var btn=f.querySelector('[type="submit"]');if(btn){btn.disabled=true;btn.setAttribute('data-t',btn.textContent);btn.textContent='发送中…';}
  function done(ft){var u=NEXT;ft=ft||FT;if(ft)u+=(u.indexOf('?')<0?'?':'&')+'ft='+encodeURIComponent(ft);location.href=u;}
  post(d).then(function(r){if(!r||!r.ok)throw new Error('http');return r.json().then(function(j){done(j&&j.ft);}).catch(function(){done();});})
    .catch(function(){if(btn){btn.disabled=false;btn.textContent=btn.getAttribute('data-t');}alert('没发出去，再试一次或直接 WhatsApp 我们');});
});});
})();
</script>'''
JS = JS % {'slug': json.dumps(FUNNEL_SLUG), 'next': json.dumps(NEXT), 'lc': json.dumps({y: v for y, v in lc.items()})}
assert h.count('</body>') == 1
h = h.replace('</body>', JS + '\n</body>', 1)
open(out, 'w', encoding='utf8').write(h)
print('raw page', len(h))
