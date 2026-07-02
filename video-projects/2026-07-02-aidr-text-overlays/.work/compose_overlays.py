#!/usr/bin/env python3
"""Place the 10 aidr-text-overlays alpha .mov parts on a NEW top video track of
the hand-finished shipped timeline (AIDR v493 → AIDR-v5.mp4).

Additive-only, by construction:
  • a FRESH video track is added on top; only that track receives items
  • per-track item counts are snapshotted before and asserted unchanged after
  • cue windows are asserted clear (≥2s) of the six reserved windows owned by
    the other session (b0-twofates, b3-wordrain, b3-cutter, b3-tower,
    b5-relay, b7-asymptote) — cues.json carries them as reserved:true

Dry-run by default; --run to place. Never touches existing items or audio.
"""
import json
import os
import sys

sys.path.insert(0, "/Users/andydepp/Projects/davinci-resolve-mcp/.claude/worktrees/practical-goldberg-4005cb")

PROJ_DIR = "/Users/andydepp/Projects/hyperframes-editor/video-projects/2026-07-02-aidr-text-overlays"
RENDERS = os.path.join(PROJ_DIR, "renders", "overlays")
CUES = json.load(open(os.path.join(PROJ_DIR, ".work", "cues.json")))
FPS_TL = 29.97          # shipped timeline
FPS_SRC = 30.0          # overlay .mov render fps
TIMELINE = "AIDR v5"  # canonical hand-finished timeline (v493 is outdated)
EXPECT_DUR_S = 634.6

parts = [c for c in CUES["cues"] if not c["reserved"]]
reserved = [c for c in CUES["cues"] if c["reserved"]]

# ---- static checks -----------------------------------------------------------
for p in parts:
    for r in reserved:
        if p["start_s"] < r["start_s"] + r["dur_s"] + 2.0 and r["start_s"] < p["start_s"] + p["dur_s"] + 2.0:
            sys.exit(f"OVERLAP {p['part']} vs {r['part']}")
    mov = os.path.join(RENDERS, p["part"] + ".mov")
    if not os.path.exists(mov):
        sys.exit(f"missing render: {mov}")
    p["path"] = mov
print(f"{len(parts)} parts, all renders present, reserved windows clear")

for p in parts:
    print(f"  @{int(p['start_s']//60)}:{p['start_s']%60:04.1f} +{p['dur_s']:5.1f}s  {p['part']:15s} {p['beat']}")

if "--run" not in sys.argv:
    print("\nDRY RUN — pass --run to place.")
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
assert abs(tl_dur_s - EXPECT_DUR_S) < 3.0, \
    f"timeline duration {tl_dur_s:.1f}s != shipped {EXPECT_DUR_S}s — wrong timeline?"

# snapshot existing tracks
n_v = int(tl.GetTrackCount("video") or 0)
n_a = int(tl.GetTrackCount("audio") or 0)
before = {("video", i): len(tl.GetItemListInTrack("video", i) or []) for i in range(1, n_v + 1)}
before.update({("audio", i): len(tl.GetItemListInTrack("audio", i) or []) for i in range(1, n_a + 1)})
print(f"timeline OK: {tl_dur_s:.1f}s, V-tracks={n_v} A-tracks={n_a}, items={before}")

assert tl.AddTrack("video"), "AddTrack failed"
track = int(tl.GetTrackCount("video"))
assert track == n_v + 1
assert not (tl.GetItemListInTrack("video", track) or []), "new track not empty?!"
print(f"added V{track} (text-overlay track)")

# import renders into their own bin
mp_ = proj.GetMediaPool()
root = mp_.GetRootFolder()
bins = {f.GetName(): f for f in (root.GetSubFolderList() or [])}
if "TEXT-OVERLAYS" not in bins:
    bins["TEXT-OVERLAYS"] = mp_.AddSubFolder(root, "TEXT-OVERLAYS")
mp_.SetCurrentFolder(bins["TEXT-OVERLAYS"])
have = {c.GetName(): c for c in (bins["TEXT-OVERLAYS"].GetClipList() or [])}
need = [p["path"] for p in parts if p["part"] + ".mov" not in have]
if need:
    mp_.ImportMedia(need)
    have = {c.GetName(): c for c in (bins["TEXT-OVERLAYS"].GetClipList() or [])}

infos = []
for p in parts:
    clip = have.get(p["part"] + ".mov")
    assert clip, f"{p['part']}.mov not in media pool"
    infos.append({
        "mediaPoolItem": clip,
        "startFrame": 0,
        "endFrame": int(round(p["dur_s"] * FPS_SRC)) - 1,
        "recordFrame": tl_start + int(round(p["start_s"] * FPS_TL)),
        "trackIndex": track,
        "mediaType": 1,
    })
appended = mp_.AppendToTimeline(infos)
print("appended:", len(appended or []), "of", len(infos))

# ---- post-assertions ---------------------------------------------------------
after = {("video", i): len(tl.GetItemListInTrack("video", i) or []) for i in range(1, n_v + 1)}
after.update({("audio", i): len(tl.GetItemListInTrack("audio", i) or []) for i in range(1, n_a + 1)})
assert after == before, f"EXISTING TRACKS CHANGED: {before} -> {after}"
new_items = tl.GetItemListInTrack("video", track) or []
print(f"existing tracks untouched ✓  V{track} items={len(new_items)}")
for it in new_items:
    lo = (it.GetStart() - tl_start) / FPS_TL
    print(f"  V{track} {it.GetName():20s} @{int(lo//60)}:{lo%60:04.1f} "
          f"+{(it.GetEnd()-it.GetStart())/FPS_TL:.1f}s")
pm.SaveProject()
print("saved.")
