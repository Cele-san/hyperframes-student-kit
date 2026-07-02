# AIDR cutaways — SFX plan

**Delivery:** one SFX stem WAV per part (`renders/sfx/<part>-sfx.wav`, same length as the part),
placed on A2 in Resolve at the same recordFrame as its V2 insert. VO stays on A1 untouched.
**Loudness law:** SFX never louder than the talent. Gains staged vs the MEASURED v5 VO peak
(hero ≈ VO−5 dB, standard ≈ VO−7..9, beds ≈ VO−11..13), auditioned in QuickTime before finals.
Whole-mix loudnorm is NOT ours here — Resolve owns the final mix; stems are pre-gained.

## Cue tables (times local to each part)

### b0-twofates (12s) — 7 cues
| t | class | event |
|---|---|---|
| 2.0 | whoosh-med | the split — one gesture, two fates |
| 3.55 | pop | slab seals shut |
| 4.7 | whoosh-exit | right copy explodes into clips |
| 7.35 | strike | bad-cut flash (both copies) |
| 8.7 | click-pop | cursor grabs the clip edge |
| 9.15 | tick | the skip heals |
| 10.05 | twinkle | editable side glows (payoff) |

### b3-wordrain (8s) — 5 cues
| t | class | event |
|---|---|---|
| 0.4–2.0 | data-whir (bed, low) | word cloud tumbles in |
| 2.3–4.9 | typing slice | words snapping to the ruler (keystrokes = landings) |
| 2.6 | whoosh-exit (soft) | ruler draws through |
| 5.35–6.85 | data-whir (rise) | playhead scrubs the ruler |
| 6.9 | twinkle | lattice fully addressed (payoff) |

### b3-cutter (14s) — ~11 cues
| t | class | event |
|---|---|---|
| 0.55 / 0.95 | pop ×2 | YOUR SCRIPT / YOUR FOOTAGE chips |
| 1.9 | whoosh-med | chips converge into the bar |
| 2.25–3.1 | data-whir (bed) | bar assembles |
| 4.54 | stamp-ink (HERO) | first blade stamp (slate) |
| 5.6 / 7.32 / 8.44 / 9.5 | strike ×4 | remaining stamps (attempt, slate, flub, dead air) — approx times, derive from walk math |
| 11.35 | whoosh-med | healed bar recenters |
| 11.9 | click-pop | settle |
| 12.2 | twinkle | take-by-take flush (payoff) |

### b3-tower (9s) — ~9 cues
| t | class | event |
|---|---|---|
| 0.4–1.6 | data-whir (bed) | tower assembles |
| 1.1 | blip | counter lands 13:16 |
| 2.4 / 4.0 / 5.8 | tick ×3 | pass labels in |
| 2.55 / 4.15 / 5.95 | whoosh-exit ×3 | blocks kicked out (first block of each pass) |
| 7.35 | stamp-ink (HERO) | shockwave off the 8:17 |
| 7.6 | twinkle | counter turns blossom |

### b5-relay (10s) — ~9 cues
| t | class | event |
|---|---|---|
| 0.45 | data-whir (soft) | lanes in |
| 0.9–2.6 | typing slice | junior assembling blocks (rhythm) |
| 3.2 | whoosh-med | handoff rises to senior lane |
| 4.35 / 6.35 / 7.95 | whoosh-exit (soft) ×3 | camera leans in per fix |
| 5.25 | pop | rough block drops |
| 7.05 / 8.55 | tick ×2 | align fix / trim fix |
| 9.1 | twinkle | shipped glow (payoff) |

### b7-asymptote (8s) — 6 cues
| t | class | event |
|---|---|---|
| 0.8–3.4 | data-whir (rise) | curve climbs |
| 3.55 | blip | gap bracket appears |
| 3.6 | whoosh-exit | ceiling escapes upward |
| 4.5–6.2 | data-whir (low) | second climb |
| 6.15 | whoosh-exit (shorter/softer) | second escape |
| 6.8 | twinkle | endlab + tip breath (payoff) |

## Notes
- Hero class (stamp-ink) reserved for exactly 2 moments across the whole package:
  cutter first stamp + tower shockwave.
- Typing slices rotate offsets (0.0 / 1.2 / 2.4 / 3.5 / 4.6) — never verbatim repeats.
- Collision rule: <0.3s apart → keep the more meaningful cue (strike beats tick).
- Exact stamp times for b3-cutter derive from the walk math (t=4.1 start; travel .44;
  debris +.62, keep +.10) → stamps at 4.54, 5.60, 6.66, 8.30, 9.94. Update table at build.
