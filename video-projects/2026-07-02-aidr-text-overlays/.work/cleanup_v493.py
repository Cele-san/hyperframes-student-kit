#!/usr/bin/env python3
"""Remove the text-overlay V4 track and SFX A3 track from outdated AIDR v493.
Only deletes tracks whose contents are verifiably ours (ov-*.mov / sfx-stem.wav)."""
import sys
sys.path.insert(0, "/Users/andydepp/Projects/davinci-resolve-mcp/.claude/worktrees/practical-goldberg-4005cb")
import src.server as s

r = s.get_resolve(); pm = r.GetProjectManager(); proj = pm.GetCurrentProject()
assert proj.GetName() == "ai-edited-davinci-resolve"
tl, _ = s._find_timeline_by_name(proj, "AIDR v493")
assert tl
proj.SetCurrentTimeline(tl)

v4 = tl.GetItemListInTrack("video", 4) or []
a3 = tl.GetItemListInTrack("audio", 3) or []
assert len(v4) == 10 and all(it.GetName().startswith("ov-") for it in v4), \
    [it.GetName() for it in v4]
assert len(a3) == 1 and a3[0].GetName() == "sfx-stem.wav", [it.GetName() for it in a3]
print("v493 V4/A3 contents verified as ours")

ok_a = tl.DeleteTrack("audio", 3)
ok_v = tl.DeleteTrack("video", 4)
print("DeleteTrack audio3:", ok_a, "video4:", ok_v)
if not (ok_a and ok_v):
    # fallback: at least empty the tracks
    if not ok_v: print("del V4 items:", tl.DeleteClips(v4))
    if not ok_a: print("del A3 items:", tl.DeleteClips(a3))

nv, na = int(tl.GetTrackCount("video")), int(tl.GetTrackCount("audio"))
items = {f"V{k}": len(tl.GetItemListInTrack("video", k) or []) for k in range(1, nv+1)}
items.update({f"A{k}": len(tl.GetItemListInTrack("audio", k) or []) for k in range(1, na+1)})
print("v493 now:", items)
assert items == {"V1": 179, "V2": 15, "V3": 4, "A1": 184, "A2": 3}, "unexpected final state"
pm.SaveProject()
print("saved — v493 restored to pre-overlay state.")
