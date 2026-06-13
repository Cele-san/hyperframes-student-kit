# LINEAR V2 — Tier 3 Brand Register (cobalt + blossom)

> The Linear register re-keyed onto Andy's Tier 3 brand — cobalt `#152848` + blossom `#F0A8C2` — via the accent-swap rule in `DESIGN.linear.md` §4, extended with a full hue rotation of the dark ramp.
> **Trigger:** this is the **workspace default** for any Linear ask — *"turn this into a Linear design"*, *"Linear V2"*, *"Linear in my brand / my Tier 3"* all land here. (Canonical grayscale V1 only when Andy explicitly asks for the original.) It is a **delta doc**: everything not listed here — the Ten Laws, motion vocabulary, typography, pacing, audio, anti-patterns, checklist — inherits from `DESIGN.linear.md` unchanged. Read both.
> **Reference build:** `video-projects/2026-06-11-ai-thumbnails-intro-linear/` (full 2-min VO-pinned intro; its Studio/render is the ground-truth look).
> Derived 2026-06-11 from the Tier 3 pass on the AI-thumbnails intro.

---

## 1 · The Core Move: hue rotation, not redesign

The Linear look lives in its **luminance relationships** — near-black canvas, barely-lit surfaces, hairline borders two steps up, gray-white type. V2 keeps every one of those relationships intact and rotates the hue axis onto cobalt. No token gets brighter or darker than its canonical counterpart; it only gets *bluer*. If a V2 frame converted to grayscale doesn't match the canonical register, the swap was done wrong.

Blossom enters **only** through the accent slot (`--lin-accent`), which in V2 owns four things and nothing else:

1. **Fill state changes** — stamps, verdict bars, YES cells, pressed rows, STEP fills, progress sweeps, landed tags: blossom background, cobalt text.
2. **Edge glows** — the sanctioned emphasis glow on stations/columns goes blossom (glints do NOT — see below).
3. **Live cursors** — the thin beam caret in inputs and the trailing `_` on mono surfaces. "Cursors are alive" is the one place the brand pulses constantly.
4. **The send flash** — the gray send circle stays cobalt-gray at rest and flashes blossom for ~3 frames on the send beat.

**Never blossom:** headlines, title-card type, body text, pill chrome, borders, station top-edge glints, backgrounds. If blossom appears anywhere it can't be read as a *state change or a living cursor*, it's off-register.

---

## 2 · Color Tokens (full map, canonical → V2)

### Canvases

| Role | Canonical | V2 |
|---|---|---|
| `--lin-bg` canvas | `#08090a` | `#070b16` |
| Code-world / circuit canvas | `#060708` | `#050811` |
| Deepest canvas (collapse beats, open-from-dark) | `#050607` | `#04070e` |
| Vignette inner stop (must match canvas, never `transparent`) | `rgba(8,9,10,0)` etc. | `rgba(7,11,22,0)` / `rgba(5,8,17,0)` / `rgba(4,7,14,0)` |

### Surfaces

| Role | Canonical | V2 |
|---|---|---|
| Panel top (lit edge) | `#15171a` | `#141e33` |
| Station / pill-card top | `#131517` | `#131c30` |
| Modal / ghost-panel top | `#131417` / `#131416` | `#121b2e` |
| Mock-thumb top | `#1a1c1f` | `#19243c` |
| Card top (input close-up) | `#17191c` | `#16213a` |
| Card / mock / surface bottom | `#121417` | `#111a2d` |
| Panel / ghost bottom | `#0c0d0f` | `#0b101c` |
| Wells (search bg, thumb wells, modal bottom) | `#0d0e10` | `#0c111e` |
| Station bottom | `#101214` | `#0f1726` |
| Flat raised card | `#101113` | `#0f1626` |
| `--lin-surface-2` (tag pills) | `#16171a` | `#141f37` |
| Chat bubble | `#1c1e21` | `#1b2742` |
| Gray circle (send, avatars, dots) | `#2c2f33` | `#2a3a5e` |

### Borders / hairlines

| Role | Canonical | V2 |
|---|---|---|
| Station border (strong) | `#3a3e44` | `#36486f` |
| Station inner hairlines, strip borders | `#2a2d31` | `#283755` |
| Pill border | `#2e3136` | `#2c3c5e` |
| `--lin-border` (panels, inputs) | `#23252a` | `#222f4c` |
| Card border | `#26282c` | `#25334f` |
| Modal border | `#232528` | `#222f4a` |
| Faint chrome dividers | `#1d1f23` | `#1c2740` |

### Text (cool-cast, same luminance — still "gray-white", never blossom)

| Role | Canonical | V2 |
|---|---|---|
| `--lin-text` primary | `#e8eaec` | `#e9edf6` |
| Chat text | `#ecedef` | `#edf0f7` |
| Pill text | `#d4d7da` | `#d3dae8` |
| Bright secondary (search text, model pill) | `#c9ccd1` | `#c8d1e3` |
| Typed headline | `#b9bdc2` | `#b8c2d6` |
| `--lin-code-hi` / close icons | `#9aa0a7` / `#9ba0a6` | `#99a5bd` |
| `--lin-text-dim` | `#8a8f98` | `#8995b0` |
| Placeholder | `#6b7076` | `#6a748e` |
| `--lin-code` plain | `#6e747c` | `#6d7894` |
| Ghost labels, rules, dim icons | `#5c6168` | `#5b6580` |

### The accent slot

| Role | Canonical | V2 |
|---|---|---|
| `--lin-fill` state-change bg | `#d9dbdd` | `#f0a8c2` (blossom) |
| Fill text (dark-on-fill) | `#17191c` | `#152848` (cobalt — 7.7:1 on blossom) |
| Send flash | `#caccce` | `#f0a8c2` |
| Live cursors (beam + underscore) | `#e8eaec` / text color | `#f0a8c2` |
| Edge glow | `rgba(255,255,255,0.16–0.22)` | `rgba(240,168,194,0.26–0.35)` — **~1.6× the canonical alpha** (blossom is dimmer than white; the bump matches perceived luminance) |
| Station top-edge glint | `rgba(255,255,255,0.18)` | `rgba(210,226,255,0.18)` — **cool white, NOT blossom.** Glints say "lit surface," not "state change." |

**Foreign content rule.** Full-color photographic/UI content placed in the world (e.g. the AI-slop thumbnails in the reference build) keeps its native color and reads as the alien object. Don't tint it toward the brand — the contrast is the point.

**Data-color reconciliation (Dashboards build).** When V2 is applied to a data-viz build, the `DESIGN.linear.md` *"data is the only color"* extension and the cobalt + blossom system **coexist without collision** — they are three independent color languages governing different layers, never overlapping:

| Layer | Color language | Re-keyed by brand swap? |
|---|---|---|
| Chrome + type (surfaces, borders, all text) | Cobalt axis (full §2 token map) | **Yes** — rotated onto cobalt |
| Interaction accent (fills, edge glows, live cursors, send flash) | Blossom `#f0a8c2`, accent slot only | **Yes** — blossom is the brand accent |
| Data marks + functional status/priority/icon chips | **Canonical semantic hue** — red=bugs/breached, cyan=cycle/effort, purple=IT, yellow=high, green=medium | **No — never re-keyed.** The hue *is* the meaning; rotating it onto cobalt would destroy it. A breached-SLA flame is red in V1, in V2, and in every brand skin. |

The disambiguating test: **blossom** answers *"did the user/system just **act**?"* · **semantic hue** answers *"what **is** this value?"* · **cobalt** is everything else. If a data mark turns up blossom, or a fill turns up red, the layers have crossed — fix it. (Semantic data hue is the same family as the foreign-content rule above: non-brand color that legitimately survives the swap because it carries meaning the brand axis can't.)

---

## 3 · V2-Specific Recipe Changes

### Progress sweep: width-clipped twin labels (difference blend is dead)

The canonical SENDING/GENERATING sweep keeps its label legible with `mix-blend-mode: difference` — which only works against a **white** fill. Difference over blossom produces muddy green. V2 replaces it:

```html
<div class="genrow">                                <!-- position:relative; overflow:hidden -->
  <span class="genlabel genlabel-a">GENERATING</span>   <!-- light copy, under -->
  <span class="genlabel genlabel-b">DONE</span>
  <span class="fill">                                   <!-- the sweep clips its own copies -->
    <span class="genlabel fill-label genlabel-a">GENERATING</span>
    <span class="genlabel fill-label genlabel-b">DONE</span>
  </span>
</div>
```

```css
.fill       { position: absolute; left: 0; top: 0; bottom: 0; width: 0;
              overflow: hidden; background: #f0a8c2; }
.genlabel   { position: absolute; inset: 0; display: flex;
              align-items: center; justify-content: center; color: #e9edf6; }
.fill-label { width: <row inner width>px; color: #152848; }  /* fixed width pins it in place */
.genlabel-b { opacity: 0; }
```

```js
tl.fromTo(sel(".fill"), { width: 0 }, { width: "100%", duration: 2.4, ease: "power1.inOut" }, T);
// label swap hits both copies at once (shared -a/-b classes):
tl.set(sel(".genlabel-a"), { opacity: 0 }, T2);
tl.set(sel(".genlabel-b"), { opacity: 1 }, T2);
```

The cobalt copy lives *inside* the fill at a fixed width, so the sweep's leading edge wipes light→cobalt character by character — same read as the canonical difference trick, no blend math. (Yes, this animates `width` — sanctioned here; the fill is a clip container, not a video element.)

### Contrast anchors

- Blossom `#f0a8c2` on cobalt-dark text `#152848`: **7.7:1** ✓ (any fill/stamp combination clears AA)
- Blossom caret/underscore on V2 canvases: reads clearly; no halo, no glow on cursors
- `#8995b0` dim text on `#0f1726` surfaces: same ratio as the canonical pairing it replaces

---

## 4 · What Does NOT Change

Everything else is `DESIGN.linear.md` verbatim — re-read it, don't quote from memory:

- The Ten Laws, especially #10 (movers blurred / rests sharp) and #3 (two speeds only)
- Motion vocabulary: dolly-past hops with full-frame smear, parked-overhead stations, blurred dives, focus-pulls, directional fall-ons, chat push, typewriters (beam in inputs / underscore on mono)
- Typography: Geist 400/500/600 + Geist Mono 400/500. **No Inter.** Type stays quiet — the brand enters through state changes, never through type stunts.
- Surface genres: product chrome (radii, hairlines, sentence case) vs flow stations (sharp corners, mono uppercase)
- Pacing/beat grid (or VO-pinned grid per the reference build's adaptation), audio grammar, anti-patterns, render-contract rules
- The pre-flight checklist (§11) — with one line amended: *"Zero hue in the frame"* becomes **"Zero hue outside the cobalt axis + the blossom accent slot + semantic data hues on data marks/chips (Dashboards build) + sanctioned foreign content"**.

---

## 5 · Quick Self-Test (before claiming a V2 piece is done)

1. Desaturate a frame — does it match the canonical Linear register? (If luminance drifted, the rotation was done wrong.)
2. Point at every blossom pixel — is each one a fill state change, an edge glow, a live cursor, or the send flash? Anything else is a violation.
3. Are the station glints still cool white?
4. Is all type still gray-white (cool-cast), with zero blossom headlines?
5. Does foreign full-color content (if any) read as the alien object, untinted?
6. **(Data-viz build)** Point at every non-cobalt, non-blossom color — is each one a semantic data mark or a status/priority/icon chip carrying its **canonical** hue (red/cyan/purple/yellow/green), *not* re-keyed to the brand? Blossom is for *actions*, semantic hue is for *values* — if those two ever swap roles, it's off-register.
