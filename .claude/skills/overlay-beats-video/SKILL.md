---
name: overlay-beats-video
description: Build and iterate a multi-beat HyperFrames overlay package that drops on V2 over a separately-rendered A-roll for a long-form YouTube video. Use when Andy says "build the overlay beats", "deliver hyperframes for [video]", "I need motion graphics for [N] beats", "start the overlay package", or when the deliverable is N independent 1920x1080 compositions timed against a locked A-roll cut sheet. Encodes the production-company playbook (11 beats, 4:34 cut, cobalt+blossom register) — full visual identity, 5-phase composition pattern, anti-generic moves, verification workflow, and delivery checklist.
---

# Multi-Beat Overlay Video (HyperFrames over A-roll)

Overlay package = N independent 1920x1080 compositions, each ~5-72s, that drop on V2 over a locked A-roll cut in Resolve. The A-roll is rendered separately by another team member (Brandon does stage 07-09). Your job is the V2 deliverable: one MP4 per beat in `OperatorOS/videos/<slug>/animations/beat-<NN>-<name>.mp4`.

Distilled from the 11-beat delivery for "I Turned Claude Into My Production Company" (May 2026). Apply on every new multi-beat package.

**Always invoke `/hyperframes` first.** This skill sits on top of it. Framework rules (`data-*` attributes, `window.__timelines`, composition structure, no `Math.random()`/`Date.now()`) are non-negotiable.

## When this skill fires

- "Build the overlay beats for [video]"
- "Deliver hyperframes for [video name]"
- "Start the overlay package for [video]"
- "I need motion graphics for [N] beats of [video]"
- Any deliverable that's N independent compositions timed against an externally-rendered A-roll
- Iterating on an existing beat (a single beat redesign also fires this skill — visual identity must stay locked)

## Pre-flight checks (run before writing any HTML)

1. **Cut-sheet config exists** — locate the locked A-roll timing. Typically `OperatorOS/videos/<video-slug>/06-cut-sheet/aroll-assembly-config.json` or similar. This gives you the actual slot duration per beat, not the motion-brief estimates.
2. **Per-beat concept docs OR script text** — each beat needs a brief. If concept docs are missing, pull from `03-script/a-roll-script-v<N>.md` for the spoken text and invent the narrative arc.
3. **Brand register confirmed** — default to the Claude Cowork register (below) unless Andy names a different brand. Never proceed with default `#3b82f6` or generic colors.
4. **Animations folder exists** — confirm `OperatorOS/videos/<slug>/animations/` is the delivery target.

## Project structure

```
video-projects/YYYY-MM-DD-<slug>/
├── index.html                   # master comp stitching all N beats
├── meta.json                    # id, name, dimensions (1920x1080), fps (30)
├── hyperframes.json             # CLI config
├── compositions/
│   ├── b01-<beat-slug>.html    # one file per beat, no shared sub-comp unless reused
│   ├── b02-<beat-slug>.html
│   └── ...
├── assets/
│   ├── brand-tokens.css         # palette + 4 fonts as CSS vars
│   ├── scout-thumbs/            # YouTube outlier thumbnails (if needed for proof)
│   └── ...
└── renders/                     # drafts + final, gitignored
```

Master `index.html` wires every beat with `data-composition-src`, `data-start`, `data-duration`, `data-track-index` (one track per beat). Placeholder slots for beats not yet built keep lint clean:

```html
<div id="slot-bNN" class="clip placeholder"
     data-start="<seconds>" data-duration="<seconds>" data-track-index="<N>">
  <span>// BNN · <NAME> · PLACEHOLDER</span>
</div>
```

## Brand discipline — Claude Cowork register

Encoded in `assets/brand-tokens.css`. Use ONLY these.

- **Palette**:
  - `--cobalt-deep: #0a1626` — primary canvas
  - `--cobalt-lift: #152848` — panels, cards
  - `--blossom: #f0a8c2` — every accent, glow, highlight
  - `--snow: #f2f5f8` — body text (full opacity), `0.65-0.85` opacity for secondary
- **Fonts** (Google CDN, no Inter fallback):
  - `Orbitron` 800/900 — impact titles, big numbers, stage labels
  - `Rajdhani` 500/700 — mid-weight body, definitions
  - `JetBrains Mono` — eyebrows, terminal lines, mono labels (use ALL-CAPS + wide letter-spacing)
  - `Bebas Neue` — high-impact alternative for titles
- **Em-dash sweep**: zero em-dashes (`—`) or en-dashes (`–`) anywhere in user-facing strings. Middle-dot ` · ` is the ONLY separator.
- **Atmosphere recipe (every shot, no exceptions)**:
  - Hex grid background `0.04` opacity (three layered 60deg gradients)
  - 12 ambient particles, seeded positions, blossom color with glow shadow
  - Scanline cycle 22-46s (single sweep, NO `repeat` — that doubles duration)
  - 60% vignette via radial-gradient
  - Subtle grain overlay (`mix-blend-mode: overlay`, opacity 0.04)
- **Coordination-layer ribbon**: shared blossom path-draw symbol — visual continuity across beats is load-bearing. The pipeline map (11-stage S-curve) is the spine asset; it's a callback symbol that should recur.

## The 5-phase composition pattern (for hero beats 20-50s)

| Phase | Time share | Purpose |
|---|---|---|
| 1 — Setup | 15-25% | Eyebrow + title + initial visual. Establish the topic. |
| 2 — Contrast/expansion | 15-25% | Second beat that pulls against or extends Phase 1 (e.g., "studio scale" → "indie scale") |
| 3 — Interrupt | 5-10% | Hard pivot — pause icon, flash + glitch slam, or scale-pop. Earns the next phase. |
| 4 — Expansion | 25-35% | The biggest beat — proof artifacts, callbacks, multi-state visual, biggest density |
| 5 — Stamp | 15-20% | Final punch + stamp/seal/signature. Land the line. |

Phase transitions: opacity fade-out (Phase N) + Y-offset stagger-in (Phase N+1). NEVER hard cuts. Each phase gets ~8-12s for a 50s beat.

For short beats (5-15s) collapse to 2-3 phases.

## Anti-generic moves (LOAD-BEARING — read every iteration)

When a beat feels "boring/generic", it's almost always one of these. The fixes are concrete:

1. **Concrete numbers over abstract labels** — "23 PEOPLE · 4 DEPARTMENTS · 1 PRODUCTION OFFICE" beats "a production studio has multiple departments". Use real headcounts, real durations, real costs.
2. **Hierarchy over rows** — org charts, S-curves, vertical stacks, layered cards beat 5 identical cards in a row. Symmetry kills.
3. **Real proof artifacts over text labels** — mini script with strikethrough beats "stages I edit". Real YouTube thumbnails beat "I pick the thumbnail". REC TAKE 04 film frame beats "I do filming". Show, don't tell.
4. **Visual rhyme between phases** — stat strips that mirror across phases (studio `23·4·1` ↔ indie `1·1·11`) create earned contrast and reward attention.
5. **Stamps/seals as punctuation** — HUMAN wax seal, CHECKMARK, signature line, polaroid — give the punchline visual weight. Rotate them off-axis (-12°) so they feel hand-applied.
6. **Scale contrast** — a big org chart and a small terminal window should feel BIG-vs-SMALL. Don't make Phase 1 and Phase 2 visuals the same size.
7. **Specificity wins** — real tab names (`production-bible.md`, `oda · agent`), real outlier video titles, real channel names, real stage labels. Generic "DASHBOARD" reads boring; specific `claude · production-company` reads earned.
8. **Break symmetry deliberately** — rotate stamps off-axis, offset thumbnail stacks, vary card sizes, kick the showrunner card bigger than the dept leads.

Source the real data — use `vidIQ` MCP for outlier thumbnails (`i.ytimg.com/vi/<id>/maxresdefault.jpg`), real screen recordings for tab layouts.

## GSAP timeline contract

```js
window.__timelines = window.__timelines || {};
(() => {
  const tl = gsap.timeline({ paused: true });
  const DUR = 50; // MUST match data-duration

  // Atmosphere — scanline drift (NO repeat:1, that doubles duration past slot)
  tl.to("#root .atm-scan", { backgroundPosition: "0% 480%", duration: 46, ease: "none" }, 0);

  // Particles drift (finite repeats only)
  document.querySelectorAll('#root .particle').forEach((p, i) => {
    tl.to(p, {
      x: (i % 2 === 0 ? 22 : -22),
      y: (i % 3 === 0 ? -16 : 14),
      duration: 8 + (i % 4),
      ease: "sine.inOut",
      repeat: 2, yoyo: true,
    }, 0);
  });

  // Phase 1 tweens at 0.3-10.4s ...
  // Phase 2 tweens at 10.5-21.0s ...
  // ...

  // Law #11 anchor — pad timeline to slot duration so player doesn't truncate
  tl.to({}, { duration: DUR }, 0);

  window.__timelines["<composition-id>"] = tl;
})();
```

**Eases**:
- `back.out(1.5-1.7)` — hero elements snapping in
- `back.out(2.0-2.2)` — high-impact pop (stamps, seals)
- `power3.out` — supporting reveal, headlines
- `power2.out` — eyebrows, small elements, exits
- `power2.in` — exit fades
- `sine.inOut` — ambient drift, glow pulses, yoyo cycles
- `steps(1)` — cursor blink, glitch flicker, frame holds

**Duration math**: tween with `repeat: N` + `yoyo: true` runs `(N+1) * duration`. Always sum up and verify total ≤ slot. If a scanline drift is 22s with `repeat: 1` it's 44s total. Use a single 46s sweep instead.

## CSS scoping pattern (avoid lint warning)

Use an explicit `#<root-id>` prefix on every selector to avoid `composition_self_attribute_selector`:

```css
/* WRONG — selector matches the block's own id, leaks to sibling instances */
[data-composition-id="b09-authority-broaden"] .role-card { ... }

/* RIGHT — explicit root id */
#b09-root .role-card { ... }
```

Apply same prefix in script selectors:

```js
document.querySelectorAll('#b09-root .particle')
```

## Verification workflow (MANDATORY — never skip)

The HyperFrames Studio iframe screenshot tool is unreliable for compositions — `preview_screenshot` returns blank or wrong frames. ALWAYS use the CLI render + ffmpeg + Read tool path.

```bash
cd video-projects/<slug>

# 1. Lint
npx hyperframes lint
# Accept "composition_file_too_large" and "composition_self_attribute_selector"
# warnings if you can't reasonably split. Fix all real errors.

# 2. Draft render
npx hyperframes render --composition compositions/b<NN>-<slug>.html \
  --quality draft --output renders/b<NN>-draft.mp4

# 3. Frame extraction — pick hero moments per phase, plus risky transitions
mkdir -p renders/frames-b<NN>
for t in 3.5 7.0 14.0 17.5 22.5 28.5 32.5 36.5 43.5 47.5; do
  ffmpeg -y -ss $t -i renders/b<NN>-draft.mp4 -frames:v 1 -q:v 2 \
    "renders/frames-b<NN>/t${t}.png" 2>/dev/null
done

# 4. Read EVERY PNG with the Read tool — don't just list filenames.
#    Verify per frame:
#    - Layout: no overflow, no clipping, hero element centered
#    - Type: brand fonts loaded (no Inter fallback), readable size
#    - Color: cobalt canvas, blossom accents, snow text
#    - Atmosphere: hex grid + scanline + particles visible
#    - Strings: zero em-dashes, middle-dot separators
#    - Transitions land cleanly between phases

# 5. Serve drafts for Andy
(lsof -ti:8080 >/dev/null 2>&1 || \
  nohup npx serve renders -p 8080 -n > /tmp/serve.log 2>&1 &)
# Hand Andy: http://localhost:8080/b<NN>-draft.mp4
# NEVER use python -m http.server — no Range support, scrubbing breaks.

# 6. Wait for EXPLICIT sign-off ("looks good", "ship it"). Silence ≠ approval.

# 7. Standard render
npx hyperframes render --composition compositions/b<NN>-<slug>.html \
  --quality standard --output renders/b<NN>.mp4

# 8. Deliver to OperatorOS
cp renders/b<NN>.mp4 \
  /Users/andydepp/Projects/OperatorOS/videos/<slug>/animations/beat-<NN>-<name>.mp4

# 9. Cleanup drafts
rm -f renders/b<NN>-draft*.mp4
rm -rf renders/frames-b<NN>*
```

## Common gotchas (each one bit during the 11-beat delivery)

1. **Timeline duration overrun**: `tl.to(..., { duration: D, repeat: 1, yoyo: true })` runs `2*D`. Scanline at 22s × repeat:1 = 44s — exceeds 31s slot. Use a single 46s drift with no repeat.
2. **Hero text overflow**: long dynamic titles in fixed-width containers wrap unpredictably. Use `max-width` constraints. When Andy says "text too big", apply ~25-30% global type reduction across all phases.
3. **YouTube thumbnails preserved**: use `aspect-ratio: 16/9` on the `.thumb` div, NOT `flex: 1` (causes horizontal crop). Pattern:
   ```css
   .thumb {
     width: 100%;
     aspect-ratio: 16 / 9;
     background-image: url('...');
     background-size: cover;
     background-position: center;
   }
   ```
4. **No `repeat: -1`**: every infinite repeat must be calculated as finite. `repeat: Math.ceil(slotDuration / cycleDuration) - 1`.
5. **No `Math.random()` or `Date.now()`**: hard-code particle positions or use seeded harmonic-sin.
6. **No `gsap.set()` on later-scene elements** at page load — they don't exist yet. Use `tl.set(selector, vars, timePosition)` inside the timeline instead.
7. **Sandbox blocks `~/Desktop` access** — ask Andy to copy files into project `assets/` manually.
8. **Composition file size warning** is acceptable for hero beats >300 lines if the content is genuinely cohesive. Splitting just to satisfy lint adds friction without benefit.
9. **Master `index.html` vs sub-comps**: master uses `data-composition-id` directly in `<body>` (NO `<template>`). Sub-comps use `<template>` + `data-composition-src`. Mixing them breaks rendering.

## Iteration with Andy (communication patterns)

- Short directional feedback is the norm: "text too big", "feels generic", "pull in real X", "at 6 seconds the text doesn't fit". Expect this style.
- **"Boring/generic"** → apply the anti-generic moves. Add specificity (numbers, names, real artifacts), hierarchy (not rows), proof (not labels), stamps (not just text).
- **"Text too big"** → ~25-30% global type reduction across all phases.
- **"Pull in real X"** → use vidIQ MCP for outlier thumbnails, real tab names from Andy's actual workflow, real channel names, real headcounts.
- **Wait for explicit sign-off** before standard renders ("looks good", "ship it", "go ahead"). Silence is NOT approval.
- After standard render: deliver, clean up drafts, summarize what's next. Don't ask permission for cleanup — just do it.

## Reusable patterns from the production-company delivery

These are battle-tested. Steal them.

- **Pipeline map (b06)**: 11-stage S-curve with 4 state labels (`state-1`/`state-3`/`state-4`). Reused in b07/b09/b10 as callback. The visual spine of the video.
- **Coordination-layer ribbon (b04)**: blossom path-draw symbol — recurring callback in b05/b07/b10.
- **Browser-window mockup**: titlebar with 3 dots + tab bar + terminal lines with `· OK` confirmations. Used in b02/b09 indie windows. Tab names matter — use real ones.
- **Org chart hierarchy (b09)**: top tier (1 head, larger card) + connecting SVG lines + 4 second-tier cards with headcounts. Adaptable to any "at scale" beat.
- **Stats strip**: `[big num][small label] · sep · [big num][small label] · sep · [big num][small label]`. Orbitron 900 36px for numbers, JetBrains Mono 11px for labels. Visual rhyme between phases is the point.
- **HUMAN wax seal (b09)**: 230px circle, blossom 4px border, dashed inner ring (10px inset), 3 lines of text, rotated -12°, blossom glow shadow. Adaptable "stamp" graphic — change the words.
- **Mini-pipeline ribbon (b09)**: tiny 11-dot reference strip showing pipeline state. Use when full b06 callback would be redundant but a spine reference helps.
- **Proof card (b09 Phase 4)**: 3 large cards each with `[stage num · label] [MINE badge] [title] [quote] [proof artifact]`. Adaptable structure for any "what I own" / "show the artifacts" beat.

## Delivery checklist

Per beat, before claiming done:

- [ ] `hyperframes lint` returns 0 errors (warnings OK)
- [ ] Draft renders cleanly, no console errors
- [ ] EVERY phase verified via ffmpeg frame + Read tool — at least one frame per phase
- [ ] No text overflow, no element clipping, hero frame readable
- [ ] Brand fonts loaded in render (no Inter fallback)
- [ ] Palette: cobalt canvas + blossom accents + snow text only
- [ ] Atmosphere recipe present: hex grid + scanline + particles + vignette + grain
- [ ] Em-dash sweep clean — zero `—` or `–` in user-facing strings
- [ ] Timeline duration ≤ slot duration (math the repeats)
- [ ] CSS uses `#<root-id>` prefix (not `[data-composition-id="..."]`)
- [ ] Andy explicit sign-off on draft via `localhost:8080` scrub
- [ ] Standard render at `renders/b<NN>.mp4`
- [ ] Delivered to `OperatorOS/videos/<slug>/animations/beat-<NN>-<name>.mp4`
- [ ] Draft files cleaned up (`b<NN>-draft*.mp4`, `frames-b<NN>*`)

When all beats delivered: animations folder has `beat-01-*.mp4` through `beat-NN-*.mp4`, all 1920x1080, ready for Resolve composite handoff.
