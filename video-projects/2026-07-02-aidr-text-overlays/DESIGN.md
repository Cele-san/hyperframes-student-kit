# AIDR text-overlay package — design register

Track B overlay package over the SHIPPED `AIDR-v5.mp4` (10:34.6, 1920×1080, 29.97fps) from
`OperatorOS/videos/2026-06-30-ai-edited-my-video-in-real-davinci-resolve/04-edit/`.
Ten pure text-animation parts, composited on a NEW video track in Resolve project
`ai-edited-davinci-resolve`. Andy's hand-finished timeline is untouchable — we only add.

## Engine — anime.js v4 via the hyperframes adapter (first production use)

Parts are authored with **anime.js v4** (`vendor/anime.esm.js`) through
`vendor/hyperframes-anime-adapter.js` (from Andy's AnimeJS eval repo). The adapter wraps a
paused anime.js Timeline in a GSAP-seconds facade on `window.__timelines[id]`, so the
stock hyperframes CLI renders it unmodified:

```js
import { createComposition } from '../../vendor/hyperframes-anime-adapter.js';
const { tl } = createComposition('ov-hook', { duration: 8, defaults: { ease: 'out(3)' } });
tl.add('.w1', { opacity: [0, 1], y: [24, 0], duration: 500 }, 0);
```

anime.js quirks (verified against the bundle in the eval repo):
- ease key is `ease:` — `'out(3)'` ≈ power3.out, `'inOut(4)'`; NO bounce/elastic (brand law).
- timeline positions are **ms** numbers, `'+=N'`, or `'<'`.
- `stagger(ms, {grid, from})`, `svg.createDrawable()` + `draw: ['0 0','0 1']`, `utils.round`.
- No SplitText — words are split manually in the DOM.
- Determinism: no `Date.now()`, no unseeded random (incl. `utils.random`).

## Style — Arc4 V3 "Tokyo Midnight" (tokens verbatim from the eval repo `shared/brand.css`)

| Token | Value |
|---|---|
| cobalt | `#152848` |
| card-fill | `rgba(8, 14, 26, 0.66)` |
| blossom (SOLE accent) | `#F0A8C2` |
| chrome (text) | `#F2F5F8` |
| divider | `#243A60` |
| muted | `rgba(242,245,248,0.55)` |
| hero font | Cormorant Garamond italic 600 |
| body font | DM Sans |
| mono font | JetBrains Mono |

Register: quiet editorial glass. Blossom is the only warm accent. **Ease-out only.**
Alpha-safe glass: NO `backdrop-filter` (nothing to blur over transparency) — baked
specular top-edge highlight + `card-fill` plate + blossom rim (`.gw-edge`) or divider rim
(`.gw-inner`); heroes sit on an edgeless radial scrim (`.gw-naked`). Solid-plate scrims,
not blur — blur under H.264 banded on the AnimeJS cue renders (repo commit 3a54d01).

## Part conventions (per fable5-overlays)

```
parts/<slug>/
├── index.html        ← composition + REFERENCE LAYER (proxy) for authoring
├── meta.json         ← {id, name, width:1920, height:1080, fps:30}
├── hyperframes.json
└── assets/
    ├── proxy.mp4     ← dense-keyframe segment of AIDR-v5 for the part's window
    └── fonts/        ← local woff2 (Cormorant 600italic, DM Sans 400/500, JetBrains Mono 400/700)
```

- Root: `<div id="<slug>" data-composition-id="<slug>" data-start="0" data-duration="<D>"
  data-width="1920" data-height="1080">`.
- Reference layer wrapped in `<!-- REFERENCE LAYER START/END -->`; comment records
  `proxy t=0 == AIDR-v5 timecode M:SS.s`. Stripped by `.work/gate3-strip.py` →
  `index.alpha.html` (validates no ref-video/ref-audio/proxy.mp4 residue).
- Overlay layer is fully transparent-canvas-safe: no full-frame bg, no vignette/grain.
- Render (Gate 3): `render -c index.alpha.html --format mov --fps 30` → ProRes 4444 alpha.
- Cues in `.work/cues.json`: `{part, start_s, dur_s, beat, numbers, reserved}` — includes
  the other session's six reserved windows as `reserved: true` no-go entries; placement
  must assert ≥2s clearance.

## The 10 parts

| Part | Cue (final time, transcript-locked) | One idea |
|---|---|---|
| ov-hook | B0 ~0:05 | "An AI edited this video — inside DaVinci Resolve." |
| ov-8090 | B0 ~0:40 (ends < 0:53.4) | AI 80–90% / you own the last 10–20% |
| ov-cutsheet | B1 ~1:20 | THE CUT SHEET → struck through |
| ov-fcpxml | B2 ~2:05 | FCPXML = a timeline any editor can read |
| ov-repo | B2 ~2:50 | repo = free folder of ready-made code (the unplaced STATIC) |
| ov-hours | B5 ~6:00 | 2–4 hours back, every week |
| ov-repetition | B5 tail | HERO: repetition, not originality. |
| ov-permission | B7 ~8:50 | You don't need to code. Taste + direction. |
| ov-thesis | B8 ~9:40 | Enhance, not replace. |
| ov-cta | B9 ~10:10 | Resolve MCP link + comment CTA |

Reserved (ANOTHER SESSION — do not build, clear by ≥2s): b0-twofates 0:53.4+12s ·
b3-wordrain ~3:17.7+8s · b3-cutter ~3:39.3+14s · b3-tower →4:03.5 (9s) · b5-relay ~5:16+10s ·
b7-asymptote ~7:25+8s.

## Motion rules for this package

- Word-by-word carrier reveals (first word slides furthest, tail decays), visual leads
  audio ~0.2s on punchlines. Anchor every reveal to a transcript word onset.
- Type scales on reveal — never a bare centered fade (MOTION_PHILOSOPHY anti-pattern).
- Overlays live lower-third / off-center; Andy's face is the frame — never cover it
  center-frame except ov-repetition + ov-thesis heroes (which own a breathing beat).
- Every timeline anchors its slot: `createComposition(id, {duration: SLOT})` (adapter
  handles Law #11 via the duration anchor).
- Tween end-times snap to 1/30s frame boundaries.
