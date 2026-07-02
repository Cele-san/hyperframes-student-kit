#!/usr/bin/env python3
"""Place the six AIDR abstract cutaways (+ SFX stems) on the v5 timeline in Resolve.

Anchors are spoken-phrase pins resolved in the v5 WhisperX transcript — v5 IS the
reference, no fragment-chain mapping. Video → V3 (above the existing V2 screen-rec
inserts; the wordrain intercut and cutter replacement happen by coverage).
SFX stems → A3 at the same recordFrame. VO on A1 untouched.

Dry-run by default; --run to place. --timeline <name> required for --run.
"""
import json
import os
import sys

RENDERS = "/Users/andydepp/Projects/hyperframes-editor/.claude/worktrees/interesting-rosalind-48c072/video-projects/2026-06-30-aidr-abstract-cutaways/renders"
TRANSCRIPT = "/private/tmp/claude-501/-Users-andydepp-Projects-hyperframes-editor--claude-worktrees-interesting-rosalind-48c072/106cbc2b-bae3-4977-9b8a-336b717d96a1/scratchpad/v5-transcript/AIDR-v5.json"
FPS = 29.97

data = json.load(open(TRANSCRIPT))
words = []
for seg in data.get("segments", []):
    for w in seg.get("words", []):
        if "start" in w:
            words.append({"word": w["word"].strip().lower().strip(".,!?'\""), "start": w["start"]})


def phrase_time(phrase):
    toks = phrase.lower().split()
    for i in range(len(words) - len(toks) + 1):
        if all(toks[j] in words[i + j]["word"] for j in range(len(toks))):
            return words[i]["start"]
    return None


# label, part slug, anchor phrase, offset (s relative to phrase start), duration
INSERTS = [
    ("B0 two-fates split (fills black-box gap)", "b0-twofates",
     "render me a finished", -2.2, 12.0),
    ("B3 word rain (intercut after real screen-rec)", "b3-wordrain",
     "down to the timestamp", 0.0, 8.0),
    ("B3 traveling cutter (covers [ADDED] typing insert)", "b3-cutter",
     "you give it two things", 0.0, 14.0),
    ("B3 runtime tower (lead-in to real-timeline shot)", "b3-tower",
     "cross referencing my script", 0.0, 9.0),
    ("B5 junior/senior relay", "b5-relay",
     "junior editor in your pocket", -1.0, 10.0),
    ("B7 rising ceiling", "b7-asymptote",
     "at least 80", 0.0, 8.0),
]

resolved = []
for label, slug, phrase, off, dur in INSERTS:
    t = phrase_time(phrase)
    if t is None:
        print(f"ANCHOR MISS: {label!r} — phrase {phrase!r} not found in v5 transcript")
        continue
    rec = max(0.0, t + off)
    vf = os.path.join(RENDERS, f"{slug}-final.mp4")
    af = os.path.join(RENDERS, "sfx", f"{slug}-sfx.wav")
    ok_v, ok_a = os.path.exists(vf), os.path.exists(af)
    resolved.append({"label": label, "slug": slug, "rec": rec, "dur": dur,
                     "video": vf, "sfx": af})
    print(f"  V3 @{int(rec // 60)}:{rec % 60:05.2f} +{dur:4.1f}s | {slug:14s} "
          f"video={'OK' if ok_v else 'MISSING'} sfx={'OK' if ok_a else 'MISSING'} | {label}")

# overlap clamp between our own inserts (same track): pull the EARLIER one back
resolved.sort(key=lambda r: r["rec"])
for i in range(len(resolved) - 2, -1, -1):
    a, b = resolved[i], resolved[i + 1]
    if a["rec"] + a["dur"] > b["rec"]:
        new = b["rec"] - a["dur"] - 1 / FPS
        print(f"  clamp: {a['slug']} {a['rec']:.2f} -> {new:.2f} (was overlapping {b['slug']})")
        a["rec"] = new

if "--run" not in sys.argv:
    print(f"\nDRY RUN — {len(resolved)} inserts resolved. Pass --run --timeline <name> to place.")
    sys.exit(0)

sys.path.insert(0, "/Users/andydepp/Projects/davinci-resolve-mcp/.claude/worktrees/practical-goldberg-4005cb")
import src.server as s  # noqa: E402

r = s.get_resolve()
assert r is not None, "Resolve not running"
pm = r.GetProjectManager()
proj = pm.GetCurrentProject()
print("project:", proj.GetName())
mp = proj.GetMediaPool()
root = mp.GetRootFolder()
bins = {f.GetName(): f for f in (root.GetSubFolderList() or [])}
if "HF-CUTAWAYS" not in bins:
    bins["HF-CUTAWAYS"] = mp.AddSubFolder(root, "HF-CUTAWAYS")
mp.SetCurrentFolder(bins["HF-CUTAWAYS"])
have = {c.GetName(): c for c in (bins["HF-CUTAWAYS"].GetClipList() or [])}
need = []
for r_ in resolved:
    for p in (r_["video"], r_["sfx"]):
        if os.path.basename(p) not in have:
            need.append(p)
if need:
    mp.ImportMedia(need)
    have = {c.GetName(): c for c in (bins["HF-CUTAWAYS"].GetClipList() or [])}

tl_name = sys.argv[sys.argv.index("--timeline") + 1]
tl, _ = s._find_timeline_by_name(proj, tl_name)
assert tl, f"timeline {tl_name!r} not found"
proj.SetCurrentTimeline(tl)
# always append FRESH top tracks — never touch existing content
assert tl.AddTrack("video"), "could not add video track"
assert tl.AddTrack("audio"), "could not add audio track"
vtrack = int(tl.GetTrackCount("video"))
atrack = int(tl.GetTrackCount("audio"))
print(f"placing on fresh tracks V{vtrack} / A{atrack} of {tl.GetName()!r}")

tl_start = int(tl.GetStartFrame() or 0)
infos = []
for r_ in resolved:
    vclip = have.get(os.path.basename(r_["video"]))
    aclip = have.get(os.path.basename(r_["sfx"]))
    assert vclip and aclip, f"clips missing in pool for {r_['slug']}"
    nfr = int(round(r_["dur"] * FPS))
    rec = tl_start + int(round(r_["rec"] * FPS))
    infos.append({"mediaPoolItem": vclip, "startFrame": 0, "endFrame": nfr - 1,
                  "recordFrame": rec, "trackIndex": vtrack, "mediaType": 1})
    infos.append({"mediaPoolItem": aclip, "startFrame": 0, "endFrame": nfr - 1,
                  "recordFrame": rec, "trackIndex": atrack, "mediaType": 2})
appended = mp.AppendToTimeline(infos)
print("appended:", len(appended or []), "of", len(infos))
for tr, kind in ((vtrack, "video"), (atrack, "audio")):
    items = tl.GetItemListInTrack(kind, tr) or []
    print(f"{kind.upper()}{tr}: {len(items)} items")
    for it in items:
        print(f"  {it.GetName()}: {it.GetStart()}–{it.GetEnd()} "
              f"({(it.GetEnd() - it.GetStart()) / FPS:.1f}s)")
pm.SaveProject()
print("SAVED")
