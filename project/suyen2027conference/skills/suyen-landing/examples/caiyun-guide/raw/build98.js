const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const ys=JSON.parse(fs.readFileSync('pdf98/years.json'));const b=await chromium.launch();
const c=await b.newContext({viewport:{width:390,height:844},acceptDownloads:true});
await c.route(/\/api\/track/,r=>r.fulfill({contentType:'application/json',body:'{"ok":true}'}));await c.route(/facebook/,r=>r.abort());
const m=await c.newPage();let n=0;
for(const y of ys){const f='pdf98/'+y+'.pdf';if(fs.existsSync(f)&&fs.statSync(f).size>100000){n++;continue}
 for(let t=0;t<3;t++){try{const dl=m.waitForEvent('download',{timeout:40000});await m.goto('https://suyen2027-caiyun-full.aigoal.ai/?pdf='+y+'&_='+Date.now());const d=await dl;await d.saveAs(f);n++;break}catch(e){console.log('retry',y,e.message.slice(0,60))}}}
console.log('built',n,'of',ys.length);await b.close()})()
