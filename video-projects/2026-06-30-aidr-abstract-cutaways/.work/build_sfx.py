#!/usr/bin/env python3
"""Build one SFX stem WAV per AIDR cutaway part.

Gains staged vs the MEASURED v5 master (TP -2.5 dBTP): hero -7.5 / std -10.5 /
soft -13.5 / bed -15.5 dBFS stem peaks. Cue times are local to each part.
Stems land in renders/sfx/<part>-sfx.wav (48k stereo, exactly slot length).
"""
import json
import subprocess
import sys
import os
import re

ROOT = "/Users/andydepp/Projects/hyperframes-editor/.claude/worktrees/interesting-rosalind-48c072/video-projects/2026-06-30-aidr-abstract-cutaways"
KIT = os.path.join(ROOT, "assets", "sfx")
OUT = os.path.join(ROOT, "renders", "sfx")
os.makedirs(OUT, exist_ok=True)

FILES = {
    "stamp": "stamp-ink.mp3", "strike": "strike-soft.wav", "pop": "click-pop.wav",
    "tick": "tick-pill.wav", "blip": "bubble-blip.wav", "twinkle": "twinkle-skill.mp3",
    "whoosh-med": "whoosh-med.wav", "whoosh-exit": "whoosh-exit.wav",
    "data-whir": "data-whir.wav", "typing": "typing-keys.mp3",
}
# round 2 (Andy: "decrease the overall levels — stronger than the current audio"): all classes −6
TIER_DB = {"hero": -13.5, "std": -16.5, "soft": -19.5, "bed": -21.5}

# (t, class, tier, slice_dur_or_None, slice_offset)
PARTS = {
    "b0-twofates": (12.0, [
        (2.0, "whoosh-med", "std", None, 0), (3.55, "pop", "std", None, 0),
        (4.7, "whoosh-exit", "std", None, 0), (7.35, "strike", "std", None, 0),
        (8.7, "pop", "soft", None, 0), (9.15, "tick", "std", None, 0),
        (10.05, "twinkle", "std", None, 0),
    ]),
    "b3-wordrain": (8.0, [
        (0.4, "data-whir", "bed", 1.8, 0.0), (2.3, "typing", "bed", 2.6, 0.0),
        (2.6, "whoosh-exit", "soft", None, 0), (5.35, "data-whir", "bed", 1.5, 2.0),
        (6.9, "twinkle", "std", None, 0),
    ]),
    "b3-cutter": (14.0, [
        (0.55, "pop", "std", None, 0), (0.95, "pop", "soft", None, 0),
        (1.9, "whoosh-med", "std", None, 0), (2.25, "data-whir", "bed", 1.0, 1.0),
        (4.54, "stamp", "hero", None, 0), (5.60, "strike", "std", None, 0),
        (6.66, "strike", "soft", None, 0), (8.26, "strike", "std", None, 0),
        (9.86, "strike", "soft", None, 0), (11.32, "whoosh-med", "soft", None, 0),
        (12.12, "twinkle", "std", None, 0),
    ]),
    "b3-tower": (9.0, [
        (0.4, "data-whir", "bed", 1.4, 0.5), (1.1, "blip", "std", None, 0),
        (2.55, "whoosh-exit", "std", None, 0), (4.15, "whoosh-exit", "soft", None, 0),
        (5.95, "whoosh-exit", "soft", None, 0), (7.35, "stamp", "hero", None, 0),
        (7.6, "twinkle", "std", None, 0),
    ]),
    "b5-relay": (10.0, [
        (0.9, "typing", "bed", 1.9, 1.2), (3.2, "whoosh-med", "std", None, 0),
        (4.35, "whoosh-exit", "soft", None, 0), (5.25, "pop", "std", None, 0),
        (6.35, "whoosh-exit", "soft", None, 0), (7.05, "tick", "std", None, 0),
        (7.95, "whoosh-exit", "soft", None, 0), (8.55, "tick", "soft", None, 0),
        (9.1, "twinkle", "std", None, 0),
    ]),
    "b7-asymptote": (8.0, [
        (0.8, "data-whir", "bed", 2.6, 0.0), (3.6, "whoosh-exit", "std", None, 0),
        (4.5, "data-whir", "bed", 1.7, 1.5), (6.15, "whoosh-exit", "soft", None, 0),
        (6.8, "twinkle", "std", None, 0),
    ]),
    "hook-missingtrack": (13.3, [
        (0.22, "whoosh-med", "soft", None, 0),   # skeleton rails assemble
        (1.46, "pop", "std", None, 0),           # text clips drop
        (2.25, "tick", "soft", None, 0),         # AI stamp 1
        (2.82, "whoosh-med", "std", None, 0),    # graphics slide in
        (3.72, "tick", "soft", None, 0),         # AI stamp 2
        (4.58, "whoosh-exit", "std", None, 0),   # b-roll push
        (5.65, "tick", "soft", None, 0),         # AI stamp 3
        (6.52, "data-whir", "bed", 1.0, 1.0),    # cuts fragment run
        (7.55, "tick", "std", None, 0),          # AI stamp 4
        (8.26, "strike", "std", None, 0),        # ALL pulse
        (8.6, "pop", "soft", None, 0),           # 80% sumline lands
        (11.84, "whoosh-exit", "soft", None, 0), # stack makes room
        (12.05, "stamp", "hero", None, 0),       # YOU track lands (hero)
        (12.35, "twinkle", "std", None, 0),      # payoff text
    ]),
}


def peak_db(path):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-af",
                        "astats=measure_overall=Peak_level:measure_perchannel=none",
                        "-f", "null", "-"], capture_output=True, text=True)
    m = re.findall(r"Peak level dB:\s*(-?[\d.]+)", r.stderr)
    if not m:
        sys.exit(f"no peak for {path}")
    return float(m[-1])


peaks = {cls: peak_db(os.path.join(KIT, f)) for cls, f in FILES.items()}
print("kit peaks:", {k: round(v, 1) for k, v in peaks.items()})

ONLY = [a for a in sys.argv[1:]]
for part, (dur, cues) in PARTS.items():
    if ONLY and part not in ONLY:
        continue
    inputs = ["-f", "lavfi", "-t", str(dur), "-i", "anullsrc=r=48000:cl=stereo"]
    filters, labels = [], []
    for n, (t, cls, tier, sdur, soff) in enumerate(cues):
        inputs += ["-i", os.path.join(KIT, FILES[cls])]
        gain = TIER_DB[tier] - peaks[cls]
        chain = f"[{n + 1}:a]"
        if sdur:
            chain += (f"atrim={soff}:{soff + sdur},asetpts=PTS-STARTPTS,"
                      f"afade=t=in:d=0.05,afade=t=out:st={sdur - 0.25}:d=0.25,")
        chain += (f"volume={gain:.1f}dB,aresample=48000,"
                  f"adelay={int(t * 1000)}:all=1[c{n}]")
        filters.append(chain)
        labels.append(f"[c{n}]")
    mix = f"[0:a]{''.join(labels)}amix=inputs={len(labels) + 1}:duration=first:normalize=0[out]"
    fc = ";".join(filters + [mix])
    out = os.path.join(OUT, f"{part}-sfx.wav")
    cmd = ["ffmpeg", "-y", "-v", "error"] + inputs + \
          ["-filter_complex", fc, "-map", "[out]", "-c:a", "pcm_s16le", out]
    subprocess.run(cmd, check=True)
    pk = peak_db(out)
    d = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", out], capture_output=True, text=True).stdout.strip()
    print(f"STEM OK {part}: peak {pk:.1f} dBFS, dur {d}s, {len(cues)} cues")
print("ALL STEMS DONE")
