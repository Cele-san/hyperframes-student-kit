#!/usr/bin/env python3
"""Place .work/hook-sfx-stem.wav into the A4 'TEXT-OVERLAY SFX' gap of AIDR v6
(8.24s -> 75.54s after Andy's hook ripple). Source range 8.3-65.0s of the 65s
stem at record 8.3s, so cue alignment is inherent (timeline s == stem s).
Additive-only with full track snapshots. Dry-run by default; --run to place."""
import os
import sys

sys.path.insert(0, "/Users/andydepp/Projects/davinci-resolve-mcp/.claude/worktrees/practical-goldberg-4005cb")

PROJ_DIR = "/Users/andydepp/Projects/hyperframes-editor/video-projects/2026-07-02-aidr-text-overlays"
STEM = os.path.join(PROJ_DIR, ".work", "hook-sfx-stem.wav")
FPS_TL = 29.97
TIMELINE = "AIDR v6"
EXPECT_DUR_S = 661.5
TRACK = 4                      # A4 "TEXT-OVERLAY SFX"
IN_S, OUT_S = 8.30, 65.00      # gap is 8.24 -> 75.54

assert os.path.exists(STEM), STEM
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
assert tl, TIMELINE
proj.SetCurrentTimeline(tl)

tl_start = int(tl.GetStartFrame() or 0)
tl_dur_s = (int(tl.GetEndFrame()) - tl_start) / FPS_TL
assert abs(tl_dur_s - EXPECT_DUR_S) < 3.0, tl_dur_s
n_v = int(tl.GetTrackCount("video") or 0)
n_a = int(tl.GetTrackCount("audio") or 0)
assert tl.GetTrackName("audio", TRACK) == "TEXT-OVERLAY SFX", tl.GetTrackName("audio", TRACK)
before = {("video", i): len(tl.GetItemListInTrack("video", i) or []) for i in range(1, n_v + 1)}
before.update({("audio", i): len(tl.GetItemListInTrack("audio", i) or []) for i in range(1, n_a + 1)})
# the target window on A4 must be empty
for it in tl.GetItemListInTrack("audio", TRACK) or []:
    lo = (it.GetStart() - tl_start) / FPS_TL
    hi = (it.GetEnd() - tl_start) / FPS_TL
    assert hi <= IN_S + 0.01 or lo >= OUT_S, f"A4 gap occupied: {it.GetName()} {lo:.2f}-{hi:.2f}"
print(f"timeline OK: {tl_dur_s:.1f}s, A4 gap clear, items={before}")

mp_ = proj.GetMediaPool()
root = mp_.GetRootFolder()
bins = {f.GetName(): f for f in (root.GetSubFolderList() or [])}
assert "TEXT-OVERLAYS" in bins
mp_.SetCurrentFolder(bins["TEXT-OVERLAYS"])
have = {c.GetName(): c for c in (bins["TEXT-OVERLAYS"].GetClipList() or [])}
if "hook-sfx-stem.wav" not in have:
    mp_.ImportMedia([STEM])
    have = {c.GetName(): c for c in (bins["TEXT-OVERLAYS"].GetClipList() or [])}
clip = have.get("hook-sfx-stem.wav")
assert clip, "stem not in media pool"

appended = mp_.AppendToTimeline([{
    "mediaPoolItem": clip,
    "startFrame": int(round(IN_S * FPS_TL)),
    "endFrame": int(round(OUT_S * FPS_TL)) - 1,
    "recordFrame": tl_start + int(round(IN_S * FPS_TL)),
    "trackIndex": TRACK,
    "mediaType": 2,
}])
print("appended:", len(appended or []))

after = {("video", i): len(tl.GetItemListInTrack("video", i) or []) for i in range(1, n_v + 1)}
after.update({("audio", i): len(tl.GetItemListInTrack("audio", i) or []) for i in range(1, n_a + 1)})
expected = dict(before)
expected[("audio", TRACK)] = before[("audio", TRACK)] + 1
assert after == expected, f"TRACKS CHANGED UNEXPECTEDLY: {before} -> {after}"
new = [it for it in (tl.GetItemListInTrack("audio", TRACK) or [])
       if it.GetName() == "hook-sfx-stem.wav"]
assert len(new) == 1, new
lo = (new[0].GetStart() - tl_start) / FPS_TL
dur = (new[0].GetEnd() - new[0].GetStart()) / FPS_TL
print(f"A4 hook-sfx-stem.wav @{lo:.2f}s +{dur:.1f}s")
assert abs(lo - IN_S) < 0.05 and abs(dur - (OUT_S - IN_S)) < 0.2
pm.SaveProject()
print("saved.")
