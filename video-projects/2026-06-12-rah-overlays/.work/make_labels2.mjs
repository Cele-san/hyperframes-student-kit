import { chromium } from 'playwright';
const labels = [
  ['pick-0', '0 · CURRENT — ES Chime Notification'],
  ['pick-1', '1 · Message Send (iMessage-style)'],
  ['pick-2', '2 · Multimedia Positive 19'],
  ['pick-3', '3 · Multimedia 781 (short UI blip)'],
  ['pick-4', '4 · Notifications and Buttons 01'],
  ['pick-5', '5 · Notifications and Buttons 07'],
  ['pick-6', '6 · Notifications and Buttons 18'],
  ['pick-7', '7 · Bubble Drop 12'],
];
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1200, height: 200 } });
for (const [name, text] of labels) {
  await page.setContent(`<body style="margin:0;background:transparent"><span id="chip" style="
    display:inline-block;font:700 40px Helvetica,Arial,sans-serif;color:#fff;
    background:rgba(10,16,30,0.9);border:2px solid #f0a8c2;border-radius:10px;
    padding:20px 30px;">${text}</span></body>`);
  await page.locator('#chip').screenshot({ path: `.work/${name}.png`, omitBackground: true });
}
console.log('labels done');
await browser.close();
