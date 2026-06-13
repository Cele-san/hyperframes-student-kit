# Hooks & outros — the bookends

The first 3 seconds earn the swipe; the last 3 close the loop. Both ends share the same slam/pop vocabulary, so they live together.

**Recipe conventions** (apply to every snippet in this file and the other cookbook files):
- Each recipe is a sub-composition body. Wrap it in `<template id="<id>-template">` with a root `<div data-composition-id="<id>" data-start="0" data-duration="<SLOT>" data-width="1080" data-height="1920">`.
- Scope all CSS to `[data-composition-id="<id>"]`.
- Register exactly one paused timeline on `window.__timelines["<id>"]`, key == `data-composition-id`.
- **End every timeline with the Law #11 anchor:** `tl.to({}, { duration: SLOT }, 0)`.
- All values sized for 1080x1920. No `Math.random()` / `Date.now()` / `repeat: -1`. Snap tween ends to 1/30s.
- These show the DOM + scoped CSS + the timeline. Drop them into the `compositions/scene*.html` shape from `references/pipeline.md`.

---

## The hook contract (0–3s)

Beat 1 is the highest-leverage 90 frames in the short. It must: (1) land ONE idea, (2) move within the first 0.3s (no static t=0), (3) make the payoff word fully legible by ~0.4s so the viewer can read it before deciding to swipe. Pick ONE pattern below — never open on a plain centered fade.

---

## 1 · typography-slam

Hero word punches up with a white flash and a 2-frame settle. The default "stop the scroll" open. **Size the font to the word length** — 200px fits ~6 chars across 1080; a 9+ char word needs ~120–150px (or `font-size: clamp()`) or it clips the frame edges and the payoff word stops being legible.

```html
<div class="ts-wrap"><span class="ts-word" id="ts-word">POINTLESS</span></div>
<div class="ts-flash" id="ts-flash"></div>
```
```css
[data-composition-id="hook-slam"] .ts-wrap{position:absolute;inset:0;display:flex;align-items:center;justify-content:center}
[data-composition-id="hook-slam"] .ts-word{
  font:900 200px/1 Montserrat,sans-serif;letter-spacing:-.02em;color:#fff;
  text-shadow:0 0 40px rgba(55,189,248,.45),0 8px 30px rgba(0,0,0,.6);transform-origin:center}
[data-composition-id="hook-slam"] .ts-flash{position:absolute;inset:0;background:#fff;opacity:0;pointer-events:none}
```
```js
const SLOT = 2.0, tl = gsap.timeline({ paused: true });
tl.fromTo("#ts-word", { scale: .7, opacity: 0 },
  { scale: 1, opacity: 1, duration: .28, ease: "expo.out" }, .1);
tl.fromTo("#ts-flash", { opacity: .3 }, { opacity: 0, duration: .22, ease: "power2.out" }, .1);
tl.to("#ts-word", { scale: 1.04, duration: .0667, ease: "power2.out" }, .4)       // 2-frame settle up
  .to("#ts-word", { scale: 1, duration: .1, ease: "power2.inOut" }, .4667);       // 3-frame settle back — no overlap
tl.to({}, { duration: SLOT }, 0);
window.__timelines["hook-slam"] = tl;
```

---

## 2 · word-by-word-punch

Each word enters with a **decaying slide distance and duration** — the first word carries the cut's momentum, the rest settle geometrically. Anchor word starts to real Whisper onsets.

```html
<div class="wp-line">
  <span class="wp-w" data-i="0">Most</span> <span class="wp-w" data-i="1">skills</span>
  <span class="wp-w" data-i="2">are</span> <span class="wp-w" data-i="3">useless.</span>
</div>
```
```css
[data-composition-id="hook-punch"] .wp-line{position:absolute;inset:0;display:flex;flex-wrap:wrap;
  align-content:center;justify-content:center;gap:0 24px;padding:0 70px;text-align:center}
[data-composition-id="hook-punch"] .wp-w{display:inline-block;font:900 132px/1.05 Montserrat,sans-serif;
  color:#fff;text-shadow:-3px -3px 0 #07121c,3px 3px 0 #07121c,0 6px 18px rgba(0,0,0,.5);transform-origin:center}
```
```js
const SLOT = 2.4, tl = gsap.timeline({ paused: true });
const SLIDE = [120, 80, 48, 24], DUR = [.33, .30, .26, .22];   // decaying carrier → tail
const onset = [.10, .42, .70, .96];                            // replace with Whisper word starts (edited-time)
gsap.utils.toArray("[data-composition-id='hook-punch'] .wp-w").forEach((el, i) => {
  tl.fromTo(el, { y: SLIDE[i], opacity: 0 },
    { y: 0, opacity: 1, duration: DUR[i], ease: "expo.out" }, onset[i]);
});
tl.to("[data-composition-id='hook-punch'] .wp-w[data-i='3']",
  { color: "#37bdf8", duration: .12, ease: "power2.out" }, 1.0);   // flip the payoff word
tl.to({}, { duration: SLOT }, 0);
window.__timelines["hook-punch"] = tl;
```

---

## 3 · shock-stat-counter

A number rolls up fast and locks with a scale-bomb; the label pops after the lock. Deterministic — a proxy object drives `textContent`, no random.

```html
<div class="sc-stack">
  <div class="sc-num" id="sc-num">0</div>
  <div class="sc-label" id="sc-label">skills tested</div>
</div>
```
```css
[data-composition-id="hook-stat"] .sc-stack{position:absolute;inset:0;display:flex;flex-direction:column;
  align-items:center;justify-content:center;gap:18px}
[data-composition-id="hook-stat"] .sc-num{font:900 320px/.9 "Roboto Mono",monospace;color:#fff;
  text-shadow:0 0 50px rgba(55,189,248,.5);transform-origin:center}
[data-composition-id="hook-stat"] .sc-label{font:700 56px/1 Montserrat,sans-serif;letter-spacing:.02em;
  color:#37bdf8;opacity:0;transform-origin:center}
```
```js
const SLOT = 2.2, tl = gsap.timeline({ paused: true });
const num = { v: 0 }, el = document.querySelector("[data-composition-id='hook-stat'] #sc-num");
tl.to(num, { v: 127, duration: .9, ease: "power3.out",
  onUpdate: () => { el.textContent = Math.round(num.v); } }, .1);
tl.to("#sc-num", { scale: 1.12, duration: .1, ease: "back.out(3)" }, 1.0)   // lock scale-bomb
  .to("#sc-num", { scale: 1, duration: .18, ease: "power2.out" }, 1.1);
tl.to("#sc-label", { opacity: 1, y: 0, duration: .2, ease: "back.out(1.7)" }, 1.15);  // label after lock
tl.to({}, { duration: SLOT }, 0);
window.__timelines["hook-stat"] = tl;
```

---

## 4 · question-pop-scribble

A question pops in; an SVG scribble strokes under the key word a beat later. Great for "did you know / what if" openers.

```html
<div class="qp-wrap">
  <div class="qp-q">Is your <span class="qp-key">prompt</span> the problem?</div>
  <svg class="qp-scribble" viewBox="0 0 320 40" id="qp-scribble">
    <path id="qp-path" d="M6 24 C 60 8, 120 36, 180 20 S 280 12, 314 26" fill="none"
      stroke="#f09025" stroke-width="9" stroke-linecap="round"/>
  </svg>
</div>
```
```css
[data-composition-id="hook-question"] .qp-wrap{position:absolute;inset:0;display:flex;flex-direction:column;
  align-items:center;justify-content:center;padding:0 70px;text-align:center}
[data-composition-id="hook-question"] .qp-q{font:900 110px/1.12 Montserrat,sans-serif;color:#fff;
  text-shadow:-3px -3px 0 #07121c,3px 3px 0 #07121c,0 6px 18px rgba(0,0,0,.5)}
[data-composition-id="hook-question"] .qp-key{color:#37bdf8}
[data-composition-id="hook-question"] .qp-scribble{width:340px;height:42px;margin-top:14px;overflow:visible}
```
```js
const SLOT = 2.4, tl = gsap.timeline({ paused: true });
const path = document.querySelector("[data-composition-id='hook-question'] #qp-path");
const L = path.getTotalLength();
path.style.strokeDasharray = L; path.style.strokeDashoffset = L;
tl.fromTo("[data-composition-id='hook-question'] .qp-q", { scale: .85, opacity: 0 },
  { scale: 1, opacity: 1, duration: .35, ease: "back.out(1.4)" }, .1);
tl.to(path, { strokeDashoffset: 0, duration: .35, ease: "power2.out" }, .7);
tl.to({}, { duration: SLOT }, 0);
window.__timelines["hook-question"] = tl;
```

---

## 5 · before-after-vertical-split

The frame splits at y=960: BEFORE slides down from the top half, AFTER up from the bottom, a divider scan-line sweeps across, labels stamp after the panels rest. The portrait-native comparison hook.

```html
<div class="ba-top" id="ba-top"><span class="ba-label" id="ba-l1">BEFORE</span></div>
<div class="ba-bot" id="ba-bot"><span class="ba-label ba-hot" id="ba-l2">AFTER</span></div>
<div class="ba-div" id="ba-div"></div>
```
```css
[data-composition-id="hook-split"] .ba-top,[data-composition-id="hook-split"] .ba-bot{
  position:absolute;left:0;width:1080px;height:960px;display:flex;align-items:center;justify-content:center}
[data-composition-id="hook-split"] .ba-top{top:0;background:linear-gradient(180deg,#0c1420,#0a0f18)}
[data-composition-id="hook-split"] .ba-bot{top:960px;background:linear-gradient(180deg,#0a0f18,#0c1c14)}
[data-composition-id="hook-split"] .ba-label{font:900 120px/1 Montserrat,sans-serif;color:#9fb2c4;opacity:0}
[data-composition-id="hook-split"] .ba-hot{color:#37bdf8}
[data-composition-id="hook-split"] .ba-div{position:absolute;top:957px;left:0;width:1080px;height:6px;
  background:linear-gradient(90deg,transparent,#37bdf8,transparent);box-shadow:0 0 24px rgba(55,189,248,.7);
  transform:scaleX(0);transform-origin:left}
```
```js
const SLOT = 2.6, tl = gsap.timeline({ paused: true });
tl.fromTo("#ba-top", { y: -120, opacity: 0 }, { y: 0, opacity: 1, duration: .5, ease: "power3.out" }, .1);
tl.fromTo("#ba-bot", { y: 120, opacity: 0 }, { y: 0, opacity: 1, duration: .5, ease: "power3.out" }, .1);
tl.fromTo("#ba-div", { scaleX: 0 }, { scaleX: 1, duration: .5, ease: "power2.out" }, .3);
tl.to(["#ba-l1", "#ba-l2"], { opacity: 1, duration: .2, ease: "back.out(1.7)", stagger: .08 }, .7);
tl.to({}, { duration: SLOT }, 0);
window.__timelines["hook-split"] = tl;
```

---

# CTA / outro patterns

The close. End on a clear action and — ideally — loop seamlessly back to frame 0.

## 6 · follow-button-pop

Pill pops in, a faux-cursor click fires (full sequence in `references/scenes.md`), label swaps to "Following".

```html
<div class="fb-wrap"><button class="fb-btn" id="fb-btn"><span id="fb-label">Follow</span></button>
  <svg class="fb-cursor" id="fb-cursor" viewBox="0 0 24 24" width="56" height="56">
    <path d="M4.3 2.6 L20 12 L12 13 L9 21 Z" fill="#fff" stroke="#07121c" stroke-width="1.5"/></svg></div>
```
```css
[data-composition-id="outro-follow"] .fb-wrap{position:absolute;inset:0;display:flex;align-items:center;justify-content:center}
[data-composition-id="outro-follow"] .fb-btn{font:800 60px/1 Montserrat,sans-serif;color:#fff;
  background:#37bdf8;border:none;border-radius:999px;padding:34px 90px;transform-origin:center;
  box-shadow:0 10px 40px rgba(55,189,248,.5)}
[data-composition-id="outro-follow"] .fb-cursor{position:absolute;left:58%;top:58%;transform-origin:4.3px 2.6px}
```
```js
const SLOT = 3.0, tl = gsap.timeline({ paused: true });
tl.fromTo("#fb-btn", { scale: 0, opacity: 0 }, { scale: 1, opacity: 1, duration: .4, ease: "back.out(1.7)" }, .2);
tl.to("#fb-cursor", { left: "50%", top: "50%", duration: .4, ease: "power3.inOut" }, .7);
tl.to("#fb-cursor", { scale: .82, duration: .07, ease: "power4.in" }, 1.1)        // click compress
  .to("#fb-btn", { scale: .96, duration: .07, ease: "power4.in" }, 1.1)
  .to("#fb-cursor", { scale: 1, duration: .3, ease: "back.out(3)" }, 1.18)
  .to("#fb-btn", { scale: 1.02, duration: .2, ease: "elastic.out(1,0.4)" }, 1.18)
  .to("#fb-btn", { scale: 1, duration: .2, ease: "power2.out" }, 1.38);
tl.add(() => { document.querySelector("[data-composition-id='outro-follow'] #fb-label").textContent = "Following"; }, 1.2);
tl.to("#fb-btn", { backgroundColor: "#1c2b3a", duration: .25, ease: "power2.out" }, 1.2);
tl.to({}, { duration: SLOT }, 0);
window.__timelines["outro-follow"] = tl;
```

## 7 · subscribe-bounce

Button settles with elastic overshoot; a bell rocks ±12° in decaying swings. Finite swings only (no `repeat:-1`).

```js
const SLOT = 2.6, tl = gsap.timeline({ paused: true });
tl.fromTo("#sb-btn", { scale: 0 }, { scale: 1, duration: .5, ease: "elastic.out(1,0.4)" }, .2);
[12, -9, 6, -3, 0].forEach((deg, i) =>
  tl.to("#sb-bell", { rotation: deg, duration: .12, ease: "sine.inOut" }, .7 + i * .12));  // decaying bell swing
tl.to({}, { duration: SLOT }, 0);
window.__timelines["outro-subscribe"] = tl;
```

## 8 · profile-card-slide

Card slides up from below; avatar pops, handle types via `steps()`, follower counter rolls.

```js
const SLOT = 3.0, tl = gsap.timeline({ paused: true });
tl.fromTo("#pc-card", { yPercent: 120 }, { yPercent: 0, duration: .7, ease: "power3.out" }, .15);
tl.fromTo("#pc-avatar", { scale: 0 }, { scale: 1, duration: .35, ease: "back.out(1.7)" }, .6);
const handle = "@diepandy", el = document.querySelector("[data-composition-id='outro-profile'] #pc-handle");
const ch = { n: 0 };
tl.to(ch, { n: handle.length, duration: .5, ease: "steps(" + handle.length + ")",
  onUpdate: () => { el.textContent = handle.slice(0, Math.round(ch.n)); } }, .8);
const f = { v: 0 }, fel = document.querySelector("[data-composition-id='outro-profile'] #pc-followers");
tl.to(f, { v: 24300, duration: .9, ease: "power3.out",
  onUpdate: () => { fel.textContent = Math.round(f.v).toLocaleString(); } }, 1.0);
tl.to({}, { duration: SLOT }, 0);
window.__timelines["outro-profile"] = tl;
```

## 9 · loop-back-to-hook

**Not a visual — a constraint.** The outro's final 0.3–0.5s must recreate frame-0's visual state (same element positions, opacities, colors as the hook's start) so the platform's auto-loop is seamless and the viewer falls back into the hook without a seam.

Implementation: in the last scene, tween the on-screen elements toward the exact resting values the hook scene sets at its t=0 (e.g. fade the CTA out while bringing up a ghost of the hook word at the hook's start scale/opacity). Then the loop reads as one continuous motion. Spec to verify: **end-state == hook start-state** — extract the last frame and frame-0, Read both, confirm they match.
