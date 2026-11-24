const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch();const c=await b.newContext({viewport:{width:1100,height:900},deviceScaleFactor:1.25});const m=await c.newPage();
const html=fs.readFileSync('rawsite/prod-live-c.html','utf8');
await m.route('https://suyen2027-caiyun.aigoal.ai/**',async r=>{const u=new URL(r.request().url());
 if(u.pathname==='/')return r.fulfill({contentType:'text/html',body:html});
 if(u.pathname.startsWith('/api/'))return r.fulfill({contentType:'application/json',body:'{"ok":true}'});
 const res=await r.fetch({url:'https://app.aigoal.ai'+u.pathname});return r.fulfill({response:res});});
await m.route(/b-cdn\.net|mediadelivery|facebook/,r=>r.abort());
await m.goto('https://suyen2027-caiyun.aigoal.ai/',{waitUntil:'networkidle'});
await m.addStyleTag({content:'.conf,.ctab,.nx,.pdfwrap,.mbar,.ychips,[data-aigoal-modal]{display:none!important}*{animation:none!important;transition:none!important}#read .rd{padding:40px 44px 48px!important;background:#FBF4E8!important}#read .rd .yc{display:block!important}'});
await m.evaluate(()=>{for(const e of document.querySelectorAll('body *')){const p=getComputedStyle(e).position;if((p==='fixed'||p==='sticky')&&!e.closest('#read'))e.style.setProperty('display','none','important')}});
const out={};
for(const zi of [0,1,2,3,4,5,6,7,8,9,10,11]){
 await m.evaluate(zi=>{document.getElementById('z'+zi).checked=true;const y=document.querySelector('input[id^="y'+zi+'_"]');y.checked=true;document.querySelectorAll('.rd'+zi+' img').forEach(i=>i.loading='eager')},zi);
 for(let y=0;y<30000;y+=1500){await m.evaluate(v=>scrollTo(0,v),y);await m.waitForTimeout(20)}
 await m.evaluate(()=>scrollTo(0,0));
 out[zi]=await m.evaluate(zi=>{const rd=document.querySelector('.rd'+zi),R=rd.getBoundingClientRect();
   const kids=[...rd.querySelectorAll('section, .sec, [class*="sec"], h2')].filter(e=>e.offsetHeight);
   return {H:R.height,tags:kids.slice(0,60).map(e=>[e.tagName+'.'+e.className,Math.round(e.getBoundingClientRect().top-R.top)])}},zi);
 if(zi==1) console.log(JSON.stringify(out[1]).slice(0,2500));
}
fs.writeFileSync('print/z/sections.json',JSON.stringify(out));await b.close()})();
