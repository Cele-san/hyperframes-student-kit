# DESIGN — AIDR abstract cutaways

Six full-frame 1920×1080 idea-shape cutaways for "AI edited my video in real DaVinci Resolve"
(OperatorOS video 2026-06-30). Dropped on V2 of `AIDR v498` in Resolve via `insert_cutaways.py`.
Register = Andy's Claude-content house style (dark canvas + blossom hero accent), harmonizing
with the magenta room lighting of the A-roll.

## Style Prompt

Quiet, precise, dark-console motion diagrams. A near-black cobalt stage with a faint grid,
one blossom-pink accent that always marks the mover or the payoff, chrome-white type, and
mono timecode data. Every beat is one idea with one shape and one transformation — measured
pacing, holds on the before-state, no decorative flourish. Feels like instrumentation, not
a trailer.

## Colors

| Hex | Role |
|---|---|
| `#050b13` | canvas (near-black cobalt) |
| `#152848` | cobalt — structure fills (cards, segments, blocks) |
| `#2a4270` | cobalt edge — borders, rules, ticks |
| `#F0A8C2` | blossom — THE accent: mover, match, payoff glow (one meaning: "alive/kept/yours") |
| `#F2F5F8` | chrome white — primary type |
| `#5a7194` | dim slate — secondary labels, kickers, ruler labels |
| `#8a4a5a` / `#4a2333` | debris rose — rejected/cut material (dies, falls away) |

## Typography

- **Inter** — labels, captions, block text (400/500/700). NOT DM Sans (not auto-embeddable).
- **JetBrains Mono** — timecodes, counters, data tags, kickers (400/600).

## Motion

- Entrances 0.5–0.7s, `power2.out`; core moves `power2.inOut`; exits/falls `power2.in`.
- Hold the before-state ~1.3–1.5s before the transformation starts.
- ONE mover at a time; dim the past; blossom marks where the eye should be.
- Every part ends on a held, glowing end-state (≥1.5s) — these hard-cut back to A-roll/screen-rec.
- Seek-safe: hidden states via `tl.set(..., 0)` + `tl.to(...)`, never bare `.from()` for late elements.
- Deterministic: harmonic hash only, no `Math.random()`/`Date.now()`, finite repeats only.

## What NOT to Do

- No chrome-gradient trailer type, no orchestral-slam energy, no back/elastic/bounce eases.
- No second accent color; red/rose is ONLY for debris that dies.
- No kinetic type substituting for the shape — the shape carries the idea, type annotates it.
- No `backdrop-filter`, no full-frame linear gradients (H.264 banding).
- No infographic dumps — one shape per part.

## Parts (shape → slot)

| Part | Shape | Slot on AIDR v498 |
|---|---|---|
| `b0-twofates` | one video, two fates (monolith vs 162 clips) | 0:53.4 Sand gap, ~12s |
| `b3-wordrain` | word rain → addressed order (real C2288 timestamps) | ~3:17.7 intercut, ~8s |
| `b3-cutter` | traveling cutter (real debris classes) | ~3:39.3 "you give it two things", ~14s |
| `b3-tower` | block tower 13:16→8:17 (real runtime math) | lead-in to 4:03.5, ~9s |
| `b5-relay` | two-lane junior/senior relay | ~5:16 "junior editor in your pocket", ~10s |
| `b7-asymptote` | rising ceiling (never hits 100) | ~7:25 "80 percent of the way", ~8s |
