# Motion proof review

Delivered: garden-cutout-motion-v1.mp4. Verified encoded 1920x1080, 30 fps, 14 seconds, 420 frames, no audio stream, 4,286,559 bytes.

HyperFrames check: lint, runtime and layout pass with zero errors. One remaining duplicate-media warning is expected: the same library sprite is deliberately reused under separate spatial masks, each with a unique ID. Assets remain local; large-background non-inlining notice does not affect local rendering.

Inspected initial browser snapshots and encoded one-second samples across the entire video, including fold, transition, sequential collection reveal and final hold. Initial opaque crop seams were found and fixed by generating a transparent library overlay. No opaque rectangular patches remain in sampled encoded frames. Alpha verified from source PNG channels.

This is a silent motion proof, not a finished narrated demo or editorial approval. The overhead transition uses a matched cut at 6.8 seconds, not a continuous 3D camera move. Some stem segments remain absent until their connecting layer arrives. The fold uses a clipped cover rotating over the generated open pose; it is not a simulated physical sheet. Those are the specific limitations to judge before refining production assets.

Original storyboard, narration and other demos preserved. No Resolve access.
