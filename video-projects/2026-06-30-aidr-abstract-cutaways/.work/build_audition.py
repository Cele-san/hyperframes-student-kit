#!/usr/bin/env python3
"""Audition reel: each cutaway final over the REAL v5 VO at its anchor position,
SFX stem mixed at staged gain. Six slices, one concat-filter render.
Usage: build_audition.py <rec_seconds_for_each_part_in_order>  (from the dry-run)
Order: b0-twofates b3-wordrain b3-cutter b3-tower b5-relay b7-asymptote
"""
import subprocess
import sys
import os

ROOT = "/Users/andydepp/Projects/hyperframes-editor/.claude/worktrees/interesting-rosalind-48c072/video-projects/2026-06-30-aidr-abstract-cutaways"
V5 = "/Users/andydepp/Projects/OperatorOS/videos/2026-06-30-ai-edited-my-video-in-real-davinci-resolve/04-edit/AIDR-v5.mp4"
PARTS = [("b0-twofates", 12.0), ("b3-wordrain", 8.0), ("b3-cutter", 14.0),
         ("b3-tower", 9.0), ("b5-relay", 10.0), ("b7-asymptote", 8.0)]

recs = [float(x) for x in sys.argv[1:7]]
assert len(recs) == 6, "need 6 rec times"

inputs = ["-i", V5]
for slug, _ in PARTS:
    inputs += ["-i", os.path.join(ROOT, "renders", f"{slug}-final.mp4")]
    inputs += ["-i", os.path.join(ROOT, "renders", "sfx", f"{slug}-sfx.wav")]

f = []
segs = []
f.append(f"[0:a]asplit=6{''.join(f'[voa{i}]' for i in range(6))}")
for i, ((slug, dur), rec) in enumerate(zip(PARTS, recs)):
    vi = 1 + i * 2       # part video input index
    ai = 2 + i * 2       # stem input index
    f.append(f"[voa{i}]atrim={rec}:{rec + dur},asetpts=PTS-STARTPTS[vo{i}]")
    f.append(f"[vo{i}][{ai}:a]amix=inputs=2:duration=first:normalize=0[a{i}]")
    f.append(f"[{vi}:v]setpts=PTS-STARTPTS,fps=30000/1001[v{i}]")
    segs.append(f"[v{i}][a{i}]")
f.append(f"{''.join(segs)}concat=n=6:v=1:a=1[vout][aout]")
out = os.path.join(ROOT, "renders", "sfx-audition.mp4")
cmd = (["ffmpeg", "-y", "-v", "error"] + inputs +
       ["-filter_complex", ";".join(f), "-map", "[vout]", "-map", "[aout]",
        "-c:v", "libx264", "-crf", "23", "-preset", "veryfast",
        "-c:a", "aac", "-b:a", "192k", out])
subprocess.run(cmd, check=True)
d = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                    "-of", "csv=p=0", out], capture_output=True, text=True).stdout.strip()
print(f"AUDITION OK {out} dur={d}s (expected ~61s)")
