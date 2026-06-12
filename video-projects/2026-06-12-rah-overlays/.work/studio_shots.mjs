// Playwright self-check: screenshot the Studio player at given timestamps.
// Usage: node studio_shots.mjs <comp-id> <t1> <t2> ...
import { chromium } from 'playwright';

const PORT = process.env.STUDIO_PORT || '3003';
const [comp, ...times] = process.argv.slice(2);
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
await page.goto(`http://localhost:${PORT}/?comp=${comp}`, { waitUntil: 'domcontentloaded', timeout: 30000 });
await page.waitForTimeout(6000);

// Find the player and probe its API surface once.
const api = await page.evaluate(() => {
  const p = document.querySelector('hyperframes-player');
  if (!p) return { player: false };
  return {
    player: true,
    props: ['currentTime', 'seek', 'pause', 'play'].filter((k) => k in p),
  };
});
console.log('player api:', JSON.stringify(api));

for (const t of times.map(Number)) {
  await page.evaluate(async (t) => {
    const p = document.querySelector('hyperframes-player');
    if (p) {
      if ('pause' in p) try { p.pause(); } catch {}
      if ('currentTime' in p) p.currentTime = t;
      else if ('seek' in p) p.seek(t);
    }
    // also drive the iframe timeline directly as a fallback
    const iframe = p && p.shadowRoot ? p.shadowRoot.querySelector('iframe') : document.querySelector('iframe');
    const iw = iframe && iframe.contentWindow;
    if (iw && iw.__timelines) {
      Object.values(iw.__timelines).forEach((tl) => { try { tl.pause(); tl.seek(t); } catch {} });
    }
  }, t);
  await page.waitForTimeout(900);
  const out = `.work/shots/${comp}-t${t}.png`;
  await page.screenshot({ path: out });
  console.log('shot', out);
}
await browser.close();
