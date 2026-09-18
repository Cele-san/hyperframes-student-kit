const {chromium}=require('playwright');
const fs=require('fs'),crypto=require('crypto');
(async()=>{
const b=await chromium.launch({headless:true,...(process.env.PLAYWRIGHT_CHANNEL?{channel:process.env.PLAYWRIGHT_CHANNEL}:{})}),page=await b.newPage({viewport:{width:1920,height:1080}});
const errors=[];page.on('pageerror',e=>errors.push(e.message));
await page.goto('file://'+__dirname+'/index.html');await page.evaluate(async()=>{await document.fonts.ready;return true});
const hashes={},states=[];let repeatable=true;
for(const t of [5,7.3,14.8,21,29,5,29,7.3]){
 await page.evaluate(t=>{window.__timelines.main.seek(t,false)},t);
 const hash=crypto.createHash('sha256').update(await page.screenshot()).digest('hex');if(hashes[t]&&hashes[t]!==hash)repeatable=false;hashes[t]=hash;
 states.push(await page.evaluate(()=>window.gardenState));
}
const invariants=await page.evaluate(()=>{
 const get=(t,id)=>{window.__timelines.main.seek(t,false);const c=plants.find(c=>c.id===id);return {shell:c.shell.getAttribute('d'),strokes:c.strokes.map(n=>n.getAttribute('d')),opacity:c.g.getAttribute('opacity')}};
 const firstBefore=get(13.4,'hero'),firstAfter=get(14.8,'hero'),secondBefore=get(24.6,'read'),secondAfter=get(26.4,'read');
 let outside=[],invalid=[];for(const t of [.3,1,7.5,13,19.3,20,21,22,23.1,27,29]){window.__timelines.main.seek(t,false);for(const c of plants){if(+c.g.getAttribute('opacity')<.99)continue;const r=c.shell.getBBox();if(r.x<110||r.y<302||r.x+r.width>1810||r.y+r.height>942)outside.push({t,id:c.id,box:[r.x,r.y,r.width,r.height]});}document.querySelectorAll('svg *').forEach(n=>[...n.attributes].forEach(a=>{if(/NaN|undefined|Infinity/.test(a.value))invalid.push({t,id:n.id,attr:a.name})}));}
 let visitorOutside=[];for(const t of [13.2,14.7,18.8,19.5,20,21,22,23.1,26,29]){window.__timelines.main.seek(t,false);const r=visitor.getBoundingClientRect();if(r.left<110||r.top<302||r.right>1810||r.bottom>942)visitorOutside.push({t,rect:[r.left,r.top,r.right,r.bottom]});}return {visitorOutside,sourceIntactFirst:JSON.stringify(firstBefore)===JSON.stringify(firstAfter),sourceIntactSecond:JSON.stringify(secondBefore)===JSON.stringify(secondAfter),outside,invalid,leafCount:plants.length,veinPathCount:plants.reduce((n,c)=>n+c.strokes.length,0)};
});
const fixedCenters=states.every(s=>JSON.stringify(s.centers)===JSON.stringify(states[0].centers));
const result={repeatable,fixedCenters,errors,...invariants,hashes,cameraElevations:states.map(s=>[s.t,s.cameraElevation])};
fs.writeFileSync(__dirname+'/verification.json',JSON.stringify(result,null,2));console.log(JSON.stringify(result));await b.close();if(!repeatable||!fixedCenters||errors.length||!invariants.sourceIntactFirst||!invariants.sourceIntactSecond||invariants.visitorOutside.length||invariants.outside.length||invariants.invalid.length)process.exit(1);
})().catch(e=>{console.error(e);process.exit(1)});
