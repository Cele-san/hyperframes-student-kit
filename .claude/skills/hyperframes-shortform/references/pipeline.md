# Pipeline — script-to-short, end to end

The workflow spine. Detect the input, lock the hook, treat audio as ground truth, derive beats, assign patterns, scaffold, build, and run the gates. Same spine for both tracks — only the scaffold and per-beat patterns differ.

---

## Step 0 — Input detection

Probe whatever you were handed before assuming a track.

```bash
# Is it video (face-cam), audio-only (faceless VO), or text (faceless script)?
ffprobe -v error -show_entries stream=codec_type -of csv=p=0 "<file>"
```

| ffprobe / file result | Track | Next |
|---|---|---|
| has a `video` stream (`.mp4`/`.mov`) | **Face-cam** | edit the recording, `references/facecam.md` |
| `audio` only (`.wav`/`.mp3`) | **Faceless (VO supplied)** | measure duration, transcribe, `references/faceless.md` |
| text file or pasted script (`.md`/`.txt`) | **Faceless (from script)** | offer `npx hyperframes tts` vs. Andy records, then transcribe |
| nothing — just a topic | **Topic** | hand to `hook-writer` + `animation-value-prop`, lock script, re-enter as Faceless |

If a video has usable audio but Andy wants it faceless (b-roll only), treat it as the Faceless track and pull the audio out as the VO.

---

## Step 2 — Lock the hook (before any HTML)

Invoke `animation-value-prop` and answer its three questions: end state (what the viewer should believe/feel by the end), before state (what they think now), visual direction. The hook beat (0–3s) is the highest-leverage 90 frames in the whole short — a vertical that doesn't earn the swipe in 3s never gets watched. For any beat whose first instinct is "a counter / a grid / kinetic type," fire `give-the-idea-a-shape` to find a truer form first.

---

## Step 3 — Audio is source of truth

**Edit the audio FIRST.** Cut retakes and dead air, save as `<name>-edit.mp4` (or generate VO). The composition is built around the *edited* audio, never the raw take.

```bash
ffprobe -v error -show_entries format=duration -of csv=p=0 assets/<name>-edit.mp4
```

That number is the root composition's `data-duration` and the `data-duration` of every full-length layer (ambient-bg, captions, face video+audio, seam).

For the Faceless-from-script path, generate the VO and measure it:

```bash
npx hyperframes tts "<script text>" --voice am_adam --output assets/vo.wav
ffprobe -v error -show_entries format=duration -of csv=p=0 assets/vo.wav
```

---

## Step 4 — Transcribe (word-level)

```bash
npx hyperframes transcribe assets/<name>-edit.mp4 --model small.en --json
```

Transcribe even when you wrote the script — **TTS/spoken pacing ≠ script pacing**, and the karaoke captions + beat boundaries need real word onsets. Keep the transcript JSON untouched; remap timestamps with `shift()` (below), never by hand-editing the JSON.

> Note: if `npx hyperframes transcribe` errors on this machine, fall back to a direct Whisper CLI for word timestamps (see `feedback_hyperframes_transcribe`). The output you need is `[{word, start, end}]`.

---

## Step 5 — Derive beats

Read the transcript, group words into **one-idea beats**:

- **Hook beat:** ≤ 3s, the first sentence/claim. Always its own beat.
- **Mid beats:** ~1.5–3s each, one idea apiece. If a sentence says two things, split it.
- **CTA beat:** last, the call to action (comment / follow / link).

Snap every boundary to a **word-end in edited-time**. Emit the scene table (this is also the retime artifact):

| Scene | Start (edited) | Dur | Idea (≤2 words) | Pattern |
|-------|----------------|-----|------------------|---------|
| 1 | 0.00 | 2.15 | the claim | typography-slam |
| 2 | 2.15 | 2.53 | the problem | shock-stat-counter |
| … | … | … | … | … |

Scenes sit back-to-back on one `data-track-index` (overlays) with **no gaps** — `scene[n].data-start = scene[n-1].data-start + scene[n-1].data-duration`.

---

## Step 6 — Assign patterns

One cookbook pattern per beat. Rules (these encode the old skill's pacing discipline + the may-shorts-18 lessons):

- **Beat 1 = a hook pattern** (`references/hooks.md`). Never open on a plain label.
- **Middle third favors data-feel beats** (`references/scenes.md` data section) — bar races, counters, rings, grids that flash in sequence. Decoration scenes read as slides; data-feel scenes read as evidence. This is where attention drops hardest.
- **Rotate transitions** — no two consecutive the same flavor (`references/transitions.md`).
- **One jaw-dropper per 5s** of runtime — a typography slam, glitch, whip, or audio-sync slam.
- **CTA beat = an outro pattern** (`references/hooks.md`), ideally `loop-back-to-hook` so the platform loop is seamless.

Record the assignment in the scene table's Pattern column before building — it's the build checklist.

---

## Scaffolds

### Face-cam — 4 always-on layers + scenes

```
index.html (root, 1080x1920, data-composition-id="main")
├── ambient-bg.html        track-index=3  — radial + drift grid + particles + vignette (full duration)
├── face-wrapper + <video> track-index=0  — talking head; wrapper transforms BOTTOM↔FULLSCREEN
├── <audio> (face)         track-index=4  — SEPARATE element, data-volume="1"
├── seam-treatment.html    track-index=5  — feathers y=960 (bottom-half scenes)
├── scene1…N.html          track-index=1  — overlays, back-to-back, no gaps
└── captions.html          track-index=2  — karaoke, word-synced
```

`data-duration` is identical across root, ambient-bg, seam, face video+audio, captions; only scene overlays change over time. The `<video>` is `muted`; its audio rides the sibling `<audio>`. Full constants in `references/facecam.md`.

### Faceless — 3 layers + scenes (no face, no seam)

```
index.html (root, 1080x1920, data-composition-id="main")
├── ambient-bg.html   track-index=3  — full duration (REQUIRED — type needs a lit stage)
├── scene1…N.html     track-index=1  — kinetic-type / list / quote scenes, back-to-back
├── captions.html     track-index=2  — karaoke when a VO exists; SKIP when on-screen type IS the message
└── <audio> (vo)      track-index=4  — VO or music bed, data-volume per MOTION_PHILOSOPHY §2.7
```

Root `index.html` skeleton (both tracks share this shape — drop the face/seam layers for faceless):

```html
<div id="root" data-composition-id="main" data-start="0"
     data-duration="<EDIT_DURATION>" data-width="1080" data-height="1920">
  <div class="scene-layer" data-composition-id="ambient-bg"
       data-composition-src="compositions/ambient-bg.html"
       data-start="0" data-duration="<EDIT_DURATION>" data-track-index="3"
       data-width="1080" data-height="1920"></div>
  <!-- face-wrapper + <video> + <audio> + seam here for FACE-CAM only -->
  <!-- scene overlays: track-index=1, back-to-back -->
  <div class="scene-layer" data-composition-id="captions"
       data-composition-src="compositions/captions.html"
       data-start="0" data-duration="<EDIT_DURATION>" data-track-index="2"
       data-width="1080" data-height="1920"></div>
</div>
```

---

## Audio-sync protocol (DO NOT skip)

**Problem:** if audio is edited (retakes/pauses removed), the source transcript's timestamps no longer match the edited video. Scene starts authored in original-time fire late.

**The rule: ALL timing lives in edited-time. Never mix.**

1. Measure both files; the difference is total cut time:
   ```bash
   ffprobe -v error -show_entries format=duration -of csv=p=0 assets/original.mp4
   ffprobe -v error -show_entries format=duration -of csv=p=0 assets/<name>-edit.mp4
   ```
2. If using a `shift()` function in `captions.html` to map transcript words, it is the source of truth: the map `shift(originalTime) = editedTime` applies to **every scene `data-start` too**.
3. Scene **internal** offsets (inside `compositions/sceneN.html`) are LOCAL relative to the scene's `data-start`. If the parent `data-start` is correct in edited-time, internal offsets stay correct **without** modification — UNLESS a scene straddles a cut, in which case both the parent duration AND the internal offsets shift.
4. Face-mode transition array times MUST use edited-time. They are **not** automatically shifted.

The `shift()` pattern (generalize the cut window to your edit):

```js
// Example: 1.12s removed from the 2.88–4.00s window of the original.
function shift(t) {
  if (t <= 2.88) return t;     // before the cut — unchanged
  if (t < 4.00) return 2.88;   // inside the cut — clamp to the cut-in point
  return t - 1.12;             // after the cut — slide back by the cut length
}
```

---

## Retime protocol (when audio is re-edited or timestamps drift)

1. Measure old and new edited audio with `ffprobe`. Delta = total cut time.
2. Identify cut window(s): which seconds were removed, from where.
3. Write the **Plan table** — every scene `data-start`, `data-duration`, every face-mode transition `t`, and any scene whose internal offsets straddle a cut:

   | Scene | Current start | Current dur | New start | New dur | Rationale |
   |-------|---------------|-------------|-----------|---------|-----------|
   | … | … | … | … | … | … |

   Then the face-mode array, then internal-offset changes, then the frame-verification list.
4. For each scene that straddles a cut, both its parent duration AND its internal offsets change. Scenes entirely on one side of the cut just need parent `data-start` shifted.
5. Lint → draft render → word-exact frame verify → final render. No shortcuts.

---

## The gates & verification

The two CLAUDE.md preview gates wrap the frame-verification gate. Order:

### Gate 1 — live Studio preview (before ANY render)

```bash
cd video-projects/<slug>
npx hyperframes preview   # run in background; wait for "Studio running" on http://localhost:3002
```

Hand Andy the URL + the individual sub-comp URLs (`http://localhost:3002/?comp=<id>` load fastest; the master can stall under software WebGL). **Wait for explicit "looks good, render a draft."** Silence is not approval. Hot reload means further edits show live.

### Frame verification (HARD-GATE — never ship without)

Lint passing ≠ design working.

```bash
npx hyperframes lint
npx hyperframes render --quality draft --output renders/<slug>-vN-draft.mp4

mkdir -p renders/frames-vN
for pair in "<t>:<label>" "<t>:<label>" ...; do      # 8–15 WORD-EXACT timestamps, not round numbers
  t="${pair%%:*}"; label="${pair##*:}"
  ffmpeg -y -ss "$t" -i renders/<slug>-vN-draft.mp4 -frames:v 1 -q:v 2 "renders/frames-vN/t${t}-${label}.png"
done
```

**Call `Read` on every PNG** (the image must load into context — do NOT just list filenames). Per frame confirm:

1. The expected visual is on-screen at the expected moment (not 1s late, not early).
2. Speaker's face is not cropped in any bottom-half scene.
3. Full-screen vs bottom-half face mode is correct for that scene.
4. Captions are on-brand, readable, not overflowing.
5. No blank frames, no unintentional overlap, no text off-canvas.

If anything fails: fix → re-render → re-verify. Never ship broken and let Andy find the bug.

> Studio iframe screenshots are unreliable here — verify via ffmpeg frame extraction + Read on PNGs, never `preview_screenshot` (see `feedback_hyperframes_preview_screenshot`).

### Gate 2 — rendered-MP4 preview (before final)

```bash
npx serve renders -p 8080 -n     # NOT python http.server — no Range support, scrubbing breaks
```

Hand Andy `http://localhost:8080/<slug>-vN-draft.mp4`. **Wait for explicit sign-off** on full motion + audio sync.

### Final render

```bash
npx hyperframes render --quality standard --output renders/<slug>-vN.mp4
```

Spot-check 3–4 frames (same timestamps, `frames-vN-final/`) to confirm the standard encode didn't shift anything.
