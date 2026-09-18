# Garden library v2 — verification

Rendered draft for Andy's editorial review. Clean master: 1920x1080, 30 fps, 30 seconds, 900 frames, 3,771,019 bytes, no audio stream. Separate timing preview: 1920x1230, 30 fps, 30 seconds, approved narration in a band below the unchanged clean picture. Voice remains unrecorded; timing is provisional.

## Selected upgrades checked
- Fixed plant centers verified identical across all sampled times. Perspective camera elevation progresses from 29 to 80 degrees, with distance and framing changes. No leaf shuffle into the library.
- Thirty persistent vein paths, six per leaf, interpolate into lesson geometry. Five original leaf identities remain throughout. No replacement icon opacity fades.
- Original hero leaf and six diagram paths compare identically before/after the first copy transfer. Original reading leaf and six diagram paths compare identically before/after the second transfer. Source opacity remains 1; copies are separate objects.
- Nonsequential seek screenshot hashes match on repeated 5, 7.3 and 29 second visits after later times. No browser exceptions or invalid SVG attributes. See verification.json and verify.cjs.
- All grown leaves remain within the picture bounds at sampled growth/camera times. Visitor bounds checked at first visit, return, camera rise and final hold. Initial tests caught top-leaf clipping and an encoded camera midpoint caught the visitor's feet crossing the lower border; both were repaired and rerendered. Earlier render retained under iterations/.

## Render and visual review
HyperFrames 0.8.46 lint/runtime/layout/contrast return zero errors. Layout retains two container-overflow warnings for the scene group that includes the offstage visitor during entry/exit; clipping to the garden stage is intentional. No blanket warning exclusions were added. Direct leaf/visitor bounds checks pass for their visible holds and camera transition.

Inspected browser snapshots across vein morph, copy lift, visitor return, camera midpoint and end. Inspected final encoded master samples every two seconds across the full duration, plus full-size camera midpoint and final copy/caption frames. Fixed leaves, retained originals, carried copies and final hold are visible. Brand-binding technical preflight passes; V5 reference material/local fonts/backdrop retained. These are technical and visual checks, not Andy's aesthetic approval or a claim of measured audience impact.

## Implementation limits and preservation
Spatial geometry uses a pinhole projection into SVG paths with depth ordering; the visitor is a camera-facing illustration rather than a fully modelled character. Lesson pictograms are illustrative. No sound design was added because it was not one of the three selected upgrades.

Only garden-library-v2 was changed. The original garden, approved-better garden-library-v1, parked cutout studies, Apple/Google/fishing demos, Resolve, parent review server, shared guidance and schedules remain untouched.
