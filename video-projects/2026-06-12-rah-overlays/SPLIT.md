# RAH Overlays — Split & Ritual (Track B, Linear V2)

Master: `/Users/andydepp/Projects/OperatorOS/videos/2026-06-26-reading-ai-output-as-html-claude-artifacts/Exports/RAH_main V2 .mp4`
1920×1080 · 29.97 (30000/1001) · 409.749s (6:49.7). **Never re-encoded until the final composite bake.**

Authority: `boundaries.json` (pinned to whisper word onsets, frame-snapped). Word dump for cue pinning: `.work/words.tsv`.
Full beat-map + overlay concepts: `/Users/andydepp/.claude/plans/brainstorm-the-animation-for-logical-lynx.md` (approved 2026-06-11).

| Part | Window | Dur | What rides on it |
|---|---|---|---|
| P01 p01-hook | 0:00.00–0:56.99 | 57.0s | 2,000-words counter · Karpathy tease · APPROVED·UNREAD stamp · wall-chip stack |
| P02 p02-doors | 0:56.99–1:29.09 | 32.1s | **TAKEOVER:** READ HARDER + SUMMARIZE stations |
| P03 p03-the-turn | 1:29.09–2:12.43 | 43.3s | Karpathy reveal · pull-quote · prompt pill #1 · corner tags |
| P04 p04-lives | 2:12.43–2:35.49 | 23.1s | panel hairline + rule-of-three pills |
| P05 p05-ladder | 2:35.49–3:28.61 | 53.1s | pills #2/#3 · jargon chip · 3-dot ladder rail |
| P06 p06-cost | 3:28.61–4:22.43 | 53.8s | rule card · price underline · 5–15× callout · DeepSeek lower-third |
| P07 p07-smallest | 4:22.43–4:58.63 | 36.2s | step ticker · prompt pill #4 |
| P08 p08-system | 4:58.63–5:41.31 | 42.7s | pill #5 + skill compression · stats underline · token meters |
| P09 p09-thesis | 5:41.31–6:12.37 | 31.1s | **TAKEOVER:** the reflow (same words, new shape) |
| P10 p10-bookend | 6:12.37–6:49.74 | 37.4s | revalued counter · model-name catch · final pill · end-screen card |

## Hard rules (Track B + Lane A)

- Each part is **self-contained** (`parts/<slug>/` with own meta/hyperframes/proxy). Never a master assembly.
- 1920×1080 native, transparent canvas, **no backdrop-filter**, no full-frame opaque layers.
- Reference layer = windowed dense-keyframe proxy (with audio) inside `REFERENCE LAYER START…END`; a sibling `<audio src="assets/proxy.mp4">` rides in the same block for Gate-2 VO sync — both stripped at alpha export.
- Proxy local t=0 == master at the part's `start_s`. All cue times in a part are **local** (master_t − start_s).
- Light-touch law over screen-rec spans: one element at a time · corner/edge anchored · entrances ≤0.3s power2.out · no scrims >35% · no continuous ambient motion · pills anchor lower-LEFT where the webcam PIP (bottom-right) is present (rah-n1/n4 spans).
- Law #11 anchor per part: `tl.to({}, { duration: <slot> }, 0)`.

## Alpha-export ritual (per part, after Gates 1–2)

```bash
cd parts/<slug>
# 1. copy index.html → index.alpha.html, delete the REFERENCE LAYER block (never mutate index.html)
# 2. render:
npx hyperframes render -c index.alpha.html --format mov --fps 30000/1001 \
  --output ../../renders/overlays/<slug>.mov     # NO --resolution flag
# 3. Gate 3 — verify:
ffprobe -v error -select_streams v -show_entries stream=pix_fmt,nb_frames <slug>.mov   # yuva444p12le
ffmpeg -ss <t> -i <slug>.mov -vf "alphaextract,format=gray" -frames:v 1 alpha-map.png  # Read the map
```

## Composite (after all parts pass Gate 3)

`.work/build.py` — ffmpeg filtergraph: master + each `<slug>.mov` overlaid at its `start_s`
(`overlay=enable='between(t,START,END)'`, chained). Audio = master's untouched (plus optional SFX mix).
Review MP4 → `renders/RAH-overlaid-draft.mp4`, served on :8080. Final bake `-crf 18` only after full-pass sign-off.

## Open items

- Karpathy PNG is 657×1218 — fine ≤700px display width; if the P03 card needs more, re-capture the post via Playwright at 2× DPR.
- End-screen tail freeze-extension (+10–14s): Andy decides at Gate 2.
- Optional privacy-blur pass in the composite: ask Andy before final bake.
- SFX pass (typewriter ticks, station clacks ~-18dB): Andy call at Gate 2; scan `linear-promo-30s/assets/sfx/` first.
