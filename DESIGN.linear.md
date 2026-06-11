# LINEAR — Motion Design Register

> Deconstruction of Linear's **Code Intelligence** 33s product spot (1920×1080, 30fps) — derived from a frame-by-frame study of the source video (`References/Linear/linear demo 2.mp4`).
> **Trigger:** the foundation spec for every Linear build — but the workspace **defaults to V2**: a plain *"turn this into a Linear design"* means this file **plus** the `DESIGN.linear-v2.md` Tier 3 color delta. This file alone (canonical grayscale) only when Andy explicitly asks for the original. Read fully — don't quote from memory.
> **Reference artifact:** `video-projects/linear-code-intelligence/` (the recreation build; its render is the ground-truth look).
> This is a design doc, not a skill. It steers taste; the render contract and authoring mechanics still live in `CLAUDE.md`, `MOTION_PHILOSOPHY.md` (discipline layer), and the `/hyperframes` skill.

---

## 1 · Style Prompt (the master prompt)

Use this paragraph verbatim as the north star when briefing any composition in this register:

> Linear is matte, monochrome, camera-led product cinema. The UI is the hero: real input fields, modals, flow stations, and answer panels floating in a near-black void, shot like hardware — one continuous 3D world the camera dives through, with real depth-of-field (sharp focal plane, lens-blurred far layers), shallow vignette, no grain, no color. Strictly grayscale: light gray circles for send buttons, white fills for pressed states, white edge-glints on station borders — luminance is the only "color." Typography is quiet Geist, gray-white on black; code and station labels are Geist Mono. Motion has two speeds: snappy beat-synced hits (station arrivals, chat-bubble pushes, typewriting with a thin beam caret in inputs and a trailing underscore on mono surfaces) and slow luminance fades (title cards and the logo breathe in over a full second, pure opacity, no scale). Product beats connect through camera moves — fast blurred dives and focus-pulls, never room-to-room cuts; fades bracket the rests. Anything moving fast is motion-blurred: the whole frame smears mid-hop and resolves razor-sharp at rest, and passed surfaces park overhead as blurred foreground depth instead of exiting. Structure: demo sprint → declarative title card → demo sprint → title card → logo, ending dead-still on the lockup with no fade-out. Restraint is the brand: if it glows in color, gradients, or bounces, it isn't Linear.

---

## 2 · Reference Timeline (the recreation spec)

| Time | Beat | What's on screen | Motion engine | Audio | Transition out |
|---|---|---|---|---|---|
| 0–4.4 | **Iso open** | Near-black; a dark panel at a steep cinematic tilt with heavy edge depth-of-field. A bright `*_` seed (asterisk + blinking underscore) sits at the bottom of an **inverted-triangle** asterisk field; headline "Code Intelligence is now available" lives **on the panel, in perspective**; "Ask Linear…" input fades in at the panel's bottom. | Slow continuous camera pull-back (3.5–4s, `power2.out`); headline = plain opacity fade; glyphs bloom **radially outward from the seed** with distance-based delays and distance-based brightness falloff. | Deep ambient synth swells into a rhythmic pulse | **Fast dive into the input** (≤0.3s, blur + scale toward it) |
| 4.4–7.3 | **The question** | Close-up of the same input, low in frame, mild perspective, panel surface above, "Ask Linear" pill button in-world bottom-right. Field starts **empty with a thin beam caret**; types "What happens when an invite link expires?" (~16–20 chars/s). Gray-circle send button — no accent anywhere. | Emerge from the dive's blur; slow settle drift; `steps()` typewriter, beam caret riding the clip edge. | Tick SFX per character over the pulse | **Send beat → blurred dive**: caret vanishes, input clears back to its placeholder (= sent), small camera pull-back, then a heavy motion-blur dive |
| 7.3–16.2 | **Flow stations** | A vertical circuit of 5 sharp-cornered terminal stations over live-typing code at multiple depths: INVITE LINK EXPIRED (hazard-triangle block + REQUEST NEW LINK → action row) → VALIDATE TOKEN (white edge-glow) → TOKEN EXPIRED? (YES/NO; **YES fills white**) → ISSUE NEW TOKEN (glow) → NEW INVITE LINK (**white SENDING sweep → SENT**). Floating mono tags (`InviteTokenValidator` …) near their stations. | **Camera dollies forward past each station** (~1.5s hold + ~0.5s hop): the **whole frame motion-blurs mid-hop** (≈11px peak + slight vertical stretch) and resolves on arrival; the outgoing card grows, defocuses, and **parks overhead** — still peeking into the top of frame at half opacity until the next hop carries it off; incoming sharpens up from 0.92. Background code types on char-by-char with trailing `_` cursors; far columns pre-blurred for depth. | Beat hit ("thud"/"clack") per station arrival | **Focus-pull out** — the world defocuses and drifts up |
| 16.2–21.4 | **The answer** | Two beats. (a) Flat black: typewritten headline "Relevant code pat`_`" (underscore cursor) while the four code-path pills stack beneath — the journey's tags assembling into a list. (b) The full Ask Linear conversation panel in **heavy perspective** (~25° composite tilt, slow drift): dim header label, right-aligned question bubble, 3-line answer, "Relevant code paths:" + pills. | Headline typewriter while the pills **fall onto the list from four different directions** — overlapping motion-blurred flights (one mid-air while another lands), each settling `power3.out`; blur-through focus-pull into the perspective panel, where the last pills land late onto the tilted stack; slow ease-none camera drift. | Track settles into a steady loop | **Soft dissolve** to black title card |
| 21.4–23.2 | **Title card 1** | "Understand product behavior" — centered, pure black, **gray-white** (~80% luminance, never full white). | **Slow luminance fade** — pure opacity over ~1.1s, micro scale-drift only, no scale-from, no slide. | Ambient riser sweep | **Cut** into the modal's slide-up |
| 23.2–28.3 | **Prompt cycle** | Large bottom-anchored "Ask Linear" modal that **extends past the frame bottom**; sentence-case header + hairline divider + close ×. Three queries as **right-aligned chat bubbles**. | Modal **slides up** into place (`power3.out`, no overshoot). **Chat push**: each new bubble rises from below while the old one slides up and clips under the header divider. | Deep bass tone; low swoosh per push | **Cut** into title 2's fade |
| 28.3–30.8 | **Title card 2** | "Answers grounded in your codebase" — same treatment as title 1. | Same slow luminance fade; 0.4s dissolve out. | Synth pad fades; ring-out tail | **Cross-dissolve** into logo |
| 30.8–33.9 | **Logo outro** | Linear mark (solid circle with diagonal stripe cuts toward the lower-left) + "Linear" wordmark, centered on pure black. | **Fade-in only** (~1s, no scale), then dead-still hold. **The piece ends on the logo — no fade-out.** | Final chord echoes into absolute silence | None — ends still |

**Sprint/rest structure.** Two demo sprints, each resolved by a title-card rest, then the logo: `sprint (0–21) → rest (21–23) → sprint (23–28) → rest (28–31) → outro (31–34)`. The sprint earns the rest; the rest names what the sprint just proved.

**Transition grammar.** Product beats live in **one continuous world** and connect through camera moves — fast blurred dives (into a surface, through a send) and focus-pulls (defocus out / sharpen in). True hard cuts are rare and bracket the modal sprint. Fades are reserved for rests: slow fade **into** every title card and the logo, soft dissolve out of demo beats that resolve into a rest. Never cut room-to-room between unrelated product surfaces — the camera always travels.

---

## 3 · The Ten Laws

1. **UI is the hero.** Every scene is a believable product surface (input, modal, flow stations, answer panel) or a declarative title card about it. No abstract object metaphors, no mascots.
2. **Strictly grayscale.** Near-black canvas, gray-white type, gray hairline chrome. The canonical register has **zero hue** — send buttons are light-on-gray circles, state changes are white fills, emphasis is a white edge-glint. Luminance is the only color.
3. **Two speeds only.** Snappy beat-synced hits (0.3–0.6s arrivals, `power2/power3.out` — pressed-in, not bouncy) or slow luminance fades (≥1s, pure opacity). If an element tween sits between the two, push it to one side. (Camera moves — pull-backs, dives, dolly hops, focus-pulls — are exempt: dives 0.25–0.45s `power3.in`, drifts 1.2–4s `power2`/`none`, never overshoot.)
4. **The camera connects, the beat times.** Product beats live in one continuous world joined by dives and focus-pulls; every hit, hop, and swap still lands on the beat grid. Build the beat map before authoring anything.
5. **Title cards are chapter breaks.** One declarative claim, ≤5 words, 2–3s, gray-white centered on pure black, fading in over a full second. They name what the previous sprint proved.
6. **Type is quiet, cursors are alive.** Weights 400–600, gray-white, no kinetic scaling stunts, no tracking stunts. The typewriter is the only type animation — **thin beam caret in inputs, trailing underscore on mono/code surfaces**, never a block.
7. **Sound drives the cut.** Tick per keystroke, clack per station, swoosh per push, riser into rests, ring-out at the end. Every visual hit has an audio twin.
8. **Real UI fidelity, two genres.** Product chrome (inputs, modals, panels): 1px hairlines, 12–24px radii, sentence-case Geist. Flow stations: **sharp corners**, mono uppercase, hazard blocks, white-fill state changes — terminal blueprints, not app cards. If it couldn't ship (or print on a schematic), rebuild it.
9. **Breathe at the end.** Logo fades in over ~1s — opacity only, no scale — then holds dead-still. **The piece ends on the logo; never fade out.** The outro is the longest still moment in the piece.
10. **Movers are blurred; rests are sharp.** This is the single biggest tell of the register. Every fast move carries velocity-matched motion blur: camera hops smear the *entire frame* (~11px peak, clearing `power3.out` on arrival), flying elements carry their own blur that clears on landing, chat bubbles are blurred whenever they're traveling, and passed surfaces park as blurred foreground layers instead of exiting. An element is either at rest and razor-sharp, or in motion and blurred — a fast sharp mover reads as cheap web animation, not cinema. (Title cards and the logo are exempt: rests never blur.)

---

## 4 · Color

| Token | Hex | Role |
|---|---|---|
| `--lin-bg` | `#08090a` | Canvas (near-black; the code world drops to `#060708`; pure `#000` only on title cards + outro) |
| `--lin-surface` | `#101113` | Panels, modals, input fields (gradient to `#17191c` at the top edge for lit surfaces) |
| `--lin-surface-2` | `#16171a` | Raised cards, tag pills, active states |
| `--lin-border` | `#23252a` | 1px hairlines, dividers (`#3a3e44` on flow stations) |
| `--lin-text` | `#e8eaec` | Primary UI type (gray-white — never pure `#fff`) |
| `--lin-title` | `#c7cacd` | Title cards and the logo lockup (~80% luminance — dimmer than UI type) |
| `--lin-text-dim` | `#8a8f98` | Placeholder, labels, secondary copy |
| `--lin-code` | `#6e747c` | Background code, plain tokens (legible texture) |
| `--lin-code-hi` | `#9aa0a7` | Background code, bright tokens (keywords, strings) |
| `--lin-fill` | `#d9dbdd` | White-fill state changes: pressed rows, YES cells, SENDING sweeps, hazard triangles |
| `--lin-accent` | *(none in canonical)* | **Brand-swap slot only.** The reference video is 100% grayscale — no accent anywhere. When adapting to a brand, the accent may take over focus rings, send buttons, status dots; never headline or title-card type. |

**Accent swap rule.** The canonical register ships with **no hue at all**. Re-branding means introducing exactly one accent into UI chrome and nothing else (e.g. "Linear design in my Tier 3" → every surface, border, and text token stays as-is; the accent becomes blossom `#F0A8C2`). If a brand adaptation needs more than that one accent, it isn't a Linear design anymore — pick a different register.

---

## 5 · Typography

```html
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600&family=Geist+Mono:wght@400;500&display=swap" rel="stylesheet">
```

- **Geist** — everything: UI copy, headlines, title cards, body. Weights **400 / 500 / 600 only** — no black weights, no italics.
- **Geist Mono** — code blocks, tag pills, flow-card labels (the ALL-CAPS step cards), keyboard hints.
- **Title cards:** 64–80px, weight 500, letter-spacing `-0.01em`, `--lin-title` (gray-white, dimmer than UI type) on `#000`.
- **UI copy:** 15–18px at 1080p-design scale, weight 400; labels 12–13px weight 500 uppercase in Geist Mono with `+0.06em` tracking.
- **No Inter.** Explicitly rejected — this register has its own voice. No per-beat font rotation (that's the MOTION_PHILOSOPHY launch-video move, not Linear).

**UI surface kit** (the recurring product chrome — two genres, never mixed):

| Surface | Spec |
|---|---|
| Input field | `--lin-surface` gradient, 1px `--lin-border`, radius 14–18px, placeholder in `--lin-text-dim`, **thin 2px beam caret**, icon row right (inline SVG, 1.5px strokes), send = light arrow on a **gray circle** (`#2c2f33`); on send the field **clears back to its placeholder** |
| Flow station | **Sharp corners (radius 0)**, `#131517→#101214` vertical gradient, 1px `#3a3e44` border + 1px white top-edge glint (`inset 0 1px 0 rgba(255,255,255,0.18)`), Geist Mono 500 uppercase `+0.14em`, stacked rows split by hairlines; hazard-triangle icon block for alerts; state changes fill **white** (`--lin-fill` with dark text): pressed action rows, YES cells, SENDING progress sweeps; emphasis stations get a white edge-glow (`0 0 18px rgba(255,255,255,0.16)`) |
| Modal | Large and bottom-anchored — extends past the frame bottom; `--lin-surface` gradient, radius 24px, **sentence-case Geist header** + full-width hairline divider + close × in `--lin-text-dim`, shadow `0 30px 90px rgba(0,0,0,0.6)` |
| Chat bubble | Right-aligned in the modal body, `#1c1e21`, radius 16px, Geist 400, `--lin-text`, max-width ~⅔ of the body, wraps to 2 lines |
| Tag pill | radius 4–6px, 1px border, Geist Mono, `#d4d7da` text on `--lin-surface-2`; floats near code in the 3D world, restates as a flat stacked list at the sprint's resolution |
| Answer panel | `--lin-surface`, dim sentence-case header label, question bubble + answer paragraph + pills; shot in **heavy perspective** (~25° composite tilt) with a slow camera drift |
| Live code texture | Hardcoded fake-code lines, Geist Mono 17–18px, two-tone (`--lin-code` plain / `--lin-code-hi` keywords), **types on char-by-char with a trailing `_`**; far columns pre-blurred (`blur(5px)`, ~50% opacity) for depth-of-field |

---

## 6 · Motion Vocabulary (GSAP recipes)

| Move | What it does | Recipe |
|---|---|---|
| **Typewriter + beam caret** | The signature "ask" moment (inputs) | Deterministic mask: text in an `overflow:hidden; white-space:nowrap; max-width:0` wrap, `tl.to(wrap, { maxWidth: W, duration: chars/20, ease: 'steps(chars)' })`; a sibling 2px beam span rides the clip edge. Blink with **finite** repeats: `tl.to(caret, { opacity: 0, duration: 0.4, ease: 'steps(1)', repeat: N, yoyo: true })` — never `repeat: -1`. Tick SFX on the same cadence. |
| **Underscore typewriter** | Headlines / code surfaces | Same masked recipe at ~14 chars/s with a trailing `_` span (Geist Mono) instead of a beam. Background code uses it per-line at ~25 chars/s with a 0.16s line stagger, the `_` baked into the last line. |
| **Send beat** | The question resolves | Caret hides (`tl.set`) → send circle flashes light for ~3 frames → typed text swaps to the dim placeholder (sent!) → small camera pull-back (`scale 0.965, 0.2s`) → dive. |
| **Velocity-matched motion blur** | The global grammar (Law #10) | Fake it with CSS `filter: blur()` ramps + a slight axis stretch — no SVG directional filters needed (the reference blur reads near-isotropic). Camera hops blur the *whole frame container*: `to { filter: 'blur(11px)', 0.22s, power2.in }` then `to { filter: 'blur(0px)', 0.3s, power3.out }`, paired with `scaleY 1 → 1.045 → 1` on the same curve. Flying elements bake the blur into their entrance/exit tweens (`filter: 'blur(6–14px)'` in the `from`/exit vars, clearing on landing). Blur peaks mid-move, is zero at rest. |
| **Dolly-past station hop** | The flow-circuit journey | Stations stacked vertically (~620px apart) in one world; hop = `tl.to(world, { y: -SPACING*i, duration: 0.5, ease: 'power3.inOut' })` + the full-frame blur ramp above. **Outgoing station parks overhead** — it lags the world and stays in frame as foreground depth: `to { y: '+=160', scale: 1.4, opacity: 0.55, filter: 'blur(13px)', 0.55s power3.out }` (the *next* hop carries it off); incoming sharpens: `from { scale: 0.92, filter: 'blur(8px)', 0.6s power3.out }`. Hold ~1.5s per station; the outer wrapper drifts (`y, ease: 'none'`) the whole time. |
| **Blurred dive** | Entering a deeper environment | Outgoing: `to(scene, { scale: 2.3–2.6, opacity: 0, filter: 'blur(20px)', duration: 0.27–0.3, ease: 'power3.in' })`, aimed at the target (add `y` toward it); incoming **emerges from blur**: `from { filter: 'blur(14–20px)', scale: 1.12–1.15, 0.3–0.4s power3.out }`. |
| **Focus-pull** | Soft hand-off between beats of one sprint | Exit: `to(world, { filter: 'blur(18px)', opacity: 0, y: '-=120', 0.5s power3.in })`; entry settles from `blur(10–12px)` over ~0.4s. Reads as a lens rack, not a cut. |
| **Directional fall-on** | Tag pills / list rows arriving | Multi-element arrivals come from **different directions with overlapping motion-blurred flights** — never a uniform stagger-fade. Per element: `from { x: ±70–340, y: ±30–210, scale: 1.1–1.3, opacity: 0, filter: 'blur(6–14px)', 0.45–0.6s, power3.out }`, start times ~0.15s apart so one is mid-air while another lands. Vary the vector per element (upper-right, hard-right streak, lower-left crossing in front, from below); give one a low blur + short flight so it lands sharp while a neighbor is still a streak. |
| **Chat push** | Queries cycling in the modal | Bubbles absolutely anchored, body `overflow: hidden` clipping at the header divider; CSS rest `y: 70, opacity: 0, filter: blur(8px)` — blurred whenever traveling, sharp only at rest. Out: `to { y: -160, opacity: 0, filter: 'blur(10px)', 0.45s power3.inOut }` (inOut, NOT `power3.in` — the outgoing must start moving at once or it shares the slot with the incoming bubble); in (~0.15s later): `to { y: 0, opacity: 1, filter: 'blur(0px)', 0.5s power3.out }`. Push lands on a beat, swoosh SFX. |
| **Title-card luminance fade** | The chapter-break rest | `tl.from(card, { opacity: 0, duration: 1.1, ease: 'power1.inOut' })` — **pure opacity, no scale-from, no slide** — then micro-drift (`scale → 1.006, ease: 'none'`) through the hold. |
| **Triangle glyph bloom** | The asterisk field | Inverted triangle of `*` rows converging on a bright `*_` seed; per-glyph delay = distance from the seed (`Math.sqrt(x²+row²) * 0.14`, precomputed — deterministic), brightness falls off with distance via per-row colors. `from { opacity: 0, scale: 0.7, 0.45s power2.out }`. |
| **Cinematic pull-back open** | The establishing shot | Stage `perspective: 1400px`; CSS rest = camera END state (`rotateX(23deg) rotateY(-14deg) scale(1.18)`). `fromTo` from steeper/closer (`rotX 30, rotY -24, scale 1.45`) over 3.8s `power2.out` while a black overlay lifts (1.2s). Headline and surfaces live **inside** the tilted group. |
| **White-fill state change** | Pressed rows, YES cells | `tl.set(cell, { backgroundColor: '#d9dbdd', color: '#17191c' })` on the beat — instant, no tween. Pressed action rows do the reverse (arrive light, settle dark ~1s later). |
| **Progress sweep microbeat** | SENDING → SENT | White fill spans the row: `fromTo(fill, { scaleX: 0 }, { scaleX: 1, duration: 0.9, ease: 'power1.inOut', transformOrigin: 'left' })` (label in `mix-blend-mode: difference` survives the sweep), then `tl.set` swap to a light SENT row on the next beat. |
| **Logo outro** | The close | `tl.from(lockup, { opacity: 0, duration: 1.0, ease: 'power2.out' })` — **no scale** — then dead-still hold to the end. **No exit fade; the piece ends on the logo.** |

**Scene anatomy (layer stack, bottom → top):** canvas (`--lin-bg`) → pre-blurred far code (depth) → live-typing near code / glyph texture → product surface(s) → faint vignette (`radial-gradient(ellipse at center, rgba(8,9,10,0) 45–55%, rgba(0,0,0,0.55–0.72) 100%)`, the only "texture" this register allows) → SFX-twin overlays if any. No grain layer. Depth-of-field is faked honestly across **three planes**: far layers carry a static CSS `blur(5px)`, the focal plane is razor-sharp, and passed surfaces park at the frame edge as large blurred foreground layers (~1.4×, `blur(13px)`, half opacity). Transitions rack the whole world's blur.

---

## 7 · Pacing & the Beat Grid

- **Build the beat map first.** Identify the track's BPM, then author everything on the grid: `const B = 60 / BPM;` — every `data-start`, dive, station hop, and bubble push sits at `n * B`, then snaps to a frame boundary (multiples of 1/30 at 30fps).
- **Demo beats:** 2–4s each (Linear breathes more than Infinite's 1.5s average) — but *within* a demo beat, something hits every 0.8–1.2s (a station, a push, a microbeat).
- **Station cadence:** ~1.5s hold + ~0.4s hop per station; never let two stations share a beat. Live code keeps typing through the holds so nothing parks.
- **Title cards:** 2–3s total — ~1.1s luminance fade in, ≥1.2s legible hold.
- **Outro:** 3s+ — ~1s fade-in, then a dead-still hold to the final frame (no fade-out).
- **No dead air >1s** inside sprints; rests are the only sanctioned stillness.

---

## 8 · Audio

Music-forward — the inverse of MOTION_PHILOSOPHY's whisper-pad default:

| Layer | `data-volume` | Role |
|---|---|---|
| Music (rhythmic synth/electronic, steady BPM) | `0.7–0.8` | **The timing grid.** Drives every cut. |
| SFX (ticks, clacks, swooshes, risers) | `0.25–0.35` | The visual hits' audio twins |
| Voiceover | — | None in the canonical form |

**SFX vocabulary:** tick per typewriter character · thud/clack per card pop · low swoosh per prompt swap · ambient riser into each title card · bass drop on the hard cut out of a title card · final chord ring-out into silence. Wire all audio as sibling `<audio>` elements per the render contract — never inside a `<video>`.

---

## 9 · Inherits / Overrides vs MOTION_PHILOSOPHY

| | MOTION_PHILOSOPHY (Infinite) | LINEAR |
|---|---|---|
| **Inherits** | One idea per beat · black canvas / negative space · motion never fully stops (cursor blink, micro-drift stand in for grid parallax) · hold the outro · callbacks · determinism rules (no `Math.random()`/`Date.now()`) · Law #11 timeline padding (`tl.to({}, { duration: SLOT }, 0)`) · frame-boundary snapping · velocity-matched seams · tween-comment convention | same |
| Default transition | Motion-blurred whip-streak; hard cuts forbidden | **Camera moves through one world** — blurred dives + focus-pulls between product beats, slow fades into rests; hard cuts rare (bracketing the modal) |
| Type treatment | Chrome gradient + halo glow; type scales 8×, is "a character" | Flat gray-white Geist; type is quiet — **the UI is the character** |
| Unifying texture | Perspective grid + crosshairs + grain + vignette | Matte void + faint vignette + depth-of-field **only** — no grid, no grain |
| Palette | ≤5 symbolic colors, light-as-brand | **Strictly grayscale** (accent exists only as a brand-swap slot), matte-as-brand |
| Audio | VO-driven, 0.15 pad underscore | **Music-driven** at 0.7–0.8, no VO |
| Scene length | ~1.5s average | 2–4s demo beats on a beat grid |

When in doubt: keep MOTION_PHILOSOPHY's *discipline*, reject its *surface*.

---

## 10 · Anti-patterns

- ❌ **Chrome gradients, halo glows, light streaks on type.** Linear is matte. Flat gray-white *is* the look. (White edge-glints on stations are the one sanctioned luminance accent.)
- ❌ **Any hue in the canonical form.** The reference is 100% grayscale — no purple send buttons, no colored focus rings, no colored status dots. Accent enters only as a deliberate brand swap.
- ❌ **Block cursors.** Inputs take a thin 2px beam; mono/code surfaces take a trailing underscore. Nothing else.
- ❌ **Rounded app-cards for flow steps.** Stations are sharp-cornered terminal blueprints — radius 0, mono uppercase, hairline-split rows. A 10px-radius "card" in the journey reads as the wrong genre.
- ❌ **Recessing passed steps backward — or exiting them entirely.** The camera dollies *past* stations: outgoing cards grow, blur, and **park overhead**, peeking into the top of frame as foreground depth until the next hop. Shrinking them into a deck inverts the depth read; fading them fully off-frame throws the depth away.
- ❌ **Fast sharp movers.** Anything traveling quickly renders blurred (Law #10) — a crisp element whipping across the frame reads as cheap web animation. Conversely, never leave residual blur on a resting element.
- ❌ **Uniform stagger entrances for multi-element arrivals.** Four pills fading up in identical lockstep is the tell of a default. They fall onto the UI from different directions with overlapping motion-blurred flights.
- ❌ **Scale-pops on title cards or the logo.** Rests fade in by luminance over a full second; the logo never scales and never fades out at the end.
- ❌ **Room-to-room hard cuts between product beats.** The world is continuous — dive or focus-pull. Cuts that teleport between unrelated surfaces break the camera's reality.
- ❌ **Elastic/bouncy easing.** Arrivals are pressed-in (`power2`/`power3.out`); keep `back.out` ≤1.2 and rare. No `elastic.*`, no `bounce.*`.
- ❌ **Static background code.** The code world is alive — it types on with trailing `_` cursors. A frozen code wallpaper reads as a screenshot.
- ❌ **Kinetic type stunts** — 8× scale-throughs, tracking-expands, word-by-word chrome sweeps, per-beat font swaps. Wrong register.
- ❌ **Hits that ignore the music.** If a hop or push lands off-beat, the piece reads broken even if every frame is beautiful.
- ❌ **Fake-looking UI.** Wrong paddings, missing borders, lorem-ipsum microcopy — the register lives or dies on product believability.
- ❌ **Full-screen linear gradients** (H.264 banding) and the **`transparent` keyword in gradients** (shader-compat rule) — use `rgba(8,9,10,0)`.
- ❌ **Pure `#fff` text or pure `#000` canvas in demo beats.** Gray-white on near-black; pure black is reserved for rests.
- ❌ Standard render-contract violations: `Math.random()`/`Date.now()`, `repeat: -1`, unpadded timelines, animating `<video>` geometry directly.

---

## 11 · Pre-flight Checklist (before claiming a Linear piece is done)

- [ ] **Beat map existed before authoring** — BPM documented at the top of `index.html`, all `data-start` values on the grid
- [ ] **Every hit lands on a beat** — dives, station hops, bubble pushes, white-fill swaps (scrub the draft against the track)
- [ ] **Zero hue in the frame** (canonical) — or exactly one deliberate brand accent confined to UI chrome
- [ ] **Cursors correct**: thin beam in inputs, trailing `_` on mono/code — no block cursors anywhere
- [ ] **The camera travels** — product beats connect by dive or focus-pull; no room-to-room cuts inside a sprint
- [ ] **Passed stations park overhead** (grow + blur + stay peeking into the top of frame), never recess backward, never exit fully
- [ ] **Motion blur on every fast move** — full-frame smear on camera hops (peaking mid-hop, resolving on arrival), per-element blur on flights; movers blurred, rests razor-sharp
- [ ] **Multi-element arrivals come from different directions** with overlapping flights — no uniform stagger-fades
- [ ] **Background code is typing** somewhere in every code-world frame
- [ ] **Title cards ≤5 words**, ~1.1s luminance fade, ≥1.2s legible hold, gray-white on pure black
- [ ] **Typewriter ticks sync** with character reveals
- [ ] **UI surfaces pass the "could this ship?" squint test** (borders, radii, paddings, microcopy) — and stations pass the "could this print on a schematic?" test
- [ ] **Outro: ~1s fade-in, dead-still hold, ends on the logo** — no fade-out, no scale
- [ ] **Every sub-composition timeline ends with the Law #11 duration anchor**
- [ ] **All tween end-times snap to frame boundaries** (multiples of 1/30)
- [ ] **Visual verification done** — frames extracted per scene hero moment, actually opened and checked against the reference frames
