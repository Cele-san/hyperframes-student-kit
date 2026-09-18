# Garden library v1 — verification

Status: rendered draft for Andy's editorial review. Not final voice sync.

- Clean master: 1920x1080, 30 fps, 26 seconds, 780 frames, no audio stream. Captioned timing preview adds the approved narration below the clean canvas. No words were rewritten and no narration was recorded or cloned.
- HyperFrames 0.8.46: lint 0 errors/0 warnings; runtime 0 errors; layout 0 errors/4 heuristic rotation warnings; contrast 15/15 checks passed. Source and logs retained.
- Rotation warnings reviewed: three leaves deliberately translate while rotating into the collection, so their world-space centers move. The fourth warning treats a lesson symbol as a dial. These are diagram transformations, not gauges. No warnings were suppressed. Direct geometry verification across 18, 19, 20, 21, 22 and 25 seconds found maximum stem-to-leaf attachment error below 0.00001 pixel.
- Nonsequential seeking checked at 4, 8, 14, 20 and 25 seconds, then revisited 4, 25 and 8 seconds. Repeated screenshot hashes match. Five leaf identities present; no invalid SVG attributes or browser exceptions.
- Inspected browser snapshots through growth, initial lesson reveal, both visitor appearances, library transformation and final hold. Inspected encoded master frames every two seconds across the full duration. No empty render, cutaway replacement, missing final leaves or frame-edge clipping in those samples. First runtime check caught a numeric timing/property-name collision; fixed and rerun. Failed evidence preserved separately.
- Brand binding technical preflight passed; original garden local fonts, backdrop and V5 material retained and compared with its supplied reference. This is the video's own standalone graphic, not a graphic inserted on source footage. Technical checks do not constitute aesthetic approval.

## Intentional limits

The raised viewpoint is conveyed by 2D leaf rotation and reorganisation into a collection, not a physical 3D overhead orbit. Care is represented by staged development, with no literal watering-can illustration. Lesson pictograms are illustrative content types. The same visitor leaves and returns; this is a metaphor, not measured audience behaviour. Timing is provisional until Andy records the approved narration.

Only the new garden-library-v1 folder was written during this build. Original garden, parked cutout work, other demos, Resolve, shared guidance, schedules and parent review server were not modified.
