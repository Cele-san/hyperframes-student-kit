# Scenes — b-roll patterns & data/proof beats

The middle of the short. B-roll patterns carry footage/UI; data beats turn claims into evidence. Recipe conventions are the same as `references/hooks.md` (template wrapper, scoped CSS, paused timeline, Law #11 anchor, no random, 1/30s snapping).

## Scene pacing rules (run on every scene)

- **No dead frames.** Every 100ms has ≥1 animating element. Offset the first entrance 0.1–0.3s, not t=0.
- **Payoff ≥ 1s hold.** The reveal (stamp, number lock, punchline) gets ≥1s on screen, ideally 1.5s. Budget by reveal time, not total time.
- **Motion through full duration.** If entrances all land by local 2s on a 4s scene, add secondary motion — underline sweeps, checkmark pops, ambient card drift, small oscillating glows.
- **Vary eases.** ≥3 different eases per scene across entrances.
- **One jaw-dropper per 5s.** Typography slam, glitch, whip, audio-sync slam.

---

# B-roll patterns

## 1 · vertical-ken-burns

A still fills the portrait frame and slowly scales + drifts. Animate the **wrapper**, never the `<img>`/`<video>` (animating media dims freezes frames). Alternate pan direction between consecutive stills.

```html
<div class="kb-wrap" id="kb-wrap"><img class="kb-img" src="assets/shot.jpg"></div>
```
```css
[data-composition-id="scene-kb"] .kb-wrap{position:absolute;inset:0;overflow:hidden}
[data-composition-id="scene-kb"] .kb-img{width:1080px;height:1920px;object-fit:cover;will-change:transform}
```
```js
const SLOT = 3.0, tl = gsap.timeline({ paused: true });
tl.fromTo("#kb-wrap", { scale: 1.0, y: 0 }, { scale: 1.10, y: -30, duration: SLOT, ease: "none" }, 0);
tl.to({}, { duration: SLOT }, 0);
window.__timelines["scene-kb"] = tl;
```

## 2 · phone-mockup-scroll

A phone chrome frame holds a screenshot that scrolls between hardcoded stops with a hold at each.

```css
[data-composition-id="scene-phone"] .pm-frame{position:absolute;left:110px;top:240px;width:860px;height:1440px;
  border-radius:64px;border:14px solid #0c1620;overflow:hidden;box-shadow:0 30px 80px rgba(0,0,0,.6)}
[data-composition-id="scene-phone"] .pm-shot{width:860px;will-change:transform}  /* tall image */
```
```js
const SLOT = 4.0, tl = gsap.timeline({ paused: true });
const STOPS = [0, -520, -1040];   // hardcoded scroll positions
STOPS.forEach((y, i) => {
  if (i === 0) tl.set("#pm-shot", { y }, 0);
  else tl.to("#pm-shot", { y, duration: .6, ease: "power2.inOut" }, .2 + i * 1.1);  // hold ≥0.8s between hops
});
tl.to({}, { duration: SLOT }, 0);
window.__timelines["scene-phone"] = tl;
```

## 3 · browser-slide-up

A browser-chrome card rises from below; the URL types in via a `steps()` width tween; content rows stagger in.

```js
const SLOT = 3.5, tl = gsap.timeline({ paused: true });
tl.fromTo("#bw-card", { yPercent: 100 }, { yPercent: 0, duration: .8, ease: "power3.out" }, .1);
const url = "claude.ai/code", el = document.querySelector("[data-composition-id='scene-browser'] #bw-url");
const ch = { n: 0 };
tl.to(ch, { n: url.length, duration: .6, ease: "steps(" + url.length + ")",
  onUpdate: () => { el.textContent = url.slice(0, Math.round(ch.n)); } }, .9);
tl.fromTo("[data-composition-id='scene-browser'] .bw-row", { x: -40, opacity: 0 },
  { x: 0, opacity: 1, duration: .3, ease: "power2.out", stagger: .08 }, 1.4);
tl.to({}, { duration: SLOT }, 0);
window.__timelines["scene-browser"] = tl;
```

## 4 · list-cascade-check

Items slide in staggered; once they rest, SVG check ticks stroke-draw in sequence. The listicle workhorse.

```js
const SLOT = 4.0, tl = gsap.timeline({ paused: true });
tl.fromTo("[data-composition-id='scene-list'] .lc-item", { x: -60, opacity: 0 },
  { x: 0, opacity: 1, duration: .35, ease: "power3.out", stagger: .16 }, .15);
gsap.utils.toArray("[data-composition-id='scene-list'] .lc-check").forEach((p, i) => {
  const L = p.getTotalLength(); p.style.strokeDasharray = L; p.style.strokeDashoffset = L;
  tl.to(p, { strokeDashoffset: 0, duration: .2, ease: "power2.out" }, 1.0 + i * .2);
});
tl.to({}, { duration: SLOT }, 0);
window.__timelines["scene-list"] = tl;
```

## 5 · faux-cursor-click

The full 7-tween sequence that sells a UI interaction. The cursor SVG's `transform-origin` MUST sit at the click-tip pixel (e.g. `transform-origin: 4.3px 2.6px`).

```js
const tl = gsap.timeline({ paused: true });
tl.to("#cursor", { scale: .82, duration: .07, ease: "power4.in" }, t)            // 1 cursor compress
  .to("#target", { scale: .96, duration: .07, ease: "power4.in" }, t)            // 2 target compress
  .set("#ripple", { scale: 0, opacity: .9 }, t + .07)                            // 3 ripple…
  .to("#ripple", { scale: 2.5, opacity: 0, duration: .2, ease: "power2.out" }, t + .07)
  .to("#cursor", { scale: 1, duration: .3, ease: "back.out(3)" }, t + .1)        // 4 cursor release
  .to("#target", { scale: 1.02, duration: .2, ease: "elastic.out(1,0.4)" }, t + .1)  // 5 overshoot
  .to("#target", { scale: 1, duration: .2, ease: "power2.out" }, t + .3);        // 6 settle  (7 = the resulting nav/state change you wire after)
```

---

# Proof / data beats

The middle grind is where attention drops hardest. Lean on visuals that read as **information**, not decoration — a number ticking, a bar filling, a chart stroking in, a grid flashing in sequence. (This is the may-shorts-18 lesson #4: data-feel scenes feel like evidence; typography-plus-icon scenes feel like slides.)

## 6 · counter-roll-up

Same proxy-object engine as the hook stat, framed for mid-video. Deterministic — `onUpdate` writes formatted `textContent`.

```js
const SLOT = 2.5, tl = gsap.timeline({ paused: true });
const num = { v: 0 }, el = document.querySelector("[data-composition-id='scene-counter'] #ct-num");
tl.to(num, { v: 4.2, duration: 1.0, ease: "power3.out",
  onUpdate: () => { el.textContent = num.v.toFixed(1) + "×"; } }, .2);
tl.to("#ct-num", { scale: 1.1, duration: .1, ease: "back.out(3)" }, 1.2)
  .to("#ct-num", { scale: 1, duration: .18, ease: "power2.out" }, 1.3);
tl.to({}, { duration: SLOT }, 0);
window.__timelines["scene-counter"] = tl;
```

## 7 · percentage-ring

An SVG ring fills via `stroke-dashoffset`; the center number counts from the SAME proxy so ring and number stay locked.

```html
<svg class="pr-svg" viewBox="0 0 200 200">
  <circle cx="100" cy="100" r="86" fill="none" stroke="#1c2b3a" stroke-width="16"/>
  <circle id="pr-arc" cx="100" cy="100" r="86" fill="none" stroke="#37bdf8" stroke-width="16"
    stroke-linecap="round" transform="rotate(-90 100 100)"/>
</svg><div class="pr-num" id="pr-num">0%</div>
```
```js
const SLOT = 2.6, tl = gsap.timeline({ paused: true });
const arc = document.querySelector("[data-composition-id='scene-ring'] #pr-arc");
const C = 2 * Math.PI * 86; arc.style.strokeDasharray = C; arc.style.strokeDashoffset = C;
const p = { v: 0 }, el = document.querySelector("[data-composition-id='scene-ring'] #pr-num");
tl.to(p, { v: 73, duration: 1.2, ease: "power2.inOut", onUpdate: () => {
  arc.style.strokeDashoffset = C * (1 - p.v / 100); el.textContent = Math.round(p.v) + "%"; } }, .2);
tl.to({}, { duration: SLOT }, 0);
window.__timelines["scene-ring"] = tl;
```

## 8 · bar-race

3–5 horizontal bars grow from the left, staggered; value labels count alongside. For an "overtake," swap two bars' `y` via a `power2.inOut` tween.

```js
const SLOT = 3.2, tl = gsap.timeline({ paused: true });
const BARS = [ { sel: "#b0", w: 920, val: 127 }, { sel: "#b1", w: 540, val: 74 }, { sel: "#b2", w: 300, val: 41 } ];
BARS.forEach((b, i) => {
  tl.fromTo(b.sel, { scaleX: 0 }, { scaleX: 1, duration: .8, ease: "power3.out" }, .2 + i * .15);  // transform-origin:left in CSS
  const o = { v: 0 }, el = document.querySelector("[data-composition-id='scene-bars'] " + b.sel + "-val");
  tl.to(o, { v: b.val, duration: .8, ease: "power3.out", onUpdate: () => { el.textContent = Math.round(o.v); } }, .2 + i * .15);
});
tl.to({}, { duration: SLOT }, 0);
window.__timelines["scene-bars"] = tl;
```

## 9 · graph-draw-on

An SVG line strokes on; the area fill fades up after the stroke; a YOU-ARE-HERE dot pops at the path end. (The may-shorts-18 sparkline move.)

```js
const SLOT = 3.0, tl = gsap.timeline({ paused: true });
const path = document.querySelector("[data-composition-id='scene-graph'] #gr-line");
const L = path.getTotalLength(); path.style.strokeDasharray = L; path.style.strokeDashoffset = L;
tl.to(path, { strokeDashoffset: 0, duration: 1.0, ease: "power2.out" }, .2);
tl.fromTo("#gr-fill", { opacity: 0 }, { opacity: .35, duration: .4, ease: "power2.out" }, 1.1);  // area fill after stroke
tl.fromTo("#gr-dot", { scale: 0 }, { scale: 1, duration: .25, ease: "back.out(2)" }, 1.2);        // YOU-ARE-HERE dot
tl.to({}, { duration: SLOT }, 0);
window.__timelines["scene-graph"] = tl;
```

---

When a middle scene feels bland, replace the decoration with one of beats 6–9: a small number ticking up, a bar filling, a chart stroking in, a grid flashing in sequence. That single swap is the difference between "labeled talking head" and "this is evidence."
