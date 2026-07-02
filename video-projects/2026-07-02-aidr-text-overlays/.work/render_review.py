#!/usr/bin/env python3
"""Render AIDR v493 (overlays + SFX) to a 1080p H.264 review mp4."""
import sys
import time

sys.path.insert(0, "/Users/andydepp/Projects/davinci-resolve-mcp/.claude/worktrees/practical-goldberg-4005cb")
import src.server as s  # noqa: E402

OUT_DIR = "/Users/andydepp/Projects/OperatorOS/videos/2026-06-30-ai-edited-my-video-in-real-davinci-resolve/04-edit"
NAME = "AIDR-v5-textoverlays-sfx-review"

r = s.get_resolve()
pm = r.GetProjectManager()
proj = pm.GetCurrentProject()
assert proj.GetName() == "ai-edited-davinci-resolve"
tl, _ = s._find_timeline_by_name(proj, "AIDR v5")
proj.SetCurrentTimeline(tl)

proj.DeleteAllRenderJobs()
assert proj.SetRenderSettings({
    "SelectAllFrames": True,
    "TargetDir": OUT_DIR,
    "CustomName": NAME,
    "ExportVideo": True,
    "ExportAudio": True,
    "FormatWidth": 1920,
    "FormatHeight": 1080,
})
job = proj.AddRenderJob()
assert job, "AddRenderJob failed"
assert proj.StartRendering([job], isInteractiveMode=False)
while proj.IsRenderingInProgress():
    time.sleep(5)
st = proj.GetRenderJobStatus(job)
print("status:", st)
assert st.get("JobStatus") == "Complete", st
print("RENDER OK:", f"{OUT_DIR}/{NAME}.mp4")
