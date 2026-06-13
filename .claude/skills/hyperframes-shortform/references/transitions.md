# Transitions — vertical-first

Scene-to-scene motion. In portrait the rules are different from landscape: the **vertical axis is the energy axis** (it matches the thumb-scroll the viewer is already doing), and width is the scarce dimension. Don't port 16:9 horizontal whips into a 1080-wide frame — they read as wasted travel.

## 9:16 vs 16:9 — which transition reads right

| Transition | Reads in portrait? | Why |
|---|---|---|
| **Whip UP** (vertical) | ✅ best default | Matches thumb-scroll muscle memory; the eye is already moving up |
| Whip LEFT/RIGHT (horizontal) | ❌ avoid | Only ~1080px of travel; the streak barely registers before it's off-frame |
| **Zoom-punch** | ✅ aspect-agnostic | Scale reads the same in any aspect; lands on a beat |
| **Flash-through-white** | ✅ | Brightness cut hides the seam regardless of axis |
| **Glitch-cut** | ✅ (use sparingly) | Slice offsets are vertical-friendly; budget one per short |
| **Face-mode change** | ✅ (face-cam only) | The free transition — the mode morph IS the cut |
| Side-panel slide (L/R) | ⚠️ restage | Stack panels top/bottom instead — width is scarce |

**Rotation rule:** no two consecutive transitions the same flavor. Six identical cuts in a row is the #1 tell for AI editing. Rotate: whip-up → zoom-punch → flash → face-mode → whip-up …

---

## 1 · whip-up (the default cut)

Velocity-matched vertical whip — the outgoing beat rides up with blur, the incoming beat rises from below with matching blur, velocities matched at the cut so the eye reads one continuous motion. (Adapted from MOTION_PHILOSOPHY §2.4 "cut-the-curve vertical whip" + §3.9.) Put these on each scene's own wrapper.

```js
// EXIT — on the OUTGOING scene wrapper, at its local end:
tl.to("#scene-wrap", { y: -150, filter: "blur(30px)", duration: .33, ease: "power2.in" }, localEnd);

// ENTRY — on the INCOMING scene wrapper, at its local 0:
gsap.set("#scene-wrap", { y: 150, filter: "blur(30px)" });
tl.to("#scene-wrap", { y: 0, filter: "blur(0px)", duration: 1.0, ease: "power2.out" }, 0);
```

Comment the seam: name the matching tween in the adjacent beat (MOTION_PHILOSOPHY §3.15). If you can't name it, you haven't designed the seam.

## 2 · zoom-punch

Exit scales up and blurs; entry scales down to rest. Land the entry on a beat for a percussive cut.

```js
tl.to("#out-wrap", { scale: 1.18, filter: "blur(12px)", opacity: 0, duration: .25, ease: "power2.in" }, localEnd);
// incoming:
gsap.set("#in-wrap", { scale: 1.3, opacity: 0 });
tl.to("#in-wrap", { scale: 1, opacity: 1, filter: "blur(0px)", duration: .6, ease: "power3.out" }, 0);
```

## 3 · flash-through

White overlay ramps to full, the cut happens at peak brightness, then it ramps out. Hides the seam entirely. Or install the registry block: `npx hyperframes add flash-through-white`.

```js
// full-comp overlay on a high track-index:
tl.fromTo("#flash", { opacity: 0 }, { opacity: 1, duration: .12, ease: "power2.in" }, cutT - .12);
tl.to("#flash", { opacity: 0, duration: .2, ease: "power2.out" }, cutT);   // cut the underlying scene AT cutT
```

## 4 · glitch-cut (deterministic)

Slice offsets + RGB split + jitter straddling the cut. **Deterministic only** — hardcoded offset arrays and `steps()` eases, never `Math.random()`. Budget one per short.

```js
const SLICES = [ -18, 12, -8, 22, -4 ];   // hardcoded — deterministic
SLICES.forEach((dx, i) => {
  tl.set("#glitch", { x: dx, clipPath: "inset(" + (i * 20) + "% 0 " + (80 - i * 20) + "% 0)" }, cutT + i * .02);
});
tl.set("#glitch", { x: 0, clipPath: "inset(0 0 0 0)" }, cutT + SLICES.length * .02);
tl.fromTo("#glitch", { textShadow: "3px 0 #ff004c, -3px 0 #00e5ff" },   // RGB split
  { textShadow: "0 0 transparent", duration: .12, ease: "steps(3)" }, cutT);
```

## 5 · face-mode-transition (face-cam only)

When the face changes mode between adjacent scenes, the BOTTOM↔FULLSCREEN morph IS the transition — you get it for free. Full choreography (per-entry `dur`, the 0.25–0.30s pre-roll, the outgoing-panel fade+blur "three things at once" rule) is in `references/facecam.md`. Use it as one of your rotated flavors so you're not always reaching for an overlay.

---

## Registry transitions

Don't write what you can install — then decide which hero moments deserve a bespoke rebuild.

```bash
npx hyperframes add whip-pan            # if you want a packaged whip
npx hyperframes add flash-through-white # act breaks
npx hyperframes add sdf-iris            # iris reveal
npx hyperframes add push-up             # pure overlay scene-to-scene push (vertical-friendly)
npx hyperframes catalog --type block    # browse the full shader-transition pack
```

Scope every installed block's CSS to `[data-composition-id="..."]` immediately — catalog blocks ship `html, body { … }` rules that bleed into the parent when loaded as sub-compositions.
