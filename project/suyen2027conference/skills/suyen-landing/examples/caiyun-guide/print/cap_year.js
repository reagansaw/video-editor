// capture one zodiac guide exactly as the visitor of that birth year sees it
const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const years=process.argv.slice(2).map(Number);const b=await chromium.launch();
const c=await b.newContext({viewport:{width:1100,height:900},deviceScaleFactor:1.25});const m=await c.newPage();
const html=fs.readFileSync('rawsite/prod-live-c.html','utf8');
await m.route('https://suyen2027-caiyun.aigoal.ai/**',async r=>{const u=new URL(r.request().url());
 if(u.pathname==='/')return r.fulfill({contentType:'text/html',body:html});
 if(u.pathname.startsWith('/api/'))return r.fulfill({contentType:'application/json',body:'{"ok":true}'});
 const res=await r.fetch({url:'https://app.aigoal.ai'+u.pathname});return r.fulfill({response:res});});
await m.route(/b-cdn\.net|mediadelivery|facebook/,r=>r.abort());
await m.goto('https://suyen2027-caiyun.aigoal.ai/',{waitUntil:'networkidle'});
await m.addStyleTag({content:'.conf,.ctab,.nx,.pdfwrap,.mbar,.ychips,.ypanel>b,[data-aigoal-modal]{display:none!important}#read .nxt{display:block!important}*{animation:none!important;transition:none!important}#read .rd{padding:40px 44px 48px!important;background:#FBF4E8!important}'});
await m.evaluate(()=>{for(const e of document.querySelectorAll('body *')){const p=getComputedStyle(e).position;if((p==='fixed'||p==='sticky')&&!e.closest('#read'))e.style.setProperty('display','none','important')}});
fs.mkdirSync('print/zy',{recursive:true});
for(const y of years){const zi=((y-4)%12+12)%12;
 await m.evaluate(([zi,y])=>{document.getElementById('z'+zi).checked=true;document.getElementById('y'+zi+'_'+y).checked=true;document.querySelectorAll('.rd'+zi+' img').forEach(i=>i.loading='eager')},[zi,y]);
 for(let s=0;s<30000;s+=700){await m.evaluate(v=>scrollTo(0,v),s);await m.waitForTimeout(25)}
 await m.evaluate(async zi=>{await Promise.all([...document.querySelectorAll('.rd'+zi+' img')].map(i=>(i.complete&&i.naturalWidth)?0:new Promise(ok=>{i.addEventListener('load',ok);i.addEventListener('error',ok)})));await document.fonts.ready;scrollTo(0,0)},zi);
 await m.waitForTimeout(1500);
 await m.locator('.rd'+zi).screenshot({path:`print/zy/${y}.jpg`,type:'jpeg',quality:82});process.stdout.write(y+' ')}
await b.close();console.log('done')})();
