---
name: hyperframes-shortform
description: THE single authority for GSAP-animated shortform vertical video (9:16, 1080x1920) in HyperFrames — TikTok, Reels, Shorts. ALWAYS use when Andy says "make a short", "shortform", "short-form video", "vertical video", "9:16", "TikTok", "Reels", "Shorts", or when the target composition is 1080x1920 — whatever the input. Three entry points, auto-detected: an edited face-cam recording (face-cam track), a written script or finished VO audio file (faceless track), or a topic only (the hook gets written first, then it builds faceless). Covers the full script-to-short pipeline (detect input, derive beats, assign patterns, scaffold, build, verify, render), a 9:16-tuned GSAP cookbook (hook patterns, karaoke captions, b-roll and data beats, vertical transitions, CTA outros, ambient layers, audio reactivity), the face-cam track (BOTTOM/FULLSCREEN choreography, seam treatment, audio-sync edited-time protocol), and the faceless track (kinetic typography, listicles, quote cards). Supersedes and replaces the retired short-form-video skill — its entire playbook lives here now. Do NOT use for 16:9 landscape work (overlay-beats-video for overlay packages, make-a-video for generic builds), for cutting A-roll in Resolve (cutting-video-from-script), or for long-form YouTube scripting (research-to-script).
---

# Shortform Vertical Video (HyperFrames)

Shortform = **1080x1920 vertical, ~10–60s**, built for TikTok / Reels / Shorts. This skill is the single authority for it: a script-to-short **pipeline**, a 9:16-tuned **GSAP cookbook**, and two tracks — **face-cam** (talking head + scene overlays + karaoke captions) and **faceless** (pure motion graphics: kinetic typography, listicles, quote cards). It supersedes the old `short-form-video` skill; everything that skill knew lives here now.

**Always invoke `/hyperframes` first.** This skill sits on top of the framework — it does not replace the render contract (`data-*` attributes, `window.__timelines`, composition structure, the timeline-padding anchor). Those rules are non-negotiable regardless of format. Read `MOTION_PHILOSOPHY.md` at the workspace root before brainstorming any beat — it is the aesthetic baseline the cookbook is tuned to.

## When this skill fires — and when it does NOT

**Fires when:**
- "Make a short", "shortform", "short-form video", "vertical video", "TikTok", "Reels", "Shorts", "9:16"
- The target composition is 1080x1920 (portrait), regardless of source
- Building from a talking-head recording, a script, a VO file, or just a topic, intended for social
- Retiming, recutting, or re-syncing an existing short; adding karaoke captions to a vertical

**Does NOT fire (hand off instead):**
- 16:9 landscape overlay package over a locked A-roll → `/overlay-beats-video`
- 16:9 generic build / beginner end-to-end → `/make-a-video` (it hands 9:16 builds *here* at its Gate 5)
- Cutting A-roll from a script in DaVinci Resolve → `cutting-video-from-script`
- Long-form YouTube scripting (research → packaging → full script) → `research-to-script`
- Sound design on an already-built short → `/hyperframes-add-sfx` (post-render pass)

## Step 0 — Detect the input, pick the track

Probe whatever Andy hands you, then route. Detection logic + ffprobe commands in `references/pipeline.md`.

| Input | Detect by | Track |
|-------|-----------|-------|
| Edited face-cam recording (`.mp4`/`.mov` **with a video stream**) | `ffprobe -show_streams` finds a video stream | **Face-cam** → `references/facecam.md` |
| Script (`.md`/`.txt`/pasted text) or finished VO (`.wav`/`.mp3`, audio-only) | no video stream / text file | **Faceless** → `references/faceless.md`. Generate VO with `npx hyperframes tts` if only a script exists. |
| Topic only ("make a short about X") | nothing provided | **Topic** → write the hook first (`hook-writer` + `animation-value-prop`), lock the script, then **re-enter as Faceless** |

Whichever track, the pipeline below is the same spine — only the scaffold (4-layer vs 3-layer) and the per-beat patterns differ.

## The pipeline (the spine)

Detail for each step lives in `references/pipeline.md`. Steps marked **HARD-GATE** are non-skippable.

1. **Detect input → pick track** (Step 0 above).
2. **Lock the hook** — invoke `animation-value-prop` (end state → before state → visual direction). Fire `give-the-idea-a-shape` for any beat whose first instinct is "counter / grid / kinetic type."
3. **Audio is source of truth** — edit audio FIRST (cut retakes/pauses) → `<name>-edit.mp4`, or generate VO via `tts`. Measure exact duration with `ffprobe` — that is the composition's `data-duration`.
4. **Transcribe** the edited/VO audio: `npx hyperframes transcribe <file> --model small.en --json` (word-level timestamps — even when you wrote the script; TTS pacing ≠ script pacing).
5. **Derive beats** — group words into one-idea beats (hook ≤3s, mid beats ~1.5–3s, CTA last). Emit the scene table in **edited-time**.
6. **Assign patterns** — one cookbook pattern per beat (see Cookbook index). Beat 1 from `hooks.md`; middle third favors data-feel beats; rotate transitions; one jaw-dropper per 5s; CTA from `hooks.md` outros.
7. **Scaffold** the project (face-cam 4-layer or faceless 3-layer) + `index.html`.
8. **Build scenes** — local 0-based offsets, Law #11 anchor on every timeline, frame-snapped tween ends, captions layer last.
9. **HARD-GATE — Gate 1, live Studio preview** (CLAUDE.md): `npx hyperframes preview` in background, hand Andy the URL, wait for explicit sign-off before ANY render.
10. **Lint → draft render → HARD-GATE frame verification**: extract 8–15 word-exact frames, **Read every PNG**, fix + re-verify until clean.
11. **HARD-GATE — Gate 2, rendered-MP4 preview** (CLAUDE.md) → final `--quality standard` render → 3–4 frame spot-check.

## Non-negotiables (framework + determinism)

- Every sub-composition registers exactly **one paused GSAP timeline** on `window.__timelines["<data-composition-id>"]`, key matching `data-composition-id` exactly.
- Timed visible elements carry `class="clip"` + `data-start` + `data-duration` + `data-track-index` — **except `<video>`/`<audio>`** (`class="clip"` breaks them).
- **Law #11 anchor** ends every timeline: `tl.to({}, { duration: SLOT_DURATION }, 0)` so `tl.duration()` ≥ `data-duration` (no black-frame flash). The older `tl.set({}, {}, DUR)` form also works; new code uses the Law #11 form.
- **Never animate `<video>` dimensions** — it freezes frames. Wrap the video in a div and transform the wrapper.
- **Determinism:** no `Math.random()`, no `Date.now()`, no `repeat: -1` in the render path, no render-time fetches. Seeded PRNGs / harmonic-sin hashes only.
- Tween end-times snap to multiples of `1/fps` (at 30fps: 0.0333, 0.0667, 0.1…). Steep-tail eases alias at sub-frame boundaries.
- **All timing in edited-time.** Never mix original-time and edited-time anchors in one file (see `references/pipeline.md` audio-sync protocol).

## The 11 quality rules (run DURING authoring, not after)

1. **No dead frames.** Every 100ms has an animating element. Offset the first entrance 0.1–0.3s, not t=0.
2. **Scene payoff ≥ 1s hold.** Budget scenes by reveal time, not total time.
3. **Face is a character.** Grade + Ken Burns + side vignette (face-cam track).
4. **No hard seams.** Feather y=960 with a gradient + scan line (bottom-half scenes).
5. **One jaw-dropper per 5s.** Typography slam, glitch, whip-pan, audio-sync slam.
6. **Audio reactivity non-negotiable.** 3–6% on text, 10–30% on background.
7. **Rotate transition flavors.** No two consecutive the same.
8. **Captions pop, don't politely label.** Stroke not pill. Scale + color on the active word.
9. **Motion through full scene duration.** Secondary motion if entrances land early.
10. **Background is a layer, not a color.** Radial + noise + particles + vignette minimum.
11. **Slam/stamp overlays land AFTER target text is fully visible.** `stamp_t ≥ target-visible_t + 0.10–0.25s`. Reveal logic beats word-sync, or the punchline lands before the setup.

## Cookbook index (load on demand)

Pull only the reference files the current beat needs.

| Task | File |
|------|------|
| Building beat 1, the hook | `references/hooks.md` |
| CTA / outro beat | `references/hooks.md` |
| Karaoke + emphasis captions | `references/captions.md` |
| Mid-video b-roll & data/proof beats | `references/scenes.md` |
| Scene-to-scene boundaries | `references/transitions.md` |
| Face on screen (talking head) | `references/facecam.md` |
| No face (kinetic type / listicle / quote) | `references/faceless.md` |
| Background layers & audio pulse | `references/ambient-audio.md` |
| Input detection, beat derivation, scaffolds, retime, verification | `references/pipeline.md` |

## What NOT to do

- Don't animate `<video>` element dimensions — freezes frames. Animate the wrapper div.
- Don't use `repeat: -1` on any timeline — breaks the capture engine. Finite counts only.
- Don't use `Math.random()` / `Date.now()` — breaks determinism. Seeded PRNG if pseudo-random is needed.
- Don't use `<br>` inside captions — natural wrapping + `<br>` produces extra unwanted breaks.
- Don't skip the frame-verification gate. Lint exit code is not visual truth.
- Don't author in original-time if the audio is edited. Edited-time or nothing.
- Don't leave `background: #07121c` flat. Layer it.
- Don't hard-cut between scenes. Rotate transition flavors.
- Don't polite-caption. Pop them.
- Don't let the face sit still. Grade + Ken Burns always (face-cam track).
- Don't lean on `npx hyperframes add <block>` for hero moments — hand-build the jaw-droppers; the registry is for velocity.

## Sibling skills (reference, don't duplicate)

- `/hyperframes` — framework rules. **Always first.**
- `/hyperframes-cli` — `init`, `lint`, `preview`, `render`, `transcribe`, `tts`.
- `/gsap` — generic GSAP semantics (tweens, eases, stagger, timelines).
- `/hyperframes-registry` — installing transition blocks (`whip-pan`, `flash-through-white`, `sdf-iris`, shader packs).
- `animation-value-prop` — Step 2, the hook methodology (end state → before state → visual direction).
- `give-the-idea-a-shape` — Step 6 rescue when a beat's first instinct is a generic counter/grid/kinetic-type.
- `hook-writer` — Topic track: write the hook/script before building.
- `/hyperframes-add-sfx` — post-render sound-design pass.
- `/make-a-video` — receives generic/beginner asks; hands 9:16 builds here at its Gate 5.

## Reference projects + memory pointers

- `video-projects/may-shorts-19/` — canonical short (18.84s, 1080x1920, 7 scenes, face-mode choreography, karaoke + `shift()`, ambient bg + seam). Read `index.html` + a `compositions/scene*.html` before authoring a new face-cam short.
- `video-projects/may-shorts-18/` — secondary reference; the 4 face-cam lessons baked in (BOTTOM scale 0.75, stamp-after-reveal, scene-1→2 fluid fade, data-dashboard scene).

Memory pointers (relevant feedback entries):
- `feedback_short_form_principles.md` — the rules, full rationale
- `feedback_contrast_technique.md` — glow localization + text-shadow halos + brightening dim text
- `feedback_techy_background_layers.md` — 6-layer control-room background stack
- `feedback_visual_verification.md` — the verification gate
- `project_ais_brand_specs.md` — if the short is AIS-branded (hex codes, fonts, logo glow)
