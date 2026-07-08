#!/usr/bin/env python3
"""Build the SFX-only stem for the AIDR v6 hook overlays (hv-*).

One 65.0 s stereo WAV, silence except at cue times. Class targets are the SAME
as the approved v5 stem (consistency with the rest of the video matters more
than re-staging against the hotter v6 bus): stamp -7.5 dBFS, strike -8.5,
standard -10.5, wexit -13.5, whir -14.5. amix normalize=0; no loudnorm
(Resolve owns the mix). Mono file peaks measured POST-upmix.

Usage: python3 build_hook_sfx.py            -> renders .work/hook-sfx-stem.wav
       python3 build_hook_sfx.py --audition -> also renders two labeled
                                               audition slices over the hook
"""
import os
import re
import subprocess
import sys

PROJ = "/Users/andydepp/Projects/hyperframes-editor/video-projects/2026-07-02-aidr-text-overlays"
SFX = os.path.join(PROJ, "assets", "sfx")
WORK = os.path.join(PROJ, ".work")
MASTER = "/Users/andydepp/Projects/OperatorOS/videos/2026-06-30-ai-edited-my-video-in-real-davinci-resolve/04-edit/AIDR-v6-hook-v2.mp4"
FFMPEG = "/opt/homebrew/bin/ffmpeg"
DUR = 65.0

# class -> (file, target peak dBFS pre-mix, optional (slice_start, slice_dur))
CLASSES = {
    "pop":      ("click-pop.wav",    -10.5, None),
    "tick":     ("tick-pill.wav",    -10.5, None),
    "blip":     ("bubble-blip.wav",  -10.5, None),
    "chime":    ("chime-send.mp3",   -10.5, None),
    "pen":      ("pen-underline.mp3", -11.5, (0.0, 0.9)),
    "wmed":     ("whoosh-med.wav",   -12.0, None),
    "wexit":    ("whoosh-exit.wav",  -13.5, None),
    "whir_s":   ("data-whir.wav",    -14.5, (2.0, 0.9)),
    "stamp":    ("stamp-ink.mp3",     -7.5, None),   # HERO: ALL — EDITED BY AI
    "strike":   ("strike-soft.wav",   -8.5, None),   # HERO-ish: can't describe it
}

# (hook time s == AIDR v6 timeline s, class, comment)
CUES = [
    # hv-stack (part @8.50)
    (12.00, "tick",   "chip: text animation"),
    (13.34, "tick",   "chip: graphic animation"),
    (15.20, "tick",   "chip: b-roll overlays"),
    (17.26, "tick",   "chip: the cuts themselves"),
    (19.90, "stamp",  "ALL — EDITED BY AI ink stamp HERO"),
    (22.40, "blip",   "flip: the 80% recedes"),
    (23.36, "pop",    "chip: the 20% — mine"),
    (25.30, "wexit",  "stack exit"),
    # hv-loop (part @28.50)
    (29.45, "pop",    "full MP4 pill in"),
    (33.76, "blip",   "pill re-pulse"),
    (35.00, "whir_s", "loop starts"),
    (39.90, "whir_s", "loop accelerates"),
    (41.40, "blip",   "jitter climax (going crazy)"),
    (43.10, "wexit",  "loop snap-clear"),
    # hv-seesay (part @46.80) — quiet hero beat
    (47.60, "tick",   "eyebrow: do it yourself"),
    (51.30, "wmed",   "hero L1 in"),
    (53.30, "strike", "hero L2: can't describe it"),
    # hv-both (part @56.80)
    (57.64, "wmed",   "eyebrow: best of both worlds"),
    (60.20, "wmed",   "your editor slides in"),
    (62.20, "pen",    "plus sign draws"),
    (63.10, "wmed",   "your agent slides in"),
    (63.90, "chime",  "lockup settles"),
]

def file_peak(path):
    """Peak after the same mono->stereo upmix the cue chain applies (mono
    sources lose ~3 dB there, so measure post-upmix, not the raw file)."""
    out = subprocess.run([FFMPEG, "-i", path, "-af",
                          "aformat=channel_layouts=stereo,volumedetect",
                          "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    m = re.search(r"max_volume: (-?[\d.]+) dB", out)
    return float(m.group(1))

peaks = {}
for cls, (fname, _t, _s) in CLASSES.items():
    p = os.path.join(SFX, fname)
    if fname not in peaks:
        peaks[fname] = file_peak(p)

# build filtergraph: one input per cue
inputs, chains, mixes = [], [], []
for i, (t, cls, _c) in enumerate(CUES):
    fname, target, slc = CLASSES[cls]
    gain = target - peaks[fname]
    inputs += ["-i", os.path.join(SFX, fname)]
    f = f"[{i}:a]"
    if slc:
        st, d = slc
        f += f"atrim={st}:{st+d},asetpts=PTS-STARTPTS,afade=in:d=0.03,afade=out:st={d-0.1:.2f}:d=0.1,"
    f += (f"volume={gain:.1f}dB,aresample=48000,aformat=channel_layouts=stereo,"
          f"adelay={int(round(t*1000))}:all=1[c{i}]")
    chains.append(f)
    mixes.append(f"[c{i}]")

groups = [mixes[i:i+16] for i in range(0, len(mixes), 16)]
gouts = []
for gi, g in enumerate(groups):
    chains.append("".join(g) + f"amix=inputs={len(g)}:duration=longest:normalize=0[g{gi}]")
    gouts.append(f"[g{gi}]")
chains.append(f"anullsrc=r=48000:cl=stereo:d={DUR}[base]")
chains.append("[base]" + "".join(gouts) +
              f"amix=inputs={len(gouts)+1}:duration=first:normalize=0[out]")

os.makedirs(WORK, exist_ok=True)
stem = os.path.join(WORK, "hook-sfx-stem.wav")
cmd = [FFMPEG, "-y", "-v", "error"] + inputs + [
    "-filter_complex", ";".join(chains), "-map", "[out]",
    "-c:a", "pcm_s16le", stem]
subprocess.run(cmd, check=True)
print("stem:", stem)

with open(os.path.join(WORK, "hook-sfx-plan.md"), "w") as fh:
    fh.write("# SFX plan — AIDR v6 hook overlays (hv-*)\n\n"
             "Same class targets as the approved v5 stem (stamp -7.5 / strike -8.5 / "
             "standard -10.5 / wexit -13.5 / whir -14.5 dBFS pre-mix). Stem placed in "
             "the A4 gap 8.30-65.00s of AIDR v6; amix normalize=0, no loudnorm.\n\n"
             "| hook t | class | file | note |\n|---|---|---|---|\n")
    for t, cls, c in CUES:
        fh.write(f"| {int(t//60)}:{t%60:05.2f} | {cls} | {CLASSES[cls][0]} | {c} |\n")
print("plan: .work/hook-sfx-plan.md  cues:", len(CUES))

if "--audition" in sys.argv:
    for name, lo, hi in [("audition-stack", 8, 27), ("audition-both", 56, 65)]:
        out = os.path.join(WORK, f"{name}.mp4")
        subprocess.run([
            FFMPEG, "-y", "-v", "error",
            "-ss", str(lo), "-to", str(hi), "-i", MASTER,
            "-ss", str(lo), "-to", str(hi), "-i", stem,
            "-filter_complex",
            "[0:a][1:a]amix=inputs=2:duration=first:normalize=0[a]",
            "-map", "0:v", "-map", "[a]", "-c:v", "libx264", "-preset", "fast",
            "-crf", "20", "-c:a", "aac", "-b:a", "192k", out], check=True)
        print("audition:", out)
