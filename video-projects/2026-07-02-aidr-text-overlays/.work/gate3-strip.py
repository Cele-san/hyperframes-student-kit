#!/usr/bin/env python3
"""Gate 3 reference-layer stripper. For each part, write a non-destructive
index.alpha.html = index.html with the REFERENCE LAYER block removed, so the
alpha .mov renders overlays-only over transparency. Canonical index.html is
never mutated. Usage: python3 .work/gate3-strip.py [slug ...]  (no args = all)"""
import os, re, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# match the START comment (no nested <!-- before the marker) ... END comment's closing -->
BLOCK = re.compile(
    r'<!--(?:(?!<!--).)*?REFERENCE LAYER START.*?REFERENCE LAYER END(?:(?!-->).)*?-->',
    re.DOTALL)

want = sys.argv[1:] or [os.path.basename(os.path.dirname(p))
                        for p in sorted(glob.glob(os.path.join(ROOT, 'parts', 'part-0*', 'index.html')))]

for slug in want:
    f = os.path.join(ROOT, 'parts', slug, 'index.html')
    src = open(f).read()
    n = len(BLOCK.findall(src))
    if n != 1:
        print(f"!! {slug}: expected 1 reference block, found {n} — SKIPPED"); continue
    out = BLOCK.sub('<!-- reference layer stripped for alpha export -->', src)
    # safety assertions
    bad = [t for t in ('ref-video', 'ref-audio', 'proxy.mp4') if t in out]
    need = [t for t in ('data-composition-id', 'window.__timelines') if t not in out]
    if bad or need:
        print(f"!! {slug}: strip unsafe (residual={bad}, missing={need}) — SKIPPED"); continue
    open(os.path.join(ROOT, 'parts', slug, 'index.alpha.html'), 'w').write(out)
    print(f"{slug:34s} stripped OK  ({len(src)-len(out)} chars removed)  -> index.alpha.html")
