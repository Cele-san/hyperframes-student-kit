# Ambient layers & audio reactivity

The background is a **layer, not a color**, and the motion should breathe with the audio. Both are non-negotiable (quality rules #10 and #6).

---

## 1 · ambient-stack-vertical (the minimum floor)

`background: #07121c` flat is a placeholder, not a design. Every short's `ambient-bg.html` carries at least these four, full duration on `track-index=3`:

1. **Radial gradient base** — center lighter than edges by 15–20%.
2. **Animated noise/grain** at 8–12% opacity.
3. **4–8 drifting particles** or grid traces (seeded positions — no `Math.random()`).
4. **Subtle vignette.**

```css
[data-composition-id="ambient-bg"]{position:absolute;inset:0;overflow:hidden;
  background:radial-gradient(ellipse 80% 60% at 50% 38%, #102234 0%, #0a1622 55%, #07121c 100%)}
[data-composition-id="ambient-bg"] .amb-vignette{position:absolute;inset:0;pointer-events:none;
  background:radial-gradient(ellipse at center, transparent 45%, rgba(0,0,0,.55) 100%)}
[data-composition-id="ambient-bg"] .amb-dot{position:absolute;width:6px;height:6px;border-radius:50%;
  background:rgba(55,189,248,.5);box-shadow:0 0 12px rgba(55,189,248,.6)}
```
```js
const SLOT = 18.84, tl = gsap.timeline({ paused: true });
// Seeded particle drift — harmonic-sin hash for "random-looking" deterministic positions.
const stage = document.querySelector('[data-composition-id="ambient-bg"]');
for (let i = 0; i < 6; i++) {
  const d = document.createElement("div"); d.className = "amb-dot";
  const x = 80 + 920 * Math.abs(Math.sin(i * 1.7 + 0.3));     // deterministic
  const y = 200 + 1500 * Math.abs(Math.cos(i * 1.3 + 0.7));
  d.style.left = x + "px"; d.style.top = y + "px"; stage.appendChild(d);
  // finite back-and-forth drift (no repeat:-1) — yoyo a fixed number of times across the slot
  tl.to(d, { y: "-=40", duration: 3, ease: "sine.inOut", yoyo: true, repeat: Math.ceil(SLOT / 6) }, i * .4);
}
tl.to({}, { duration: SLOT }, 0);
window.__timelines["ambient-bg"] = tl;
```

> `repeat:` with a **finite** count + `yoyo` is fine (it's bounded). `repeat: -1` is the banned form — it never resolves and breaks the capture engine.

---

## 2 · control-room-stack (techy variant)

For a HUD / control-room aesthetic, layer the 6-layer stack from `feedback_techy_background_layers.md`:

1. HUD grid masked to the vignette (so it fades at the edges)
2. Circuit traces (thin SVG paths)
3. Pulse nodes at trace junctions (finite glow yoyo)
4. A scan beam sweeping vertically
5. A telemetry ticker (mono numerals updating off a seeded series)
6. Corner mono labels (REC ●, timecode, coordinates)

Keep it on `track-index=3`, full duration, well under the type — it's atmosphere, not the subject.

---

## Audio reactivity

- **Headlines pulse 3–6%** on the beat (keep text subtle so captions stay readable).
- **Backgrounds can go 10–30%** on bass.
- **Use a SEEDED offline analyser** — pre-compute the audio feature track and bake it into the timeline. Do **NOT** use `AnalyserNode` in the render path; real-time audio nodes and `Math.random()` break determinism frame-to-frame.

Extract the feature track with the helper that ships with the gsap skill:

```bash
python3 .claude/skills/gsap/scripts/extract-audio-data.py assets/<name>-edit.mp4 > assets/audio-data.json
```

## 3 · beat-pulse

Drive scale/glow off the precomputed series via a proxy tween's `onUpdate` (deterministic — reads a baked array, never a live node).

```js
// audio-data.json: { fps: 30, amp: [...per-frame 0..1...], bass: [...] }
const DATA = /* fetched at build time and inlined, or read from a <script type="application/json"> */;
const SLOT = 18.84, tl = gsap.timeline({ paused: true });
const head = document.querySelector("[data-composition-id='scene-x'] .headline");
const bg = document.querySelector("[data-composition-id='ambient-bg']");
const proxy = { f: 0 };
tl.to(proxy, { f: DATA.amp.length - 1, duration: SLOT, ease: "none", onUpdate: () => {
  const i = Math.round(proxy.f);
  head.style.transform = "scale(" + (1 + 0.05 * DATA.amp[i]) + ")";    // 5% text pulse
  bg.style.filter = "brightness(" + (1 + 0.22 * DATA.bass[i]) + ")";   // 22% bg pulse on bass
}}, 0);
tl.to({}, { duration: SLOT }, 0);
window.__timelines["beat-pulse"] = tl;
```

Keep text reactivity at 3–6% and background at 10–30% — push text harder and captions start to jitter and lose readability.
