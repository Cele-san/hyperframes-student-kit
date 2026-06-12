# SFX Plan — RAH Overlay Composite

SFX are mixed at COMPOSITE time in `.work/build.py` (amix over the master's VO), never baked into
the alpha parts. Cue times below are PART-LOCAL seconds, verified against each part's GSAP
timeline on 2026-06-11. `master_time = part.start_s + local_t` (starts from `boundaries.json`).
If a part's timeline shifts during revisions, update the local cue here — build.py recomputes.

## Loudness law (the "never louder than the talent" contract)

Master measured (`RAH_main V2 .mp4`, full pass):

| metric | value |
|---|---|
| VO integrated | **-34.8 LUFS** |
| VO true peak | **-10.5 dBTP** |
| VO mean (volumedetect) | -38.1 dB |
| LRA | 4.4 LU |

The export is quiet (un-mastered VO level). Rules (REV 5 — LOCKED by Andy 2026-06-11 after five
audition rounds: REV 1 inaudible → +8 → +12 → +16 ("now I hear it") → **REV 5 = REV 4 − 5 dB**):

1. SFX gains below are PRE-normalization, staged against the raw master. Hero stamp peaks
   -16 dBFS raw (5.5 dB under VO peak); everything else ≤ -17; typing bed -23.
2. **The composite's final audio chain normalizes the WHOLE MIX to YouTube reference:
   `loudnorm=I=-14:TP=-1.5:LRA=11` (two-pass, measured)** — Andy's call 2026-06-11. VO and SFX
   ride up together (~+20 dB), so the calibrated balance is preserved. The raw master file is
   never touched; normalization lives in the build.py output chain only.
3. Order matters: amix all SFX with the raw VO FIRST, loudnorm LAST. Never normalize the VO
   before mixing — that would invalidate the calibrated relative gains.
4. Final tune by ear at the Gate-2 :8080 scrub, ±3 dB granularity, per-class only from here.

## Kit — `assets/sfx/` (copied from sibling stashes, semantic renames)

| file | source | dur | src peak | class | raw target peak | **mix gain (REV 5 — LOCKED)** |
|---|---|---|---|---|---|---|
| typing-keys.mp3 | ES_Apple Keyboard 7 | 6.74s | -0.7 | typing bed | -23 | **-22.3 dB** |
| chime-send.mp3 | ES_Multimedia 781 (Andy-picked from 8-way audition; replaced ES_Chime Notification) | 0.47s | -1.4 | send-flash | -21 | **-19.6 dB** (Andy: -4 dB below the send class) |
| stamp-ink.mp3 | ES_Stamp Self Inking 1 | 0.63s | -0.7 | stamp hero | -16 | **-15.3 dB** (P02 reuse: -19.3) |
| wire-twang.mp3 | ES_Wire Twang | 1.64s | -15.5 | wire snap | -21 | **-5.5 dB** |
| pen-underline.mp3 | ES_Pen Write On Paper 3 | 1.18s | -12.6 | underline draw | -21 | **-8.4 dB** |
| click-pop.wav | Click 11 (pop) | 1.49s | -10.6 | card/chip pop | -19 | **-8.4 dB** |
| tick-pill.wav | tick-pill-state (proven kit) | 0.06s | -28.2 | small tag tick | -17 | **+11.2 dB** |
| bubble-blip.wav | cowork kit (proven) | 0.05s | -18.9 | micro state-change | -17 | **+1.9 dB** |
| strike-soft.wav | strike-identity-flip (proven) | 0.44s | -24.3 | strike/punch | -17 | **+7.3 dB** |
| twinkle-skill.mp3 | twinkle-halo-resolve (proven) | 0.50s | -24.8 | save/complete | -17 | **+7.8 dB** |
| whoosh-exit.wav | Woosh Effect 8 (Andy-picked #3 from 8-way in-context picker, class-wide; replaced grid-sweep) | 0.31s | -2.4 | exit/focus-pull | -21 | **-18.6 dB** |
| whoosh-med.wav | Woosh Effect 4 | 1.32s | -4.2 | takeover/dolly move | -19 | **-14.8 dB** |
| data-whir.wav | Data 16(long) | 1.16s | -13.5 | meter/shuffle texture | -22 | **-8.5 dB** |

(History: REV 1 inaudible → +8 → +12 → REV 4 +16 over REV 1 "now I hear it" → **REV 5 locked at
REV 4 − 5 dB, with whole-mix loudnorm to -14 LUFS downstream.**)

**Typing slices:** each type-on cue takes `atrim=<offset>:<offset+dur>` from typing-keys.mp3 with
`afade=in:d=0.03, afade=out:st=<dur-0.08>:d=0.08`. Rotate offsets (0.0 / 1.2 / 2.4 / 3.5 / 4.6)
so the keystroke pattern never repeats verbatim. The jargon chip slice (4.1s) gets an extra -2 dB.

## Cue sheet (~50 cues, ≈1 per 8s)

### P01 · hook (start 0.000)
| local | master | sound | event |
|---|---|---|---|
| 8.85 | 8.85 | bubble-blip | counter revalues to RETAINED · ~0 (moved 8.35→8.85, lands on "none") |
| 17.75 | 17.75 | pen-underline | kline tease draws on blurred Karpathy card |
| 26.90 | 26.90 | whoosh-small | card focus-pull exit |
| 42.14 | 42.14 | **stamp-ink (hero -24)** | APPROVED · UNREAD stamp lands |
| 49.60 | 49.60 | whoosh-med | 12-chip wall pile flights (one whoosh covers the flutter) |
| 52.05 | 52.05 | tick-pill | ALL DAY · EVERY DAY label |

### P02 · doors (start 56.990)
| local | master | sound | event |
|---|---|---|---|
| 8.05 | 65.04 | whoosh-med | dolly hop Station A → B |
| 19.95 | 76.94 | wire-twang | PUNCH 1 · wire retracts, step DROPPED |
| 21.25 | 78.24 | strike-soft | PUNCH 2 · blossom orphan bar, NOT IN PLAN |
| 23.65 | 80.64 | stamp-ink (-4 dB) | APPROVED sweep (rhymes with P01 stamp) |
| 26.00 | 82.99 | whoosh-small | world focus-pull out |
| 28.90 | 85.89 | click-pop | Karpathy card resolves center |

### P03 · the turn (start 89.090)
| local | master | sound | event |
|---|---|---|---|
| 2.20 | 91.29 | pen-underline | kline underline draws (legible payoff) |
| 6.20 | 95.29 | typing ×1.3s | pull-quote line 1 types |
| 7.83 | 96.92 | typing ×0.85s | pull-quote line 2 types |
| 10.10 | 99.19 | whoosh-small | card + quote exit |
| 18.75 | 107.84 | tick-pill | SAME PLAN · NEW SHAPE tag |
| 33.70 | 122.79 | tick-pill | ANY AI · SAME MOVE tag |

### P04 · lives (start 132.430)
| local | master | sound | event |
|---|---|---|---|
| 5.30 | 137.73 | click-pop | WHERE IT LIVES station enters |
| 8.50 | 140.93 | tick-pill | NO NEW TAB |
| 9.55 | 141.98 | tick-pill | NO PUBLISH |
| 10.95 | 143.38 | tick-pill | NO SIGN-UP |
| 16.10 | 148.53 | whoosh-small | station exit |

### P05 · ladder (start 155.490)
| local | master | sound | event |
|---|---|---|---|
| 5.00 | 160.49 | typing ×2.4s | pill #2 types (apple reference) |
| 8.80 | 164.29 | bubble-blip | ⌘V apple.com paste-chip snaps |
| 9.60 | 165.09 | chime-send | pill #2 send-flash |
| — | — | — | (pill #3 CUT at Gate 2 — footage shows the typed sentence; eyebrow only, silent) |
| 25.30 | 180.79 | typing ×4.1s (-2 dB) | jargon chip types verbatim plan line |
| 36.70 | 192.19 | strike-soft | blossom strike on worst clause |
| 45.85 | 201.34 | twinkle-skill | ladder rail rd-3 completes (3-cycle payoff) |

### P06 · cost (start 208.610)
| local | master | sound | event |
|---|---|---|---|
| 5.50 | 214.11 | tick-pill | rule row 1 |
| 9.30 | 217.91 | tick-pill | rule row 2 |
| 13.80 | 222.41 | tick-pill | rule row 3 (COSTS A LITTLE EXTRA) |
| 35.00 | 243.61 | click-pop | DeepSeek price chip |
| — | — | — | (5 TO 15× callout CUT at Gate 2 — the chart's headline carries it) |
| 41.00 | 249.61 | click-pop | DeepSeek cross-link card |
| 47.20 | 255.81 | tick-pill | THIS PAGE · THE SAME TRICK tag |

### P07 · smallest (start 262.434)
| local | master | sound | event |
|---|---|---|---|
| 2.70 | 265.13 | click-pop | step ticker enters |
| 7.00 | 269.43 | tick-pill | dot 02 PLAN |
| 13.30 | 275.73 | typing ×2.1s | pill #4 types (dot 03 at 11.75 now SILENT — ticker is dimmed under the pill) |
| 16.40 | 278.83 | chime-send | send (dot 04 at 16.45 stays SILENT — collision) |

### P08 · system (start 298.630)
| local | master | sound | event |
|---|---|---|---|
| 2.70 | 301.33 | typing ×2.7s | pill #5 types (create skill) |
| 5.60 | 304.23 | chime-send | send-flash |
| 6.40 | 305.03 | twinkle-skill | ◇ skill chip lands [SAVED] |
| 25.00 | 323.63 | tick-pill | THE WIP · UNPACK SKILL tag |
| 33.90 | 332.53 | data-whir | work meter cells light (one whir covers) |

### P09 · thesis (start 341.310)
| local | master | sound | event |
|---|---|---|---|
| 3.45 | 344.76 | whoosh-med | wall assembles (15 staggered bars) |
| 9.10 | 350.41 | whoosh-med | THE REFLOW begins |
| 9.20 | 350.51 | data-whir | reflow shuffle texture (layered under whoosh) |
| 12.20 | 353.51 | tick-pill | 0 WORDS ADDED · 0 REMOVED chip |
| 13.40 | 354.71 | click-pop | pagebox materializes |
| 21.90 | 363.21 | whoosh-small | BEFORE ghost + stage shift |
| 25.35 | 366.66 | strike-soft | blossom edge-glow punch |
| 25.45 | 366.76 | typing ×1.25s | SAME WORDS · NEW SHAPE types |
| 27.85 | 369.16 | whoosh-small | takeover exit, back to Andy |

### P10 · bookend (start 372.371)
| local | master | sound | event |
|---|---|---|---|
| 4.95 | 377.32 | bubble-blip | ACTUALLY READ got-span flash |
| 11.00 | 383.37 | strike-soft | strike on CHAMP · GEMINI 3.5 PRO (moved 9.6→11.0, leads "wrong" by 0.17s) |
| 11.45 | 383.82 | tick-pill | 3.5 FLASH fix chip (moved 10.05→11.45) |
| 22.00 | 394.37 | typing ×1.42s | takeaway pill types |
| 23.72 | 396.09 | chime-send | send #1 |
| 27.55 | 399.92 | typing ×0.85s | ◇ retype (skill compression) |
| 29.15 | 401.52 | chime-send | send #2 (last cue of the video — the tail runs clean; end-screen card REMOVED per Andy 2026-06-11) |

## build.py integration recipe

Each cue becomes one ffmpeg input chain:

```
[i]atrim=...(typing only),volume=<gain>dB,adelay=<master_ms>|<master_ms>[s<i>]
```

then `amix=inputs=<N+1>:duration=first:normalize=0` with the master audio as input 0 at
volume 1.0 (`normalize=0` is REQUIRED — default amix normalization would duck the VO).
Better for >32 inputs: pre-mix the SFX bed in groups of ~25 (`amix` chains), then one final
`[vo][sfxbed]amix=inputs=2:duration=first:normalize=0`.

**Final stage (after the mix):** `loudnorm=I=-14:TP=-1.5:LRA=11` — two-pass: run pass 1 with
`print_format=json` on the MIXED audio to get measured_I/TP/LRA/thresh, feed those into pass 2.
The raw master is ~21 LU below target so loudnorm runs in dynamic mode (linear gain is capped by
true peak) — expected and fine for speech with LRA 4.4.

## AUDIO LOCKED (Andy, 2026-06-11 — "we should be good")

Final chain: REV 5 gains + chime-send = Multimedia 781 at -19.6 dB + whole-mix
`loudnorm=I=-14:TP=-1.5:LRA=11` (two-pass) at composite time. Remaining ear-checks happen on
the full Gate-2 scrub only:
- The two stamps (P01/P02) are the loudest cues by design (the irony pair). Veto if too literal.
- Wire-twang (P02 punch 1) is a literal sound for a literal visual — easy cut if cheesy.
- Counter tick-up at P01 0–8s deliberately has NO sfx (a 12-cue tick run would fight the cold
  open). data-whir at 0.5 is available if the open feels dry.
