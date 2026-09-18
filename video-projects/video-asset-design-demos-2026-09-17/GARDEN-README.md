# Garden demo handoff

Current review candidate: **garden-library-v2**. It contains the three selected upgrades: persistent leaf veins morph into lessons, a continuous perspective camera rises over fixed plant positions, and a visitor takes copies while the original lessons remain intact.

- [Latest review](garden-library-v2/review.html), [clean master](garden-library-v2/master.mp4), [captioned timing preview](garden-library-v2/timing-preview.mp4).
- [Previous smooth version](garden-library-v1/review.html), retained for comparison.
- [Ten original concepts](garden-concepts/TEN-CONCEPTS.md).
- Parked experiment: [cutout storyboard](garden-concepts/cutout-test-v1/index.html) and [stop-motion proof](garden-concepts/cutout-motion-v1/review.html). It was explored, then parked; it is not the selected direction.

V2 is a 30-second, 1920x1080, 30 fps silent render. The separate preview adds the unchanged narration beneath the picture. Narration is unrecorded and final voice alignment remains pending. Detailed design and verification notes live beside each composition. No performance metrics or editorial approval are inferred from technical checks.

## Preview and reproduce

Open a review HTML file locally or serve this folder through a local static server. The review pages link only to bundled assets. From the repository root, install the existing development dependencies with `npm ci` and install Playwright Chromium with `npx playwright install chromium` to run the dedicated geometry checks. Python 3 with Pillow and FFmpeg are required only to regenerate caption strips.

From `garden-library-v2/`:

```sh
npx --yes hyperframes@0.8.46 check --json
node verify.cjs
npx --yes hyperframes@0.8.46 render --quality standard --fps 30 --output "$PWD/master.mp4"
python3 package_preview.py
```

Set `PLAYWRIGHT_CHANNEL=chrome` when deliberately testing with an installed Google Chrome instead of Playwright's bundled Chromium. V1 uses `node verify-seeking.cjs`. The composition and its local fonts, tokens, background, and runtime travel together; no OperatorOS checkout or absolute user directory is required for playback.

`SHA256SUMS` records the shipped payload. Generated snapshots, failed passes, render logs, and caption intermediates are excluded from this package and remain preserved in the canonical local project. The original garden demo and the Apple, Google, fishing, Resolve, and other project work were not included or changed.
