#!/bin/bash
# render-ov.sh <ov-asset-name> — renders a text-overlay part to the overlays/ delivery folder.
# ProRes 4444 alpha .mov, 1920x1080, 29.97 (30000/1001). Sequential batch only.
set -euo pipefail
P="$(cd "$(dirname "$0")" && pwd)"
OUT_DIR=/Users/andydepp/Projects/OperatorOS/videos/2026-07-31-chatgpt-56-sol-vs-fable-5-first-pass-comparison/05-motion-assets/hyperframes/overlays

NAME="$1"
SRC="$P/compositions/$NAME.html"
[ -f "$SRC" ] || { echo "MISSING composition: $SRC" >&2; exit 1; }
mkdir -p "$OUT_DIR"

cp "$SRC" "$P/index.html"
cd "$P"
npx --yes hyperframes@0.7.42 render -o "$OUT_DIR/$NAME.mov" --format mov -f 30000/1001 --quality high 2>&1 \
  | grep -viE "Render:trace|initSession|Capturing frame|Encoding video|Assembling" | tail -4
echo "OUT=$OUT_DIR/$NAME.mov"
