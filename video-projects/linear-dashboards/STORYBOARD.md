# Linear — "Introducing Dashboards" Reproduction Spec

Ground truth derived from frame-by-frame study of `References/Linear/linear demo 3.mp4`
(1fps full sweep + luma-curve cut detection + saturated-pixel clustering on 13 key frames).
Source: **1920×960 (2:1) @ 60fps, 44.183s, 2651 frames.** Reproduction: 1920×960 @ 60fps, 44.2s.

## Cut map (luma-verified, frame-exact at 60fps)

Hard cuts (|Δ luma| > 3): **5.100, 9.900, 19.483 (snapped → 19.5), 24.349 (→ 24.35)**.
Rest valleys (luma < 18.5): 24.35–25.13, 29.10–29.83 + 30.87–31.43 (title 2 bracketed by dissolves),
33.98–34.78 + 35.70–36.23 (title 3), 40.90–end (logo). Bars→particles (~15.3) is a smooth pan, NOT a cut.

| # | Comp | Start | End | Dur | Transition out |
|---|---|---|---|---|---|
| 01 | `01-landing-strip` | 0.00 | 5.10 | 5.10 | hard cut |
| 02 | `02-triage-scatter` | 5.10 | 9.90 | 4.80 | hard cut |
| 03 | `03-distribution-bars` | 9.90 | 15.30 | 5.40 | smooth pan/dissolve hand-off |
| 04 | `04-effort-particles` | 15.30 | 19.50 | 4.20 | hard cut |
| 05 | `05-issues-burnup` | 19.50 | 24.35 | 4.85 | fast dissolve to black |
| 06 | `06-title-monitor` | 24.35 | 26.10 | 1.75 | dissolve into next |
| 07 | `07-module-cascade` | 26.10 | 29.10 | 3.00 | dissolve to black |
| 08 | `08-title-layouts` | 29.10 | 31.40 | 2.30 | dissolve into next |
| 09 | `09-layout-customize` | 31.40 | 34.00 | 2.60 | dissolve to black |
| 10 | `10-title-drill` | 34.00 | 36.20 | 2.20 | dissolve into next |
| 11 | `11-sla-drilldown` | 36.20 | 40.90 | 4.70 | recede + fade to black |
| 12 | `12-logo-outro` | 40.90 | 44.20 | 3.30 | none — ends on logo |

All starts ×60 are integer frames. Beat grid: source cuts are NOT on a clean BPM —
match the source cut times exactly; internal micro-hits land on 0.25s subdivisions
relative to each beat's start (declared per comp).

## Sampled palette (hot = 95th-pct-luma core, mid = median of saturated cluster)

**Canvas is pure black `#000000`–`#080808` everywhere** (blacker than V1's `#08090a`).
Surfaces are barely-lit panels ≈ `#0c0d10`–`#141519` with hairlines ≈ `#222428`.
**Type: titles/logo `#f8f8f8` near-white** (brighter than V1's `#c7cacd` title law — deliberate here);
headers `#e8e8e8`; dim labels `#787878`–`#b8b8b8`.

| Data element | Hot core | Mid/falloff |
|---|---|---|
| Open: indigo trim-path strips | `#6b79ea` | `#393fad` |
| Issue-board status dots (depth, beat 01) | `#ff6134` (orange), `#6160dc` (indigo) | — |
| Triage scatter red | `#dd0327` / `#d80d45` | `#8a030b` |
| Cycle bars cyan | `#50caf0` / `#4db5dd` | `#255d77` |
| Bug bars red | `#f7545e` / `#eb515e` | `#a1303a` |
| Particles (beat 04) | teal `#7ff4ee`, yellow `#ebe373`, orange `#ba714e`, green `#588949` | dim variants ~45% |
| Stacked-segment bars (beat 05) | indigo `#818cf1`, cyan `#74fcff`, blue `#80a1f7`, red `#f08085`, green `#63b89e`, purple `#725aa6` | ~55% luma |
| Burn-up area layers | edge `#5151c7`, fill `#313399`→`#4d5295` | cyan accent `#47b3c3` |
| Priority scatter (beat 09) | green `#70bf60`, teal `#51a5a7`, orange `#e15c38`, yellow `#b5a355` | — |
| Module icon chips (beat 07) | orange `#996c47`, green (bug), indigo `#393d71`+ | chip bg = dark rounded square |
| SLA purple stacked bars (beat 11) | `#8a7fd6`-ish (dim in frame; verify in build) | — |

Andy's pasted storyboard hexes (#3B82F6 / #EF4444 / #10B981 / #A855F7) are Tailwind guesses — do not use.

## Per-beat content spec

### 01 — Landing-strip open (0–5.10)
Dark 3D world, slow L→R camera pan. Low-left: a chart plane at raking angle ("landing strip") —
timeline/Gantt-like rows whose gridlines ignite as **indigo trim-path light strips** tracing on
sequentially (hot `#6b79ea` core, bloom falloff); faint month label "Feb" on axis. Right depth:
heavily blurred issue-board panel (columns w/ status dots — blue "Done", yellow "In progress",
rows of dim issue text + numbers). "**Introducing Dashboards**" (`#f8f8f8`, Geist 500) luminance-fades
in centered ~2.2–2.6s, holds to cut. Sub-bass boom twin on text arrival (SFX slot only — no music pass).

### 02 — Time-in-triage scatter (5.10–9.90)
Steep-tilt card plane, slow drift. Breadcrumb "Dashboards › Engineering performance" + `⋯` + `☆`.
Card header "Time in triage" / sub "Shown over time". X-axis Week 2…Week 7 (italic-ish dim gray).
**Crimson scatter dots accumulate left→right over the beat** (hot `#dd0327` core + glow, distance
falloff `#8a030b`), rising trend, ~120+ dots by end. Below: summary strip "Issue count" + per-week
values (23, 28, …). Heavy DoF: card razor-sharp center, edges blurred.

### 03 — Distribution bars (9.90–15.30)
Two cards over black, camera glides right across them. Left: "Cycle distribution effort" /
"Issue effort sliced by assignee for this cycle" — **cyan neon rod bars** (thin rounded rods,
hot `#50caf0`, glow) descending heights, **avatar circles as x-axis**, dim y ticks (8/6/4).
Right: "Bug distribution" / "Issue count sliced by assignee" — red rods (`#f7545e`).
~13.5s: **tooltip pill** slides up over a red bar: dark pill, red square swatch, "Issue count  268",
drop shadow. Far depth above: blurred table w/ colored project icons. Soft pan/dissolve out.

### 04 — Effort & priority particles (15.30–19.50)
Wide flat-ish view, slow tracking. Top metric cards: "Project effort ~2,109" / second metric "~722".
Body: 4 column groups — "Small redesign", "Customer requests", "Website polishing",
"Website navigation update" — **multi-hue glowing dot clusters** (teal/yellow/orange/green/white)
arranged in loose priority rows, pulsing subtly in luminosity. Hard cut out.

### 05 — Issues created + burn-up (19.50–24.35)
Left card "Issues created": **stacked multi-hue segment rod bars** (each bar = stacked colored
segments: indigo/cyan/blue/red/green/purple) over day-number x-axis (12, 13, …), grow upward on
entrance. Behind top-right at depth: category table — "Pull requests" ●indigo, "Edit mode" ●teal,
"Papercuts" ●red + count columns (70, 72, …). ~22.3s camera pans right to "Issue count by
burn-up and status": **layered indigo area chart** — glowing top-edge strokes `#5151c7`,
translucent fills `#313399`, smooth bezier mounds, month x-axis, y ticks (100/200). Luma peaks
(brightest demo beat). Fast dissolve to black.

### 06 — Title 1 (24.35–26.10): "Monitor key metrics"
Pure black, centered Geist 500 `#f8f8f8`, pure-opacity luminance fade ≈0.8s, hold, dissolve out.

### 07 — Module cascade (26.10–29.10)
Three overlapping iso cards slide up along Z with offset delays + heavy ease-out, each with a
**colored icon chip** (rounded-square dark chip + colored glyph) and real sub-content:
"Distribution of Effort" (orange bar-chart chip; "Open bugs" section) →
"Bug & Cycle Performance" (green bug chip; "Current open bugs / Priority / No priority / High…") →
"IT requests" (indigo shield chip; "Outstanding SLAs / SLA status / Issue count / Breached 48").
Three offset whoosh twins. Dissolve to black.

### 08 — Title 2 (29.10–31.40): "Build custom layouts"

### 09 — Layout customization (31.40–34.00)
Flat-ish dashboard "Bug & Cycle Performance" (green bug chip): left "Bug resolution time trailing 90d"
— priority-colored scatter columns (orange/yellow/green/cyan clusters above priority icon glyphs),
y ticks 5w/4w/3w/2w/1w/0; center "Median triage time" **big stat "46m"** (`#e8e8e8`, ~64px);
right "Current open bugs" priority table (No priority 8 / High 1 / Medium 9 / Low 14, colored
priority bar icons). **A real arrow cursor drags the scatter card wider; the grid reflows**
("46m" stat shifts position with eased layout move). Snappy UI move SFX twins. Dissolve to black.

### 10 — Title 3 (34.00–36.20): "Drill into any insight"

### 11 — SLA drill-down (36.20–40.90)
"IT requests" dashboard (indigo shield chip), "+ Add insight" ghost button top-right.
Left: "Outstanding SLAs" table — SLA status × Issue count: 🔥 Breached 51 (red flame),
High Risk 4 (orange), Moderate Risk 34 (yellow), Low Risk 5 (gray). Center/right: big stats
"Issues in Triage **29**", "Unassigned accepted **27**", "Completed this week **52**".
Below: "IT request volume over time and by source" — purple stacked bars; "Lead time by priority".
Cursor moves to **Moderate Risk row → hover highlight → click** → right side expands into
"**34 issues**" list view: rows reveal top-to-bottom (~0.06s stagger): priority glyph + ID
(SEC-3590, SEC-3514, INF-158, INF-3484, INF-9616, INF-3946, DEV-3988, DEV-9555, DEV-3957,
DEV-3958, APP-3530, APP-3551, APP-3954, APP-3953, SLA-3543…) + status circle + title
("Restrict access to admin routes behind VPN-o…", "Validate expired credentials cleanup process",
"Audit service account usage across enviro…", "Patch SSL certificates nearing expiration th…",
"Reduce timeout errors from edge proxy layer", "Align DNS TTL settings for consistency acr…",
"Address pipeline skips due to hydration flag fa…", "Re-enable test matrix after instability on arm6…",
"Increase retention window for CI build ar…", "Remove deprecated scripts from deploy auto…",
"Roadmap not displaying in custom view", "Stroke missing on milestone indicator in group…", …)
+ 🔥 duration chips (7d, 5d, 2d 11h, 2d 21h, 7d, 2d 16h…) + avatars. Then world recedes into
blur/black. Click SFX twin + whoosh on expansion.

### 12 — Logo outro (40.90–44.20)
Linear lockup (circle mark w/ diagonal stripe cuts toward lower-left + "Linear" wordmark),
centered, `#f8f8f8`, luminance fade-in ≈1s, dead-still hold. **Ends on the logo. No fade-out.**

## New-technique recipes (to encode in DESIGN.linear.md after sign-off)

1. **Data is the only color** — chrome/type gray; saturated hue only in data marks + semantic icons.
2. **Neon data marks** — layered box-shadow glow stacks (hot core ≤2px, 6px bloom, 18px halo).
3. **Rod bars** — thin rounded light-rods + avatar axes (not filled rects).
4. **Stacked multi-hue segments**, **layered glowing area chart**.
5. **Data populates on the beat** — seeded-PRNG scatter accumulation, rod growth, area morph.
6. **Trim-path light strips** — SVG `stroke-dashoffset` traces (shader-safe).
7. **Tooltip-pill microbeat** (swatch + label + value).
8. **Cursor as protagonist** — hover → row highlight → click → drill-down; top-to-bottom row reveal.
9. **Colored icon chips** + flame/priority glyph iconography.
10. **Big-stat typography**.
11. **2:1 canvas, 60fps drift cam** — gentler glides vs V1 station hops; dissolves bracket rests.
12. **Titles/logo at `#f8f8f8`** (vs V1 `#c7cacd`) — register reconciliation needed.

## Determinism + render-contract notes

Seeded PRNG (mulberry32) for all scatter/particle layouts — no `Math.random()`.
No `transparent` keyword in gradients (use `rgba(0,0,0,0)`); no full-screen linear gradients.
Glow via box-shadow/filter only. Every comp ends with Law #11 anchor `tl.to({}, {duration: SLOT}, 0)`.
All tween end-times snap to 1/60.
