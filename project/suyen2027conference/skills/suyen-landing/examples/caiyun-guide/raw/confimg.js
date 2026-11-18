const {chromium}=require('playwright');const fs=require('fs');const DSF=1.25;
(async()=>{const b=await chromium.launch();const c=await b.newContext({viewport:{width:1100,height:900},deviceScaleFactor:DSF});const m=await c.newPage();
const html=fs.readFileSync('rawsite/prod-live.html','utf8');
await m.route('https://suyen2027-caiyun.aigoal.ai/**',async r=>{const u=new URL(r.request().url());
 if(u.pathname==='/')return r.fulfill({contentType:'text/html',body:html});
 if(u.pathname.startsWith('/api/'))return r.fulfill({contentType:'application/json',body:'{"ok":true}'});
 const res=await r.fetch({url:'https://app.aigoal.ai'+u.pathname});return r.fulfill({response:res});});
await m.route(/b-cdn\.net|mediadelivery|facebook/,r=>r.abort());
await m.goto('https://suyen2027-caiyun.aigoal.ai/',{waitUntil:'networkidle'});
await m.addStyleTag({content:'.ctab,.nx,.pdfwrap,.mbar,.ychips,[data-aigoal-modal]{display:none!important}*{animation:none!important;transition:none!important}#read .rd{padding:40px 44px 48px!important;background:#FBF4E8!important}'});
await m.evaluate(()=>{for(const e of document.querySelectorAll('body *')){const p=getComputedStyle(e).position;if((p==='fixed'||p==='sticky')&&!e.closest('#read'))e.style.setProperty('display','none','important')};document.getElementById('z0').checked=true});
await m.evaluate(()=>document.fonts.ready);
const g=await m.evaluate(()=>{const rd=document.querySelector('.rd0'),cf=rd.querySelector('.conf'),R=rd.getBoundingClientRect(),C=cf.getBoundingClientRect(),a=cf.querySelector('a.btn').getBoundingClientRect();
 return {x:R.left+scrollX,w:R.width,y:C.top+scrollY,h:C.height+48,btn:[a.left-R.left,a.top-C.top,a.width,a.height],href:cf.querySelector('a.btn').href}});
await m.screenshot({path:'pdfz/conf.jpg',type:'jpeg',quality:82,clip:{x:g.x,y:g.y,width:g.w,height:g.h},fullPage:true});
fs.writeFileSync('pdfz/conf.json',JSON.stringify(g));console.log(g);await b.close()})()
