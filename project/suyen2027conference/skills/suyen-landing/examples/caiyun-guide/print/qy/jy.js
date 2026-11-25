const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://'+process.argv[2],{waitUntil:'networkidle'});await p.evaluate(()=>document.fonts.ready);
console.log(await p.evaluate(()=>{const r=document.getElementById('t').getBoundingClientRect();return [r.top*0.75,r.bottom*0.75]}));
await p.pdf({path:process.argv[3],width:'560px',height:'793.33px',printBackground:false});await b.close()})();
