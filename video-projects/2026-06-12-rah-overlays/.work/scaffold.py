#!/usr/bin/env python3
"""Scaffold the 10 self-contained part sub-projects + generate windowed
dense-keyframe 1080p proxies (with audio, for VO sync checks at Gate 2)."""
import json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
b = json.load(open(os.path.join(ROOT, "boundaries.json")))
MASTER = b["source"]

HF_JSON = {
    "$schema": "https://hyperframes.heygen.com/schema/hyperframes.json",
    "registry": "https://raw.githubusercontent.com/heygen-com/hyperframes/main/registry",
    "paths": {"blocks": "compositions", "components": "compositions/components", "assets": "assets"},
}

# Project root configs
json.dump({"id": "2026-06-12-rah-overlays",
           "name": "RAH overlays — Stop reading Claude Code's walls of text (Linear V2)",
           "createdAt": "2026-06-11T00:00:00.000Z",
           "width": 1920, "height": 1080, "fps": 30},
          open(os.path.join(ROOT, "meta.json"), "w"), indent=2)
json.dump(HF_JSON, open(os.path.join(ROOT, "hyperframes.json"), "w"), indent=2)

only = sys.argv[1] if len(sys.argv) > 1 else None
for p in b["parts"]:
    slug = p["slug"]
    if only and slug != only:
        continue
    pdir = os.path.join(ROOT, "parts", slug)
    os.makedirs(os.path.join(pdir, "assets"), exist_ok=True)
    os.makedirs(os.path.join(pdir, "renders"), exist_ok=True)
    json.dump({"id": slug, "name": f"RAH {p['part']} — {p['title']}",
               "createdAt": "2026-06-11T00:00:00.000Z",
               "width": 1920, "height": 1080, "fps": 30},
              open(os.path.join(pdir, "meta.json"), "w"), indent=2)
    json.dump(HF_JSON, open(os.path.join(pdir, "hyperframes.json"), "w"), indent=2)

    proxy = os.path.join(pdir, "assets", "proxy.mp4")
    if not os.path.exists(proxy):
        cmd = ["ffmpeg", "-y", "-v", "error",
               "-ss", f"{p['start_s']:.3f}", "-t", f"{p['duration_s']:.3f}",
               "-i", MASTER,
               "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
               "-g", "30", "-keyint_min", "30", "-sc_threshold", "0",
               "-pix_fmt", "yuv420p",
               "-c:a", "aac", "-b:a", "160k",
               "-movflags", "+faststart", proxy]
        subprocess.run(cmd, check=True)
    dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", proxy], capture_output=True, text=True).stdout.strip()
    print(f"{slug:14} proxy={dur}s (slot {p['duration_s']}s)")
print("scaffold done")
