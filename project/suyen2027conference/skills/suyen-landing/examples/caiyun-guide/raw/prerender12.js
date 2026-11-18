const {chromium}=require('playwright');const fs=require('fs');const DSF=1.25;
(async()=>{const b=await chromium.launch();const c=await b.newContext({viewport:{width:1100,height:900},deviceScaleFactor:DSF});const m=await c.newPage();
const html=fs.readFileSync('rawsite/prod-live.html','utf8');
await m.route('https://suyen2027-caiyun.aigoal.ai/**',async r=>{const u=new URL(r.request().url());
 if(u.pathname==='/')return r.fulfill({contentType:'text/html',body:html});
 if(u.pathname.startsWith('/api/'))return r.fulfill({contentType:'application/json',body:'{"ok":true}'});
 const res=await r.fetch({url:'https://app.aigoal.ai'+u.pathname});return r.fulfill({response:res});});
await m.route(/b-cdn\.net|mediadelivery|facebook/,r=>r.abort());
await m.goto('https://suyen2027-caiyun.aigoal.ai/',{waitUntil:'networkidle'});
await m.addStyleTag({content:'.conf,.ctab,.nx,.pdfwrap,.mbar,.ychips,[data-aigoal-modal]{display:none!important}*{animation:none!important;transition:none!important}#read .rd{padding:40px 44px 48px!important;background:#FBF4E8!important}#read .rd .yc{display:block!important}'});
await m.evaluate(()=>{for(const e of document.querySelectorAll('body *')){const p=getComputedStyle(e).position;if((p==='fixed'||p==='sticky')&&!e.closest('#read'))e.style.setProperty('display','none','important')}});
const meta={};
for(let zi=0;zi<12;zi++){
 const first=await m.evaluate(zi=>{document.getElementById('z'+zi).checked=true;const y=document.querySelector('input[id^="y'+zi+'_"]');y.checked=true;document.querySelectorAll('.rd'+zi+' img').forEach(i=>i.loading='eager');return y.id},zi);
 for(let y=0;y<30000;y+=700){await m.evaluate(v=>scrollTo(0,v),y);await m.waitForTimeout(30)}
 await m.evaluate(async zi=>{await Promise.all([...document.querySelectorAll('.rd'+zi+' img')].map(i=>(i.complete&&i.naturalWidth)?(i.decode?i.decode().catch(()=>0):0):new Promise(ok=>{i.addEventListener('load',ok);i.addEventListener('error',ok)})));await document.fonts.ready},zi);
 await m.evaluate(()=>scrollTo(0,0));await m.waitForTimeout(150);
 const g=await m.evaluate(zi=>{const rd=document.querySelector('.rd'+zi),R=rd.getBoundingClientRect();const cards={};let a=1e9,z=0;
   for(const e of rd.querySelectorAll('.yc')){const r=e.getBoundingClientRect(),y=(e.className.match(/yc\d+_(\d+)/)||[])[1];const cs=getComputedStyle(e);
     const t=r.top-R.top,bo=r.bottom-R.top;cards[y]=[t,bo];a=Math.min(a,t);z=Math.max(z,bo)}
   return {W:R.width,H:R.height,top:a,bottom:z,cards}},zi);
 await m.locator('.rd'+zi).screenshot({path:'pdfz/z'+zi+'.jpg',type:'jpeg',quality:80});
 meta[zi]=g;process.stdout.write(zi+' ')}
fs.writeFileSync('pdfz/meta.json',JSON.stringify(meta));await b.close();console.log('done')})()
