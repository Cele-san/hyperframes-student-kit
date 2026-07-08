#!/usr/bin/env python3
"""Place .work/sfx-stem.wav on a NEW audio track of AIDR v493.

Additive-only, same discipline as compose_overlays.py: fresh track, per-track
item counts snapshotted before and asserted unchanged after. The stem is one
full-duration clip at timeline start, so cue alignment is inherent.

Dry-run by default; --run to place.
"""
import os
import sys

sys.path.insert(0, "/Users/andydepp/Projects/davinci-resolve-mcp/.claude/worktrees/practical-goldberg-4005cb")

PROJ_DIR = "/Users/andydepp/Projects/hyperframes-editor/video-projects/2026-07-02-aidr-text-overlays"
STEM = os.path.join(PROJ_DIR, ".work", "sfx-stem.wav")
FPS_TL = 29.97
TIMELINE = "AIDR v5"  # canonical hand-finished timeline (v493 is outdated)
EXPECT_DUR_S = 634.6
STEM_DUR_S = 634.7

assert os.path.exists(STEM), STEM
print("stem:", STEM)

if "--run" not in sys.argv:
    print("DRY RUN — pass --run to place.")
    sys.exit(0)

import src.server as s  # noqa: E402

r = s.get_resolve()
assert r is not None, "Resolve not running"
pm = r.GetProjectManager()
proj = pm.GetCurrentProject()
assert proj.GetName() == "ai-edited-davinci-resolve", proj.GetName()

tl, _ = s._find_timeline_by_name(proj, TIMELINE)
assert tl, f"timeline {TIMELINE!r} not found"
proj.SetCurrentTimeline(tl)

tl_start = int(tl.GetStartFrame() or 0)
tl_dur_s = (int(tl.GetEndFrame()) - tl_start) / FPS_TL
assert abs(tl_dur_s - EXPECT_DUR_S) < 3.0, f"timeline {tl_dur_s:.1f}s — wrong timeline?"

n_v = int(tl.GetTrackCount("video") or 0)
n_a = int(tl.GetTrackCount("audio") or 0)
before = {("video", i): len(tl.GetItemListInTrack("video", i) or []) for i in range(1, n_v + 1)}
before.update({("audio", i): len(tl.GetItemListInTrack("audio", i) or []) for i in range(1, n_a + 1)})
print(f"timeline OK: {tl_dur_s:.1f}s, V={n_v} A={n_a}, items={before}")

assert tl.AddTrack("audio", "stereo"), "AddTrack audio failed"
track = int(tl.GetTrackCount("audio"))
assert track == n_a + 1
assert not (tl.GetItemListInTrack("audio", track) or []), "new track not empty?!"
tl.SetTrackName("audio", track, "TEXT-OVERLAY SFX")
print(f"added A{track} (TEXT-OVERLAY SFX)")

mp_ = proj.GetMediaPool()
root = mp_.GetRootFolder()
bins = {f.GetName(): f for f in (root.GetSubFolderList() or [])}
if "TEXT-OVERLAYS" not in bins:
    bins["TEXT-OVERLAYS"] = mp_.AddSubFolder(root, "TEXT-OVERLAYS")
mp_.SetCurrentFolder(bins["TEXT-OVERLAYS"])
have = {c.GetName(): c for c in (bins["TEXT-OVERLAYS"].GetClipList() or [])}
if "sfx-stem.wav" not in have:
    mp_.ImportMedia([STEM])
    have = {c.GetName(): c for c in (bins["TEXT-OVERLAYS"].GetClipList() or [])}
clip = have.get("sfx-stem.wav")
assert clip, "stem not in media pool"

appended = mp_.AppendToTimeline([{
    "mediaPoolItem": clip,
    "startFrame": 0,
    "endFrame": int(round(STEM_DUR_S * FPS_TL)) - 1,
    "recordFrame": tl_start,
    "trackIndex": track,
    "mediaType": 2,
}])
print("appended:", len(appended or []))

after = {("video", i): len(tl.GetItemListInTrack("video", i) or []) for i in range(1, n_v + 1)}
after.update({("audio", i): len(tl.GetItemListInTrack("audio", i) or []) for i in range(1, n_a + 1)})
assert after == before, f"EXISTING TRACKS CHANGED: {before} -> {after}"
items = tl.GetItemListInTrack("audio", track) or []
assert len(items) == 1, f"expected 1 stem item, got {len(items)}"
it = items[0]
lo = (it.GetStart() - tl_start) / FPS_TL
dur = (it.GetEnd() - it.GetStart()) / FPS_TL
print(f"existing tracks untouched ✓  A{track}: {it.GetName()} @{lo:.2f}s +{dur:.1f}s")
assert abs(lo) < 0.05 and abs(dur - EXPECT_DUR_S) < 3.0
pm.SaveProject()
print("saved.")
