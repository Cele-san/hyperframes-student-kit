#!/usr/bin/env python3
"""Pin part boundaries for the RAH overlay package from the master-V2 whisper
transcript (word timestamps). Boundaries snap DOWN to a 29.97fps frame edge.

Source of truth: .work/master-v2-transcript.json (whisper small.en, word_timestamps).
Output: boundaries.json (project root) + .work/words.tsv (full word dump for cue pinning).
"""
import json, re, sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FPS = 30000 / 1001
TOTAL_S = 409.749333  # ffprobe duration of RAH_main V2 .mp4
MASTER = "/Users/andydepp/Projects/OperatorOS/videos/2026-06-26-reading-ai-output-as-html-claude-artifacts/Exports/RAH_main V2 .mp4"

def norm(w):
    return re.sub(r"[^a-z0-9]", "", w.lower())

doc = json.load(open(os.path.join(ROOT, ".work", "master-v2-transcript.json")))
words = []
for seg in doc["segments"]:
    for w in seg.get("words", []):
        words.append((norm(w["word"]), float(w["start"]), float(w["end"]), w["word"].strip()))

# Full word dump for overlay cue pinning during part builds
with open(os.path.join(ROOT, ".work", "words.tsv"), "w") as f:
    f.write("start\tend\tword\n")
    for n, s, e, raw in words:
        f.write(f"{s:.2f}\t{e:.2f}\t{raw}\n")

def find_phrase(phrase, after=0.0):
    """Return start time of the first word of `phrase` occurring after `after` seconds."""
    target = [norm(t) for t in phrase.split() if norm(t)]
    for i in range(len(words) - len(target) + 1):
        if words[i][1] < after:
            continue
        if all(words[i + j][0] == target[j] for j in range(len(target))):
            return words[i][1]
    raise SystemExit(f"PHRASE NOT FOUND: {phrase!r} after {after}s")

def snap(t):
    return int(t * FPS) / FPS  # snap down to frame edge

# slug, title, anchor phrase that OPENS the part (None = 0.0), search-after guard
PARTS = [
    ("p01-hook",      "Hook + rubber stamp (B1-B2)",            None,                                   0),
    ("p02-doors",     "Doors closing takeover (B3)",            "reading harder didn't work either",    40),
    ("p03-the-turn",  "The turn + prompt pill #1 (B4)",         "whole point at least the way",         80),
    ("p04-lives",     "Where it lives (B5)",                    "now if the word page",                 120),
    ("p05-ladder",    "The ladder, cycles 2-3 (B6)",            "once you've got a page",               150),
    ("p06-cost",      "Rule + cost + DeepSeek (B7)",            "before you go turn everything",        200),
    ("p07-smallest",  "Smallest version walkthrough (B8)",      "feels like a lot",                     255),
    ("p08-system",    "Skill + unpack WIP (B9)",                "at the end of the first plan",         290),
    ("p09-thesis",    "The reflow takeover (B10)",              "remember how I said",                  335),
    ("p10-bookend",   "Bookend + end screen (B11)",             "2000 word plan from the start",        365),
]

starts = []
for slug, title, phrase, after in PARTS:
    t = 0.0 if phrase is None else snap(find_phrase(phrase, after))
    starts.append(t)

def tc(t):
    m = int(t // 60)
    return f"{m}:{t - m * 60:05.2f}"

parts_out = []
for i, (slug, title, phrase, after) in enumerate(PARTS):
    s = starts[i]
    e = starts[i + 1] if i + 1 < len(PARTS) else snap(TOTAL_S)
    parts_out.append({
        "part": f"P{i+1:02d}", "slug": slug, "title": title,
        "start_s": round(s, 3), "end_s": round(e, 3),
        "duration_s": round(e - s, 3),
        "start_tc": tc(s), "end_tc": tc(e),
        "proxy": f"parts/{slug}/assets/proxy.mp4",
    })

out = {"source": MASTER, "fps": "30000/1001", "total_s": TOTAL_S, "parts": parts_out}
with open(os.path.join(ROOT, "boundaries.json"), "w") as f:
    json.dump(out, f, indent=2)

for p in parts_out:
    print(f"{p['part']}  {p['start_tc']:>8} → {p['end_tc']:>8}  ({p['duration_s']:6.2f}s)  {p['slug']:14} {p['title']}")
print(f"\nsum check: {sum(p['duration_s'] for p in parts_out):.3f} vs {snap(TOTAL_S):.3f}")
