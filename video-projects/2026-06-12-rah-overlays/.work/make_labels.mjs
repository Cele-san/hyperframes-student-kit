import { chromium } from 'playwright';
const labels = [
  ['lbl-pop',    'POP — step ticker appears here'],
  ['lbl-tick',   'TICK — dot 2 fills'],
  ['lbl-typing', 'TYPING — prompt pill types'],
  ['lbl-chime',  'CHIME — send flash'],
  ['lbl-stamp',  'STAMP — APPROVED·UNREAD lands here'],
];
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1400, height: 200 } });
for (const [name, text] of labels) {
  await page.setContent(`<body style="margin:0;background:transparent"><span id="chip" style="
    display:inline-block;font:700 44px Helvetica,Arial,sans-serif;color:#fff;
    background:rgba(0,0,0,0.72);border:2px solid #f0a8c2;border-radius:10px;
    padding:18px 28px;">${text}</span></body>`);
  await page.locator('#chip').screenshot({ path: `.work/${name}.png`, omitBackground: true });
  console.log('made', name);
}
await browser.close();
