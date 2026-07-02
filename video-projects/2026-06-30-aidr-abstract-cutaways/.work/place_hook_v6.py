#!/usr/bin/env python3
"""Place hook-missingtrack (+ SFX stem) on the AIDR v6 timeline.

Anchor: master 0:11.011 of AIDR-v6-hook-v2.mp4 (= frame 330 @ 30000/1001),
assuming the hook export aligns to the timeline head. --inspect prints the
timeline's early items so that assumption can be verified before --run.
Video + stem trimmed to 398 frames (13.2799s) for 49ms VO clearance.
"""
import os
import sys

RENDERS = "/Users/andydepp/Projects/hyperframes-editor/.claude/worktrees/interesting-rosalind-48c072/video-projects/2026-06-30-aidr-abstract-cutaways/renders"
VIDEO = os.path.join(RENDERS, "hook-missingtrack-final.mp4")
STEM = os.path.join(RENDERS, "sfx", "hook-missingtrack-sfx.wav")
REC_OFFSET_FRAMES = 330
NFRAMES = 398
FPS = 29.97

sys.path.insert(0, "/Users/andydepp/Projects/davinci-resolve-mcp/.claude/worktrees/practical-goldberg-4005cb")
import src.server as s  # noqa: E402

r = s.get_resolve()
assert r is not None, "Resolve not running"
pm = r.GetProjectManager()
proj = pm.GetCurrentProject()
print("project:", proj.GetName())

tl = None
for i in range(1, int(proj.GetTimelineCount()) + 1):
    t = proj.GetTimelineByIndex(i)
    print("timeline:", t.GetName())
    if t.GetName().strip().lower() in ("aidr v6", "aidr-v6"):
        tl = t
assert tl, "AIDR v6 timeline not found"
proj.SetCurrentTimeline(tl)
tl_start = int(tl.GetStartFrame() or 0)
print(f"\nusing timeline {tl.GetName()!r}, startFrame={tl_start}, "
      f"dur={(int(tl.GetEndFrame()) - tl_start) / FPS:.1f}s, "
      f"Vtracks={tl.GetTrackCount('video')}, Atracks={tl.GetTrackCount('audio')}")

# what lives in the first 40s of each track?
horizon = tl_start + int(40 * FPS)
for kind in ("video", "audio"):
    for tr in range(1, int(tl.GetTrackCount(kind)) + 1):
        items = tl.GetItemListInTrack(kind, tr) or []
        early = [it for it in items if it.GetStart() < horizon]
        if early:
            desc = ", ".join(f"{it.GetName()}@{(it.GetStart() - tl_start) / FPS:.1f}s"
                             for it in early[:6])
            print(f"  {kind[0].upper()}{tr}: {desc}" + (" …" if len(early) > 6 else ""))

if "--run" not in sys.argv:
    print("\nINSPECT ONLY — pass --run to place.")
    sys.exit(0)

mp = proj.GetMediaPool()
root = mp.GetRootFolder()
bins = {f.GetName(): f for f in (root.GetSubFolderList() or [])}
if "HF-CUTAWAYS" not in bins:
    bins["HF-CUTAWAYS"] = mp.AddSubFolder(root, "HF-CUTAWAYS")
mp.SetCurrentFolder(bins["HF-CUTAWAYS"])
have = {c.GetName(): c for c in (bins["HF-CUTAWAYS"].GetClipList() or [])}
need = [p for p in (VIDEO, STEM) if os.path.basename(p) not in have]
if need:
    mp.ImportMedia(need)
    have = {c.GetName(): c for c in (bins["HF-CUTAWAYS"].GetClipList() or [])}
vclip = have.get(os.path.basename(VIDEO))
aclip = have.get(os.path.basename(STEM))
assert vclip and aclip, "imported clips not found in pool"

assert tl.AddTrack("video"), "could not add video track"
assert tl.AddTrack("audio"), "could not add audio track"
vtrack = int(tl.GetTrackCount("video"))
atrack = int(tl.GetTrackCount("audio"))
print(f"placing on fresh tracks V{vtrack} / A{atrack}")

rec = tl_start + REC_OFFSET_FRAMES
infos = [
    {"mediaPoolItem": vclip, "startFrame": 0, "endFrame": NFRAMES - 1,
     "recordFrame": rec, "trackIndex": vtrack, "mediaType": 1},
    {"mediaPoolItem": aclip, "startFrame": 0, "endFrame": NFRAMES - 1,
     "recordFrame": rec, "trackIndex": atrack, "mediaType": 2},
]
appended = mp.AppendToTimeline(infos)
print("appended:", len(appended or []), "of 2")
for tr, kind in ((vtrack, "video"), (atrack, "audio")):
    for it in tl.GetItemListInTrack(kind, tr) or []:
        print(f"  {kind.upper()}{tr}: {it.GetName()} {it.GetStart()}–{it.GetEnd()} "
              f"({(it.GetEnd() - it.GetStart()) / FPS:.2f}s @ "
              f"{(it.GetStart() - tl_start) / FPS:.3f}s)")
pm.SaveProject()
print("SAVED")
