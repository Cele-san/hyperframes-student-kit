# Face-cam track — the talking head

The signature short-form move: a landscape face recording choreographed between a bottom-half mode and a full-screen mode, graded so it reads as a character, with scene overlays and karaoke captions over the top. Constants below are validated against `video-projects/may-shorts-19/index.html`.

---

## The face wrapper rule

The face lives in a **wrapper div sized at the source's native landscape (1920x1080)**. GSAP animates the WRAPPER — never the `<video>` element. Animating `<video>` width/height/top/left freezes frames.

```html
<div id="face-wrapper">
  <video id="face-video" data-start="0" data-duration="<DUR>" data-track-index="0"
         src="assets/<name>-edit.mp4" muted playsinline></video>
</div>
<!-- audio is a SEPARATE sibling element so the mixer owns it -->
<audio id="face-audio" data-start="0" data-duration="<DUR>" data-track-index="4"
       data-volume="1" src="assets/<name>-edit.mp4"></audio>
```

```css
#face-wrapper {
  position: absolute; top: 0; left: 0;
  width: 1920px; height: 1080px;   /* source native */
  transform-origin: 0 0;
  transform: translate(0px, 1136px) scale(0.5625);  /* initial BOTTOM */
  z-index: 0;
}
```

`class="clip"` never goes on `<video>` or `<audio>` — it breaks them.

---

## The two modes

```js
const BOTTOM     = { x: 0,       y: 1136, scale: 0.5625 }; // bottom-half, full landscape visible
const FULLSCREEN = { x: -1166.5, y: 0,    scale: 1.7778 }; // cropped-cover, fills 1080x1920
const MODE_DUR   = 0.32;
```

- `BOTTOM` at `scale 0.5625` (= 1080/1920) renders the 1920x1080 source at 1080x607.5, centered in the bottom 960px (176px navy above/below).
- `FULLSCREEN` at `scale 1.7778` with `x = -1166.5` horizontally center-crops the landscape into the portrait frame.

### BOTTOM scale — don't ship the geometric default (may-shorts-18 lesson)

`scale 0.5625` is the exact horizontal fit, but it leaves empty studio background flanking the speaker whenever they occupy <70% of the source frame. **Start from the framing-preferred override and preview ONE frame before committing:**

```js
const BOTTOM = { x: -180, y: 1110, scale: 0.75 }; // crops 180px each side, bottom-anchors to y=1920
```

Tight-framed source → `scale 0.65` may be enough; wide studio framing → push to `0.80` and re-tune `x`. **Always extract one BOTTOM frame against the actual source video and Read it before locking the constant.** Keep any `HIDDEN` state's `x`/`y`/`scale` identical to BOTTOM (differ only in `opacity`) so opacity-fade scenes don't drift geometrically mid-fade.

---

## Mode changes (the choreography)

Animate with `ease: "expo.inOut"` and **kick off 0.15s BEFORE** the new scene's content lands so the face has settled by the time the scene reads. Times are **edited-time** scene starts — they are NOT auto-shifted by `shift()`.

```js
mainTl.set("#face-wrapper", BOTTOM, 0);  // scene 1 starts in BOTTOM, no anim

[
  { t: 6.18,  mode: FULLSCREEN },  // scene 4 needs fullscreen
  { t: 8.43,  mode: BOTTOM     },  // scene 5 back to bottom-half
  { t: 12.38, mode: FULLSCREEN },
  { t: 15.43, mode: BOTTOM     },
].forEach(({ t, mode }) => {
  mainTl.to("#face-wrapper", { ...mode, duration: MODE_DUR, ease: "expo.inOut" }, t - 0.15);
});
```

A face that snaps modes instantly is the single most jarring frame in a vertical. Always interpolate.

### Hero transitions — three things at once (may-shorts-18 lesson)

A bare 0.15s pre-roll + 0.32s `expo.inOut` on just the face wrapper reads as rigid: the outgoing scene's panels are still fully opaque behind the morphing face, so the eye sees two things fighting instead of a crossfade. For any **hero** scene-to-scene mode change (especially BOTTOM ↔ FULLSCREEN), do all three:

1. Extend that transition's duration to **0.45–0.55s** (not the default 0.32s).
2. Start it **0.25–0.30s** before the new scene's `data-start` (not the default 0.15s).
3. **Fade + blur the outgoing scene's panel wrapper** to `opacity: 0, filter: blur(6px)` over 0.20–0.25s, starting 0.25s before scene end.

Promote the mode array to per-entry `dur` so one transition can run longer than the others:

```js
[ { t: 2.06, mode: FULLSCREEN, dur: 0.50 },
  { t: 3.71, mode: HIDDEN,     dur: 0.32 }, ... ]
  .forEach(({ t, mode, dur }) =>
    mainTl.to("#face-wrapper", { ...mode, duration: dur, ease: "expo.inOut" }, t));
```

Three simultaneous changes = "a real editor edited this." Any one alone = rigid.

---

## Face grading (every short, no exceptions)

```css
#face-video {
  filter: contrast(1.08) saturate(1.08) brightness(0.97);
}
```

Plus two things that turn a still cutout into a character:

```js
// Ken Burns — subtle 1.00 -> 1.025 zoom over the full duration. Perceptible "camera" motion.
mainTl.to("#face-video", { scale: 1.025, duration: <DUR>, ease: "none" }, 0);
```

```css
/* Side vignette INSIDE the wrapper so it scales in both modes — the face sinks
   into the surrounding navy instead of butting a razor edge. */
#face-wrapper::after {
  content: ""; position: absolute; inset: 0; pointer-events: none;
  background: radial-gradient(ellipse at center,
    transparent 55%, rgba(7,18,28,0.35) 85%, rgba(7,18,28,0.7) 100%);
}
```

---

## Seam treatment (required for bottom-half scenes)

A navy→transparent gradient band (60–100px) at y=960 plus a 2px accent scan line with soft glow. Draw it AFTER the face so it sits on top; full-screen scenes cover it when they take over. Razor-sharp y=960 cuts are the #2 tell for AI-edited content (after flat backgrounds). Lives in its own `compositions/seam-treatment.html` on `track-index=5`, full duration.

---

## Slam/stamp timing — reveal logic beats word-sync (may-shorts-18 lesson)

A SLAM/STAMP overlay (KILLED, DEAD, STOP) lands **after** its target text is fully visible, not during the spoken word. In may-shorts-18 v1, KILLED fired at local 0.46s while its target CHATGPT didn't appear until 0.66s — viewers saw "Claude … KILLED" with no visible target and the joke collapsed.

**Rule:** `stamp_t ≥ target-text-visible_t + 0.10–0.25s`, where "visible" is the END of the target's entrance animation, not its start. Word-sync is a guideline; visual reveal order is the constraint. (This is rule #11 in the SKILL.md checklist.)

---

## Data-feel beats beat decoration mid-video (may-shorts-18 lesson)

For scenes 3–5 of a 15–20s short (the middle grind where attention drops hardest), lean on visuals that read as **information** — bar races, stat grids with counting numbers, heatmaps, sparklines, dashboard chrome with telemetry ticking, pain-point grids flashing red in sequence. may-shorts-18 v1's radar-rings + terminal-chip combo was functional but decorative ("bland"); v2 replaced it with a 3×3 pain-point grid lighting up red-orange in sequence + a sparkline stroking in with a YOU-ARE-HERE marker — same time budget, far higher engagement.

**Rule:** pure typography-plus-icon scenes feel like slides; data-feel scenes feel like evidence. When a middle scene feels bland, swap decoration for something that reads as information. Recipes in `references/scenes.md` (data/proof section).

---

## Timeline note — anchor form

may-shorts-19 pads with `mainTl.set({}, {}, <DUR>)`; new code standardizes on the MOTION_PHILOSOPHY Law #11 form `mainTl.to({}, { duration: <DUR> }, 0)`. Both keep `tl.duration()` ≥ `data-duration` and kill the black-frame flash — either is valid; prefer Law #11 in new builds.

Reference: read `video-projects/may-shorts-19/index.html` + a `compositions/scene*.html` before authoring a new face-cam short. Captions live in `references/captions.md`; backgrounds in `references/ambient-audio.md`; transitions in `references/transitions.md`.
