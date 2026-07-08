// Deterministic gate: seek the facade + ref video, screenshot. No RAF reliance.
// Usage: node .work/gate_hook.mjs <slug> <t1> <t2> ...
// Requires `python3 -m http.server 8901` running in the project dir.
import { chromium } from 'playwright';
const [slug, ...ts] = process.argv.slice(2);
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
page.on('pageerror', e => { console.error('PAGE ERROR:', e.message); });
await page.goto(`http://127.0.0.1:8901/parts/${slug}/index.html`);
await page.waitForFunction(s => window.__timelines && window.__timelines[s], slug);
await page.evaluate(() => document.fonts.ready);
for (const t of ts.map(Number)) {
  await page.evaluate(async ([s, t]) => {
    window.__timelines[s].seek(t);
    const v = document.getElementById('ref-video');
    if (v) await new Promise(r => { v.onseeked = r; v.currentTime = t; });
  }, [slug, t]);
  await page.waitForTimeout(150);
  await page.screenshot({ path: `.work/gate-${slug}-${String(t).replace('.', '_')}.png` });
  console.log(`gate-${slug}-${t} ok`);
}
await browser.close();
