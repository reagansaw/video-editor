import json,re,sys
S='/tmp/claude-0/-home-user-video-editor/047dda4a-83c9-547c-814b-a439d5ed871f/scratchpad/'
new=json.load(open(S+'print/all/urls.json')); old=json.load(open(S+'pdf98/urls.json'))
book={y:v['u'] for y,v in new.items()}
# ---- guide page: button downloads the full book for the chosen year
g=json.load(open(S+'v1fix/g-src.json')); h=g['html']
assert 'window.PDFBOOK' not in h
inj='''function savePdf(btn){
  var _zi=+btn.getAttribute('data-zi'),_yr=pdfYear(_zi),_u=(window.PDFBOOK||{})[_yr];
  if(_u){var _t=btn.textContent;btn.disabled=true;btn.textContent='正在下载 PDF…';
    try{if(window.fbq)fbq('track','ViewContent',{content_name:'pdf_'+ZOD[_zi]});}catch(e){}
    try{post({event:'cta',cta:'pdf-download',source:'landing:'+OWN_SLUG});}catch(e){}
    fetch(_u).then(function(r){if(!r.ok)throw new Error('pdf '+r.status);return r.blob();}).then(function(b){
      var u=URL.createObjectURL(b),a=document.createElement('a');a.href=u;a.download='2027生肖财运指南-属'+ZOD[_zi]+'-'+_yr+'-林舒苑.pdf';document.body.appendChild(a);a.click();
      setTimeout(function(){URL.revokeObjectURL(u);a.remove();},4000);btn.disabled=false;btn.textContent=_t;
      if(document.documentElement.classList.contains('pdfmode')&&history.length>1){var bk=document.getElementById('pm-back');if(bk)bk.style.display='block';setTimeout(function(){history.back();},1800);}
    },function(){btn.disabled=false;btn.textContent=_t;location.href=_u;});return;}
'''
assert h.count('function savePdf(btn){')==1
h=h.replace('function savePdf(btn){',inj,1)
h=h.replace('<script>','<script>window.PDFBOOK='+json.dumps(book)+';</script><script>',1)
json.dump({'html':h,'updated':g['updated']},open(S+'v1fix/g-post.json','w'),ensure_ascii=False)
open(S+'v1fix/v1-book.html','w',encoding='utf8').write(h)
# ---- funnel page 2: swap the 98 links
p=json.load(open(S+'v1fix/p2-src.json')); t=p['html']; n=0
for y,v in old.items():
    if y in new and v['u'] in t: t=t.replace(v['u'],new[y]['u']); n+=1
json.dump({'html':t,'updated':p['updated']},open(S+'v1fix/p2-post.json','w'),ensure_ascii=False)
print('guide patched; page2 links swapped',n)
