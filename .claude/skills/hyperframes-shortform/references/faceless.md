# Faceless track — pure motion graphics

No talking head. The type, the data, and the motion carry the whole short. Three formats: **kinetic-typography short**, **listicle vertical**, **quote-card short**. This is the track the old face-cam skill never covered.

When faceless: there's no recording, OR there's a VO-only audio file, OR Andy explicitly wants pure motion graphics over b-roll/music.

---

## The 3-layer scaffold (no face, no seam)

```
index.html (root, 1080x1920, data-composition-id="main")
├── ambient-bg.html   track-index=3  — REQUIRED. Type needs a lit stage, not flat color.
├── scene1…N.html     track-index=1  — kinetic-type / list / quote scenes, back-to-back
├── captions.html     track-index=2  — karaoke when a VO exists; OMIT when on-screen type IS the message
└── <audio> (vo)      track-index=4  — VO or music bed
```

The face and seam layers from the face-cam scaffold are simply dropped. Everything else (ambient-bg, captions, the Law #11 anchor, edited-time timing) is identical.

---

## VO generation

If only a script exists, generate the VO before measuring duration:

```bash
npx hyperframes tts "<script text>" --voice am_adam --output assets/vo.wav
ffprobe -v error -show_entries format=duration -of csv=p=0 assets/vo.wav   # -> data-duration
```

Then transcribe the generated VO for word onsets — **TTS pacing ≠ the script's written rhythm**, so the karaoke captions and beat boundaries must come from the actual audio (see `references/pipeline.md`). Wire the VO as a sibling `<audio data-volume="1">`; add an ambient pad at `data-volume="0.15"` per MOTION_PHILOSOPHY §2.7 if the piece feels dry.

For a **music-only** faceless short (no VO), there are no word timestamps — drive beats off a precomputed seeded audio feature track (`references/ambient-audio.md`, `beat-pulse`), and the on-screen type IS the caption (skip the captions layer).

---

## Pacing: type IS the character

Without a face to hold the frame, the type has to do the work the face did. That means **bigger and bolder** than face-cam overlays:

- Hero words SCALE dramatically (the 8× dolly-through from MOTION_PHILOSOPHY §2.4 reads great in portrait — adapt it vertically).
- Chrome-gradient + halo glow on every headline (MOTION_PHILOSOPHY §2.2), not flat white.
- Word-reveal stagger 0.3–0.4s for narrative reads, 0.5–0.6s for single-word emphasis.
- Honor the **breathing rule**: every ~7–8s of kinetic density, give a 1s rest beat. In a 30s faceless short that's the quote hold or the logo card.
- Still obey the 11 quality rules — payoff ≥1s hold, one jaw-dropper per 5s, motion through full duration, rotate transitions, background is a layer.

### Adapting MOTION_PHILOSOPHY's 16:9 vocabulary to 1080x1920

That doc is deconstructed from a landscape spot. Port the moves, re-aim the axis:

| 16:9 move | 9:16 adaptation |
|---|---|
| Camera dolly through type (grows + fades) | Same — even stronger in portrait; let the word fill the 1080 width and blow past |
| Light-streak whip (horizontal) | Re-aim **vertical** (`whip-up`, `references/transitions.md`) — matches thumb-scroll |
| Perspective grid floor | Keep, but tilt the vanishing point lower; portrait shows more "floor" |
| Wheel + side-panel (L/R panels) | Stack panels **top/bottom** instead — width is the scarce axis in portrait |
| Rule of threes (3 benefits across) | Stack the three **vertically**, one per scroll-beat |

---

## Format: kinetic-typography short

The VO drives word-by-word kinetic type; each beat is one phrase landing hard.

- Open with a `hooks.md` hook (typography-slam or word-by-word-punch).
- Each mid-beat = one phrase: words enter with decaying slide distances, the key word scales + chrome-sweeps, hold the payoff ≥1s.
- Chrome gradient + halo on headlines; per-beat font discipline (a different Google font per "universe") if the script has distinct sections.
- Background carries continuous motion (perspective grid parallax + drifting particles).
- Close with a `loop-back-to-hook` outro so the platform loop is seamless.

## Format: listicle vertical

"N things" — each item is its own scene.

- Hook beat states the promise ("6 skills that actually matter").
- Each item scene: a **counter chip pops** (`1`, `2`, `3…` via `back.out(1.7)`), the item title slams in, a one-line payoff holds ≥1s.
- Use `list-cascade-check` (`references/scenes.md`) when items appear together; use counter chips when they're sequential scenes.
- Keep a persistent progress affordance (a small `3/6` or a filling bar) so the viewer knows how far in they are — it lifts retention through the middle grind.
- CTA recaps or teases the best item, then `loop-back-to-hook`.

## Format: quote-card short

The calmest format — a single quote, held and breathed.

- `stacked-line-reveal` (`references/captions.md`) brings the quote in line by line.
- Attribution slides in 0.2s after the last line rests.
- Ambient drift + a slow vignette breath keep the held frame alive (no dead frames even at rest).
- Holds 2–3s on the full quote — this is the breathing beat, so let it land.
- Optional: a single chrome `shimmer-sweep` across the quote once, mid-hold.

---

Captions in faceless: when a VO exists, karaoke still applies (`references/captions.md`). When the on-screen type IS the message (music-only), skip the caption layer entirely — don't double the words.
