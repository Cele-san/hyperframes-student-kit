# DESIGN.bakeoff-registers — three set-piece grammars (R1 / R2 / R3)

**Locked 2026-07-17.** Canonized from Andy's blind judging of the OperatorOS frontend
4-way bake-off (4 models × 3 rounds, one-shot, sealed). These three renders won their
rounds and are now **the standard grammars for their beat types** in every OperatorOS
video built in this workspace.

Authority order: this doc sits BESIDE `DESIGN.linear.md` / `DESIGN.linear-v2.md`, not
above them. Linear V2 + the OperatorOS Quiet Register (`_shared/motion/house-style.md`
in OperatorOS) remain the default for cues and diagrams; **these registers own the
set-piece beats** — the kinetic-text hook, the abstract-concept explainer, the data-viz
proof beat. Budget 1–3 set-pieces per video. Canonical deconstruction + full
house-conform mapping tables live in OperatorOS:
`_shared/motion/bakeoff-winner-registers.md` — read that before building; this doc adds
the HyperFrames-specific mechanics.

## The references (verbatim winning one-shots)

| Register | Beat type | Reference | Won by |
|---|---|---|---|
| R1 — Countdown Kinetic | kinetic text / hook | `References/Bakeoff-2026-07-17/r1-kinetic-text-fable5.html` | Fable 5 |
| R2 — Topology Argument | abstract concept | `References/Bakeoff-2026-07-17/r2-abstract-concept-opus48.html` | Opus 4.8 |
| R3 — Live-Chart Story | animated data viz | `References/Bakeoff-2026-07-17/r3-data-viz-fable5.html` | Fable 5 |

These are plain standalone HTML (GSAP-CDN / raw canvas), NOT HyperFrames compositions.
They are style ground truth — open them in a browser to study, but never render them
through the CLI as-is. Build conformed HyperFrames comps per the mechanics below.

## The shared law (why they won)

> **The composition IS the argument.** Form restates thesis; it never decorates it.

- R1: "nobody watches past 10 seconds" → the comp IS ten honest seconds; the words bail
  like viewers.
- R2: "one system replaces a team" → argued by topology (6 nodes/15 chords vs 1 core/0
  links) and rhythm (bursty-with-stalls vs metronome). The punch is subtraction.
- R3: "-42% gone by 10%" → the chart plays itself like a YouTube video; individuals
  fall, not areas shrink.

Discipline carried over from all three: **beat map as a comment before any code**, one
linear "honest driver" tween owning the spine, and a **held poster frame** at the end
(the final frame must work as a still).

## HyperFrames adaptation mechanics (the part this doc exists for)

### 1. Every register build is a registered, seekable timeline

The render pipeline drives comps by **seeking** a registered GSAP timeline — a
free-running rAF loop or `Date.now()` clock renders as a frozen frame. Rules:

- Build ONE master `gsap.timeline({ paused: true })` and register it per the
  `/hyperframes` skill conventions (`window.__timelines[<comp-id>]`).
- No `Math.random()` at animation time (seeded RNG only — R2's `mul32()` pattern),
  no `Date.now()`, no `requestAnimationFrame` state.
- `onUpdate`-driven HUDs (R1's clock, R3's playhead) are fine **only** when the state
  they read is tween-owned (`tl.to(state, {t:10, ease:'none', onUpdate})`) — seeking
  re-fires them correctly. Beware seek-suppressed onUpdate edge cases: derive
  EVERYTHING from the tweened value, never accumulate.

### 2. R2's canvas needs the proxy-driver wrap

The reference is a pure-function renderer — `render(t)` draws the complete frame for
time `t` from scratch. That purity is what makes it portable. Wrap it:

```js
const D = { t: 0 };
const tl = gsap.timeline({ paused: true });
tl.to(D, { t: END, duration: END, ease: 'none',
           onUpdate: () => render(D.t, D.t) });
// register tl as the comp timeline; the CLI seeks it frame-perfectly
```

Keep the exemplar's craft kit intact when porting: `seg(t,a,b,ease)` windows, seeded
`mul32` RNG, band-limited `nz()` noise, the dual-canvas emissive/bloom composite.
Breathing "idle" effects tied to real time (the core's `real` param) become `D.t`-driven.

### 3. Fonts + palette conform (hard, style-gated)

The references intentionally FAIL the OperatorOS style gate (Anton / Inter Tight /
JetBrains Mono via Google Fonts CDN, YouTube-red). Conformed builds must pass:

- **Type:** Geist 800/900 for slam/headline, Geist Mono for HUD/clock/axis — self-hosted
  woff2 (copy from the AIDR project's assets), never `fonts.googleapis.com`.
- **Palette:** Tier-3 tokens. Red `#EF4444` ONLY when the story is loss/cost/burn (both
  R1 and R3 references qualify — retention loss). Otherwise: blossom `#F0A8C2` takes the
  single emphasis slot, cyan `#5BA8D8` the data/secondary. R2's six actor hues re-key to
  cool desaturated cyan cousins; the work-product color = blossom (or amber for cost).
- **Drop:** grain overlays, frame-edge vignettes (banned atmosphere). Keep: R2's bloom,
  R1's camera shake + flash frame, R3's impact pulse — those are emphasis, not texture.
- **Sanctioned exceptions** (this register only, never the default language):
  R1's single `back.out` squash-pop word + post-hard-cut typewriter payoff tag;
  R3's `back.out` stamp + end-dot.

### 4. Recipe cards (condensed — full versions in the OperatorOS doc)

**R1 — Countdown Kinetic** (~10s): honest clock spine (timer + progress bar + live
readout, one `ease:'none'` driver) → staccato one-word carousel, unique signature
entrance per word (clip-rise slam / skew settle / squash pop / blink / scale slam),
throwaway words deliberately small → triple-layer hit (flash frame + giant ghost-outline
numeral + decaying shake) → sentence assembles (blur-stagger) → words drain out in
meaning order → subject word alone re-centers → hard cut at clock-zero → typed payoff
tag, hold.

**R2 — Topology Argument** (~13.6s): write the shape-picking fact first (run
`give-the-idea-a-shape`) → Act 1 problem state: out-of-sync pulses, chatter blips,
bursty work on a visible ledger (countable tiles), camera unease → TURN: subtraction,
in-flight work dies, ~0.9s void → Act 3 solution state: one core, metronomic, symmetric,
camera settles and leans in. Identity continuity: actor hues persist into role stations;
product settles to ONE color.

**R3 — Live-Chart Story** (~13.5s): skin the chart in the data's native medium
(playhead/scrub for video data — find the equivalent) → one `{p:0→100}` driver derives
playhead, clip reveal, counter, and threshold triggers → population as individual dots
that physically fall (`power2.in`, scatter, dim, fade); survivors brighten → impact beat
at the thesis threshold (band flash + shake + counter snap + rotated stamp) → slow
honest second act → end ping + relabel + comparison bracket → headline swap
(masked `yPercent`), hold. Monotone-cubic curve interpolation (no cliff overshoot);
reduced-motion fallback = final poster.

## Pre-flight (before showing Andy)

1. Beat map comment at the top of the comp — written before the code.
2. `npx hyperframes lint` clean; comp listed with correct duration in
   `npx hyperframes compositions`.
3. Seek test: scrub the Studio playhead backwards/forwards — every frame must be
   correct out of order (the R2 wrap and R1/R3 onUpdate rules above).
4. Style gate grep (from the OperatorOS doc) returns empty; reserved-color semantics
   hold (one meaning per color).
5. Final frame works as a still; ≥1s hold.
6. Register taste is cut-specific: **prototype the set-piece against the real cut and
   get Andy's pick before rolling it across the video.**
