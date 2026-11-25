const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
(async()=>{const W=+process.argv[2]||390;const b=await chromium.launch();const p=await b.newPage({viewport:{width:W,height:844},deviceScaleFactor:1});
const html=fs.readFileSync('rat/mock.html','utf8');
await p.route('https://2027shengxiaocaifu.suyenlim.com/**',async r=>{const u=new URL(r.request().url());
 if(u.pathname==='/')return r.fulfill({contentType:'text/html',body:html});
 if(u.pathname.startsWith('/ratimg/')){const f='rat/img/'+path.basename(u.pathname);return r.fulfill({body:fs.readFileSync(f),contentType:f.endsWith('png')?'image/png':'image/jpeg'})}
 if(u.pathname.startsWith('/api/'))return r.fulfill({contentType:'application/json',body:'{"ok":true}'});
 return r.continue()});
await p.goto('https://2027shengxiaocaifu.suyenlim.com/',{waitUntil:'networkidle'});
await p.addStyleTag({content:'.mbar,[data-aigoal-modal]{display:none!important}*{animation:none!important;transition:none!important}'});
await p.evaluate(()=>{document.getElementById('z0').checked=true;const y=document.querySelector('input[id="y0_1996"]');y.checked=true;y.dispatchEvent(new Event('change',{bubbles:true}));document.querySelectorAll('.rd0 img').forEach(i=>i.loading='eager')});
for(let y=0;y<30000;y+=600){await p.evaluate(v=>scrollTo(0,v),y);await p.waitForTimeout(30)}
await p.waitForTimeout(600);
await p.locator('.rd0').screenshot({path:`rat/mock-${W}.png`});
console.log(JSON.stringify(await p.evaluate(()=>[...document.querySelectorAll('.rd0 section')].map(s=>[s.id,Math.round(s.getBoundingClientRect().top-document.querySelector('.rd0').getBoundingClientRect().top)]))));
await b.close()})();
