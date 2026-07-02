#!/usr/bin/env python3
"""Place the 4 hv-* hook parts on V5 of AIDR v6. Additive-only: V5 gains
exactly 4 items inside (8.3, 65.0); V5's existing 10 items and every other
track are asserted unchanged. Dry-run by default; --run to place."""
import json
import os
import sys

sys.path.insert(0, "/Users/andydepp/Projects/davinci-resolve-mcp/.claude/worktrees/practical-goldberg-4005cb")

PROJ_DIR = "/Users/andydepp/Projects/hyperframes-editor/video-projects/2026-07-02-aidr-text-overlays"
RENDERS = os.path.join(PROJ_DIR, "renders", "overlays")
CUES = json.load(open(os.path.join(PROJ_DIR, ".work", "cues.json")))
FPS_TL = 29.97
FPS_SRC = 30.0
TIMELINE = "AIDR v6"
EXPECT_DUR_S = 661.5
WIN_LO, WIN_HI = 8.30, 65.00   # ov-hook ends 8.24; A-roll cut at 65.03

parts = [c for c in CUES["cues"] if c.get("timeline") == TIMELINE and not c["reserved"]]
assert len(parts) == 4, parts
for p in parts:
    assert p["start_s"] >= WIN_LO and p["start_s"] + p["dur_s"] <= WIN_HI, p
    p["path"] = os.path.join(RENDERS, p["part"] + ".mov")
    assert os.path.exists(p["path"]), p["path"]
    print(f"  @{p['start_s']:6.2f} +{p['dur_s']:5.1f}s  {p['part']}")

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
assert n_v == 5, n_v
TRACK = 5
before = {("video", i): len(tl.GetItemListInTrack("video", i) or []) for i in range(1, n_v + 1)}
before.update({("audio", i): len(tl.GetItemListInTrack("audio", i) or []) for i in range(1, n_a + 1)})
v5_before = {(it.GetName(), it.GetStart()) for it in (tl.GetItemListInTrack("video", TRACK) or [])}
assert len(v5_before) == 10, len(v5_before)
# target window on V5 must be empty
for it in tl.GetItemListInTrack("video", TRACK) or []:
    lo = (it.GetStart() - tl_start) / FPS_TL
    hi = (it.GetEnd() - tl_start) / FPS_TL
    assert hi <= WIN_LO + 0.01 or lo >= WIN_HI, f"V5 window occupied: {it.GetName()} {lo:.2f}-{hi:.2f}"
print(f"timeline OK: {tl_dur_s:.1f}s, V5 has {len(v5_before)} items, window clear")

mp_ = proj.GetMediaPool()
root = mp_.GetRootFolder()
bins = {f.GetName(): f for f in (root.GetSubFolderList() or [])}
assert "TEXT-OVERLAYS" in bins
mp_.SetCurrentFolder(bins["TEXT-OVERLAYS"])
have = {c.GetName(): c for c in (bins["TEXT-OVERLAYS"].GetClipList() or [])}
need = [p["path"] for p in parts if p["part"] + ".mov" not in have]
if need:
    mp_.ImportMedia(need)
    have = {c.GetName(): c for c in (bins["TEXT-OVERLAYS"].GetClipList() or [])}

infos = []
for p in parts:
    clip = have.get(p["part"] + ".mov")
    assert clip, p["part"]
    infos.append({
        "mediaPoolItem": clip,
        "startFrame": 0,
        "endFrame": int(round(p["dur_s"] * FPS_SRC)) - 1,
        "recordFrame": tl_start + int(round(p["start_s"] * FPS_TL)),
        "trackIndex": TRACK,
        "mediaType": 1,
    })
appended = mp_.AppendToTimeline(infos)
print("appended:", len(appended or []), "of", len(infos))

after = {("video", i): len(tl.GetItemListInTrack("video", i) or []) for i in range(1, n_v + 1)}
after.update({("audio", i): len(tl.GetItemListInTrack("audio", i) or []) for i in range(1, n_a + 1)})
expected = dict(before)
expected[("video", TRACK)] = before[("video", TRACK)] + 4
assert after == expected, f"TRACKS CHANGED UNEXPECTEDLY: {before} -> {after}"
v5_now = tl.GetItemListInTrack("video", TRACK) or []
assert v5_before <= {(it.GetName(), it.GetStart()) for it in v5_now}, "existing V5 items moved!"
for it in v5_now:
    lo = (it.GetStart() - tl_start) / FPS_TL
    if it.GetName().startswith("hv-"):
        print(f"  V5 {it.GetName():16s} @{int(lo//60)}:{lo%60:05.2f} +{(it.GetEnd()-it.GetStart())/FPS_TL:.1f}s")
pm.SaveProject()
print("saved.")
