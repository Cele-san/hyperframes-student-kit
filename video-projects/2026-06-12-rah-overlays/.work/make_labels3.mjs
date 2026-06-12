import { chromium } from 'playwright';
const labels = [
  ['wp-0', '0 · CURRENT — grid-sweep'],
  ['wp-1', '1 · Whoosh 1 — clean short'],
  ['wp-2', '2 · Whoosh 15 — airy'],
  ['wp-3', '3 · Woosh 8 — fast flick'],
  ['wp-4', '4 · Reverse Wipe — exit semantics'],
  ['wp-5', '5 · Whoosh Slow — soft air'],
  ['wp-6', '6 · Bed Sheet — organic fabric'],
  ['wp-7', '7 · NO SOUND — silent exit'],
];
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1300, height: 200 } });
for (const [name, text] of labels) {
  await page.setContent(`<body style="margin:0;background:transparent"><span id="chip" style="
    display:inline-block;font:700 42px Helvetica,Arial,sans-serif;color:#fff;
    background:rgba(10,16,30,0.9);border:2px solid #f0a8c2;border-radius:10px;
    padding:20px 30px;">${text}</span></body>`);
  await page.locator('#chip').screenshot({ path: `.work/${name}.png`, omitBackground: true });
}
console.log('labels done');
await browser.close();
