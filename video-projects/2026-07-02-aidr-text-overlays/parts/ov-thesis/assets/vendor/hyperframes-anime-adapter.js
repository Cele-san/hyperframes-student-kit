/* ============================================================================
   hyperframes ↔ anime.js v4 engine adapter
   ----------------------------------------------------------------------------
   Lets you author a hyperframes composition with anime.js v4 instead of GSAP,
   and render it through the STOCK (sealed) hyperframes CLI — no fork required.

   Why this works:
   The hyperframes renderer (HeyGen CLI + Playwright) is engine-agnostic about
   the object it finds on window.__timelines[id]. Per the render contract it only
   needs two things from that object, in SECONDS:
       • duration()      — read once, to know the frame count
       • seek(seconds)   — called once per frame, then it screenshots
   (CLAUDE.md: "Composition duration = `tl.duration()`".)

   GSAP timelines speak seconds; anime.js timelines speak milliseconds and use a
   `duration` PROPERTY + `seek(ms)`. This facade bridges the two: it exposes the
   GSAP time-control surface and forwards to an anime.js Timeline. Everything
   else in the contract (class="clip", data-start/duration, sub-compositions,
   audio) is engine-agnostic and unchanged — this swaps ONLY the animation engine.

   Usage (ergonomic):
       import { createComposition } from './hyperframes-anime-adapter.js';
       const { tl } = createComposition('my-id', { duration: 6, defaults: { ease: 'out(3)' } });
       tl.add('.title', { opacity: [0, 1], y: [20, 0], duration: 500 }, 0);
       // auto-registered, paused, on window.__timelines['my-id']

   Usage (wrap a timeline you already built):
       import { createTimeline } from './anime.esm.js';
       import { wrap, register } from './hyperframes-anime-adapter.js';
       const tl = createTimeline({ autoplay: false });  ...build...
       register('my-id', wrap(tl, { duration: 6 }));
   ========================================================================== */

import { createTimeline } from './anime.esm.js';

const SEC = 1000; // anime.js works in ms; hyperframes/GSAP in seconds

/**
 * Wrap an anime.js v4 Timeline in a GSAP-compatible time-control facade.
 * @param {object} animeTimeline an anime.js Timeline (should be autoplay:false)
 * @param {{duration?:number}} [opts] duration in SECONDS to anchor the
 *        composition length (so a short timeline doesn't truncate the video —
 *        mirrors hyperframes' `tl.to({}, {duration:N})` padding idiom).
 */
export function wrap(animeTimeline, opts = {}) {
  const tl = animeTimeline;
  const anchorMs = opts.duration != null ? opts.duration * SEC : 0;
  let cur = 0; // last seeked time, in seconds (don't rely on internal fields)

  // computed live so it reflects timeline content added AFTER wrapping
  const durSec = () => Math.max(tl.duration || 0, anchorMs) / SEC;
  const clamp = (s) => Math.min(Math.max(Number(s) || 0, 0), durSec());

  const facade = {
    /* identity / introspection */
    __engine: 'anime.js-v4',
    __anime: tl,
    paused: true,

    /* duration — GSAP exposes these as methods returning seconds */
    duration() { return durSec(); },
    totalDuration() { return durSec(); },

    /* the one the renderer calls per frame */
    seek(seconds) { cur = clamp(seconds); tl.seek(cur * SEC); return facade; },

    /* GSAP time-control aliases (getter when no arg, setter when arg given) —
       belt-and-suspenders so the facade works whichever the CLI happens to use */
    time(seconds) { return seconds === undefined ? cur : facade.seek(seconds); },
    totalTime(seconds) { return seconds === undefined ? cur : facade.seek(seconds); },
    progress(p) {
      const d = durSec();
      if (p === undefined) return d ? cur / d : 0;
      return facade.seek((Number(p) || 0) * d);
    },

    /* playback control — the framework owns playback, so play() is a deliberate
       no-op to preserve determinism (a self-running tween would fight the
       renderer's per-frame seek). */
    pause() { if (typeof tl.pause === 'function') tl.pause(); facade.paused = true; return facade; },
    play() { return facade; },
    restart() { return facade.seek(0); },
    kill() { return facade; },
  };

  return facade;
}

/** Register a facade (or any timeline-like object) on window.__timelines[id]. */
export function register(id, facade) {
  if (typeof window === 'undefined') return facade;
  window.__timelines = window.__timelines || {};
  window.__timelines[id] = facade;
  return facade;
}

/**
 * Convenience: create a paused anime.js timeline + wrap + register in one call.
 * @returns {{ tl: object, facade: object }} `tl` is the raw anime.js Timeline —
 *          build your animation on it with anime.js's native .add() API.
 */
export function createComposition(id, opts = {}) {
  const tl = createTimeline({ autoplay: false, defaults: opts.defaults || {} });
  const facade = wrap(tl, { duration: opts.duration });
  register(id, facade);
  return { tl, facade };
}
