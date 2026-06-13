# Captions — karaoke pop & emphasis

Captions should feel like **graffiti on the frame, not a subtitle track.** Per-word pops, a stroke that holds readability, no background pill.

## Style rules (non-negotiable)

- Montserrat 900, **46–58px** for 1080 width (54px is the may-shorts-19 default), 100% white base.
- Active word: **scale pop + color to accent** (`#37bdf8` for AIS, adapt to brand).
- Stroke via **layered `text-shadow`**, NEVER `-webkit-text-stroke` (renders inconsistently in the Chromium render path).
- **Drop the rgba background pill** — let the stroke hold readability.
- **No `<br>`** inside captions — natural wrapping + `<br>` produces extra unwanted breaks.
- For retimes, use a `shift()` function inside `captions.html` to map transcript word timestamps → edited-time, keeping the transcript JSON untouched (see `references/pipeline.md`).
- Captions live on their own sub-composition (`track-index=2`), full duration. The generic caption mechanics also live in `/hyperframes` → `references/captions.md` — this file is the shortform-tuned karaoke specifics.

---

## 1 · karaoke-pop (the canonical implementation)

Extracted verbatim from `video-projects/may-shorts-19/compositions/captions.html`. Per-word `<span>`s, dim→active→spoken color cycle, a 9-layer text-shadow stroke, and the `shift()` edited-time remap. This is the reference; copy it and swap in your `SEGMENTS` + cut window.

```css
[data-composition-id="captions"]{position:absolute;inset:0;pointer-events:none}
[data-composition-id="captions"] .cap-stage{position:absolute;left:0;right:0;bottom:220px;height:0;pointer-events:none}
[data-composition-id="captions"] .cap-line-wrap{position:absolute;bottom:0;left:0;right:0;display:flex;
  justify-content:center;padding:0 60px;opacity:0;visibility:hidden}
[data-composition-id="captions"] .cap-line{display:inline-block;max-width:940px;background:transparent;padding:0 12px;
  text-align:center;font-family:"Montserrat",sans-serif;font-weight:900;font-size:54px;line-height:1.14;
  letter-spacing:-0.01em;color:#fff;white-space:normal;
  /* 9-layer stack = uniform 4px black stroke that renders reliably in Chromium (unlike -webkit-text-stroke) */
  text-shadow:-3px -3px 0 #07121c,3px -3px 0 #07121c,-3px 3px 0 #07121c,3px 3px 0 #07121c,
    -4px 0 0 #07121c,4px 0 0 #07121c,0 -4px 0 #07121c,0 4px 0 #07121c,0 6px 14px rgba(0,0,0,.55)}
[data-composition-id="captions"] .cap-word{display:inline-block;transform-origin:center center;will-change:transform,color}
```
```js
(function () {
  // Word-level transcript in ORIGINAL-time. shift() maps it to the edited timeline.
  const SEGMENTS = [
    { words: [ { word: "I", start: 0.0, end: 0.14 }, { word: "tested", start: 0.14, end: 0.38 }, /* … */ ] },
    // … one object per caption line …
  ];

  // Edit-shift for the cut (example: 1.12s removed from the 2.88–4.00s window of the original).
  function shift(t) {
    if (t <= 2.88) return t;     // before the cut — unchanged
    if (t < 4.0)  return 2.88;   // inside the cut — clamp to cut-in
    return t - 1.12;             // after the cut — slide back by cut length
  }

  const COMP_DURATION = 18.84;
  const DIM = "rgba(255,255,255,0.65)", ACTIVE = "#37bdf8", SPOKEN = "#ffffff", ACTIVE_SCALE = 1.14;
  const stage = document.querySelector('[data-composition-id="captions"] #cap-stage');
  if (!stage) return;

  // Build DOM: one wrapper per segment, word spans inside.
  SEGMENTS.forEach(function (seg, segIdx) {
    const wrap = document.createElement("div"); wrap.className = "cap-line-wrap"; wrap.id = "cap-seg-" + segIdx;
    const line = document.createElement("div"); line.className = "cap-line";
    seg.words.forEach(function (w, wIdx) {
      const span = document.createElement("span"); span.className = "cap-word";
      span.id = "cap-w-" + segIdx + "-" + wIdx; span.textContent = w.word; line.appendChild(span);
      if (wIdx < seg.words.length - 1) line.appendChild(document.createTextNode(" "));
    });
    wrap.appendChild(line); stage.appendChild(wrap);
  });

  const tl = gsap.timeline({ paused: true });
  const FADE_IN = 0.18, FADE_OUT = 0.18, PRE_ROLL = 0.12, POST_HOLD = 0.12;

  SEGMENTS.forEach(function (seg, segIdx) {
    const wrapSel = '[data-composition-id="captions"] #cap-seg-' + segIdx;
    const segStart = shift(seg.words[0].start), segEnd = shift(seg.words[seg.words.length - 1].end);
    const fadeInAt = Math.max(segStart - PRE_ROLL, 0), fadeOutAt = segEnd + POST_HOLD, hideAt = fadeOutAt + FADE_OUT + 0.05;

    seg.words.forEach(function (w, wIdx) {                  // reset to dim/rest before line appears
      tl.set('[data-composition-id="captions"] #cap-w-' + segIdx + "-" + wIdx, { color: DIM, scale: 1.0 }, fadeInAt);
    });
    tl.set(wrapSel, { visibility: "visible" }, fadeInAt);
    tl.fromTo(wrapSel, { opacity: 0, y: 8 }, { opacity: 1, y: 0, duration: FADE_IN, ease: "power2.out" }, fadeInAt);

    seg.words.forEach(function (w, wIdx) {                  // per-word karaoke pops
      const wordSel = '[data-composition-id="captions"] #cap-w-' + segIdx + "-" + wIdx;
      tl.to(wordSel, { color: ACTIVE, scale: ACTIVE_SCALE, duration: 0.08, ease: "back.out(3)" }, shift(w.start));
      tl.to(wordSel, { color: SPOKEN, scale: 1.0, duration: 0.12, ease: "power2.out" }, shift(w.end));
    });

    tl.to(wrapSel, { opacity: 0, duration: FADE_OUT, ease: "power2.in" }, fadeOutAt);
    tl.set(wrapSel, { visibility: "hidden" }, hideAt);
  });

  tl.set({}, {}, COMP_DURATION);                            // pad to composition duration (Law #11 form)
  window.__timelines = window.__timelines || {};
  window.__timelines["captions"] = tl;
})();
```

Note: this reference uses the older `tl.set({}, {}, DUR)` anchor; either form is valid (see `references/facecam.md`).

---

## 2 · emphasis-scale-bomb

One keyword detonates — scale to 1.35 with a glow flash, then settle. Budget **≤2 per short** or it stops reading as emphasis.

```js
// On the active keyword span, layered on top of the karaoke pop:
tl.to(kw, { scale: 1.35, textShadow: "0 0 30px rgba(55,189,248,.9)", duration: .18, ease: "back.out(2)" }, t)
  .to(kw, { scale: 1.0, textShadow: "0 0 0 rgba(55,189,248,0)", duration: .25, ease: "power2.out" }, t + .18);
```

---

## 3 · marker-sweep

A highlighter rect wipes in behind a keyword (`scaleX` from the left); the word flips to a dark color at the sweep's midpoint so it reads against the highlight.

```html
<span class="ms-key" id="ms-key">actually</span><span class="ms-hl" id="ms-hl"></span>
```
```css
[data-composition-id="captions"] .ms-key{position:relative;z-index:2}
[data-composition-id="captions"] .ms-hl{position:absolute;z-index:1;left:0;top:.12em;height:.86em;width:100%;
  background:#f09025;transform:scaleX(0);transform-origin:left;border-radius:4px}
```
```js
tl.fromTo("#ms-hl", { scaleX: 0 }, { scaleX: 1, duration: .3, ease: "power2.out" }, t);
tl.set("#ms-key", { color: "#07121c" }, t + .15);   // flip dark at sweep midpoint
```

---

## 4 · stacked-line-reveal

Lines stack 3–4 high; each new line enters from below while previous lines slide up one slot and dim. The quote-card workhorse.

```js
const LINES = gsap.utils.toArray("[data-composition-id='captions'] .sl-line");
const SLOT_H = 88;  // px per line
LINES.forEach((line, i) => {
  const at = i * 0.5;
  tl.fromTo(line, { y: 40, opacity: 0 }, { y: 0, opacity: 1, duration: .4, ease: "power3.out" }, at);
  LINES.slice(0, i).forEach((prev, j) => {                       // shove earlier lines up + dim
    tl.to(prev, { y: -SLOT_H * (i - j), opacity: .45, duration: .4, ease: "power3.out" }, at);
  });
});
```
