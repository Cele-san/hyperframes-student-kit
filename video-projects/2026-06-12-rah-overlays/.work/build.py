#!/usr/bin/env python3
"""RAH overlay composite — Track B final assembly.

Video: 10 ProRes 4444 alpha parts overlaid onto the locked master at their
boundary start times (master video is decoded once, never pre-processed).
Audio: master VO + 59 SFX cues (REV 5 locked gains, .work/sfx-plan.md), mixed
first, then two-pass loudnorm to YouTube reference (I=-14, TP=-1.5, LRA=11).

Usage: python3 .work/build.py [--output renders/rah-composite.mp4] [--crf 18]
Run from the project root (video-projects/2026-06-12-rah-overlays).
"""
import argparse, glob, json, pathlib, re, subprocess, sys

MASTER = glob.glob(
    "/Users/andydepp/Projects/OperatorOS/videos/"
    "2026-06-26-reading-ai-output-as-html-claude-artifacts/Exports/RAH_main*V2*.mp4"
)[0]

PARTS = [  # (slug, master start_s) — from boundaries.json
    ("p01-hook", 0.0), ("p02-doors", 56.99), ("p03-the-turn", 89.09),
    ("p04-lives", 132.43), ("p05-ladder", 155.49), ("p06-cost", 208.61),
    ("p07-smallest", 262.434), ("p08-system", 298.63), ("p09-thesis", 341.31),
    ("p10-bookend", 372.371),
]

SFX = "assets/sfx"
# (file, REV-5 gain dB) — see .work/sfx-plan.md. chime-send carries Andy's -4.
GAIN = {
    "typing":  (f"{SFX}/typing-keys.mp3", -22.3),
    "chime":   (f"{SFX}/chime-send.mp3", -19.6),
    "stamp":   (f"{SFX}/stamp-ink.mp3", -15.3),
    "stamp2":  (f"{SFX}/stamp-ink.mp3", -19.3),
    "twang":   (f"{SFX}/wire-twang.mp3", -5.5),
    "pen":     (f"{SFX}/pen-underline.mp3", -8.4),
    "pop":     (f"{SFX}/click-pop.wav", -8.4),
    "tick":    (f"{SFX}/tick-pill.wav", 11.2),
    "blip":    (f"{SFX}/bubble-blip.wav", 1.9),
    "strike":  (f"{SFX}/strike-soft.wav", 7.3),
    "twinkle": (f"{SFX}/twinkle-skill.mp3", 7.8),
    "wh-s":    (f"{SFX}/whoosh-exit.wav", -18.6),  # Woosh Effect 8 — Andy picked #3, class-wide
    "wh-m":    (f"{SFX}/whoosh-med.wav", -14.8),
    "whir":    (f"{SFX}/data-whir.wav", -8.5),
}

# (master_time, kind, typing_slice) — typing_slice = (src_offset, dur) or None.
CUES = [
    # P01
    (8.85, "blip", None), (17.75, "pen", None), (26.90, "wh-s", None),
    (42.14, "stamp", None), (49.60, "wh-m", None), (52.05, "tick", None),
    # P02
    (65.04, "wh-m", None), (76.94, "twang", None), (78.24, "strike", None),
    (80.64, "stamp2", None), (82.99, "wh-s", None), (85.89, "pop", None),
    # P03
    (91.29, "pen", None), (95.29, "typing", (0.0, 1.3)), (96.92, "typing", (1.2, 0.85)),
    (99.19, "wh-s", None), (107.84, "tick", None), (122.79, "tick", None),
    # P04
    (137.73, "pop", None), (140.93, "tick", None), (141.98, "tick", None),
    (143.38, "tick", None), (148.53, "wh-s", None),
    # P05 (pill #3 cut — no cues 16.1/18.4; jargon slice gets extra -2 dB below)
    (160.49, "typing", (2.4, 2.4)), (164.29, "blip", None), (165.09, "chime", None),
    (180.79, "typing", (0.0, 4.1)), (192.19, "strike", None), (201.34, "twinkle", None),
    # P06 (callout cut — no cue 246.91)
    (214.11, "tick", None), (217.91, "tick", None), (222.41, "tick", None),
    (243.61, "pop", None), (249.61, "pop", None), (255.81, "tick", None),
    # P07 (dot-3 silent under the ticker dim)
    (265.13, "pop", None), (269.43, "tick", None), (275.73, "typing", (1.2, 2.1)),
    (278.83, "chime", None),
    # P08
    (301.33, "typing", (3.5, 2.7)), (304.23, "chime", None), (305.03, "twinkle", None),
    (323.63, "tick", None), (332.53, "whir", None),
    # P09
    (344.76, "wh-m", None), (350.41, "wh-m", None), (350.51, "whir", None),
    (353.51, "tick", None), (354.71, "pop", None), (363.21, "wh-s", None),
    (366.66, "strike", None), (366.76, "typing", (4.6, 1.25)), (369.16, "wh-s", None),
    # P10
    (377.32, "blip", None), (383.37, "strike", None), (383.82, "tick", None),
    (394.37, "typing", (0.0, 1.42)), (396.09, "chime", None),
    (399.92, "typing", (2.4, 0.85)), (401.52, "chime", None),
]
JARGON_EXTRA_DB = -2.0  # the long verbatim-quote typing slice at 180.79

LOUDNORM = "I=-14:TP=-1.5:LRA=11"


def audio_graph(base=11):
    """Audio filtergraph lines; audio file k maps to ffmpeg input index base+k."""
    files = []           # unique audio file -> input index (filled by caller)
    order = []           # unique files in first-use order
    uses = {}            # file -> number of cue uses
    for _, kind, _ in CUES:
        f = GAIN[kind][0]
        if f not in uses:
            order.append(f)
        uses[f] = uses.get(f, 0) + 1

    lines, cue_labels = [], []
    counters = {f: 0 for f in order}
    # asplit each unique file into one stream per use
    split_done = set()
    for ci, (t, kind, sl) in enumerate(CUES):
        f, gain = GAIN[kind]
        if f not in split_done:
            idx = order.index(f) + base  # full build: 0 master, 1-10 movs, 11+ audio
            outs = "".join(f"[u{order.index(f)}_{k}]" for k in range(uses[f]))
            lines.append(f"[{idx}:a]asplit={uses[f]}{outs}")
            split_done.add(f)
        k = counters[f]; counters[f] += 1
        src = f"[u{order.index(f)}_{k}]"
        chain = []
        if sl is not None:
            off, dur = sl
            chain.append(f"atrim={off}:{off + dur}")
            chain.append("asetpts=PTS-STARTPTS")
            chain.append("afade=t=in:d=0.03")
            chain.append(f"afade=t=out:st={max(dur - 0.08, 0):.2f}:d=0.08")
        g = gain + (JARGON_EXTRA_DB if (sl and abs(t - 180.79) < 0.01) else 0)
        chain.append(f"volume={g}dB")
        chain.append(f"adelay={round(t * 1000)}:all=1")
        lbl = f"[c{ci}]"
        lines.append(f"{src}{','.join(chain)}{lbl}")
        cue_labels.append(lbl)

    # mix in two beds (amix input caps), then with the VO; normalize=0 everywhere
    half = len(cue_labels) // 2
    lines.append(f"{''.join(cue_labels[:half])}amix=inputs={half}:duration=longest:normalize=0[bed1]")
    lines.append(f"{''.join(cue_labels[half:])}amix=inputs={len(cue_labels) - half}:duration=longest:normalize=0[bed2]")
    lines.append("[0:a][bed1][bed2]amix=inputs=3:duration=first:normalize=0[mix]")
    return order, lines


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", default="renders/rah-composite.mp4")
    ap.add_argument("--crf", default="18")
    ap.add_argument("--preset", default="medium")
    ap.add_argument("--remux-video", help="existing composite mp4 — re-mix audio only, copy its video stream")
    args = ap.parse_args()
    pathlib.Path("renders").mkdir(exist_ok=True)

    if args.remux_video:
        afiles, alines = audio_graph(base=1)  # 0 master, 1.. audio files
        cmd1 = ["ffmpeg", "-y", "-i", MASTER]
        for f in afiles: cmd1 += ["-i", f]
        fg1 = ";".join(alines + [f"[mix]loudnorm={LOUDNORM}:print_format=json[aout]"])
        cmd1 += ["-filter_complex", fg1, "-map", "[aout]", "-f", "null", "-"]
        print("pass 1 (remux): measuring mix loudness…", flush=True)
        r = subprocess.run(cmd1, capture_output=True, text=True)
        mjson = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", r.stderr, re.S)
        assert mjson, "loudnorm json not found:\n" + r.stderr[-2000:]
        m = json.loads(mjson.group(0))
        ln2 = (f"loudnorm={LOUDNORM}:measured_I={m['input_i']}:measured_TP={m['input_tp']}"
               f":measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}"
               f":offset={m['target_offset']}")
        vid_idx = 1 + len(afiles)
        cmd2 = ["ffmpeg", "-y", "-i", MASTER]
        for f in afiles: cmd2 += ["-i", f]
        cmd2 += ["-i", args.remux_video]
        fg2 = ";".join(alines + [f"[mix]{ln2}[aout]"])
        cmd2 += ["-filter_complex", fg2, "-map", f"{vid_idx}:v", "-map", "[aout]",
                 "-c:v", "copy", "-movflags", "+faststart", "-c:a", "aac", "-b:a", "256k",
                 args.output]
        print("pass 2 (remux): re-mixing audio over copied video…", flush=True)
        subprocess.run(cmd2, check=True)
        print("done:", args.output)
        return

    movs = [f"parts/{slug}/renders/{slug}-alpha.mov" for slug, _ in PARTS]
    for m in movs:
        assert pathlib.Path(m).is_file(), f"missing alpha: {m}"

    # probe part durations for enable windows
    durs = []
    for m in movs:
        d = float(subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "csv=p=0", m], capture_output=True, text=True).stdout.strip())
        durs.append(d)

    afiles, alines = audio_graph()

    # ---- pass 1: measure loudness of the mix (audio only) ----
    cmd1 = ["ffmpeg", "-y", "-i", MASTER]
    for m in movs: cmd1 += ["-i", m]
    for f in afiles: cmd1 += ["-i", f]
    fg1 = ";".join(alines + [f"[mix]loudnorm={LOUDNORM}:print_format=json[aout]"])
    cmd1 += ["-filter_complex", fg1, "-map", "[aout]", "-f", "null", "-"]
    print("pass 1: measuring mix loudness…", flush=True)
    r = subprocess.run(cmd1, capture_output=True, text=True)
    mjson = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", r.stderr, re.S)
    assert mjson, "loudnorm json not found:\n" + r.stderr[-2000:]
    m = json.loads(mjson.group(0))
    print("  measured:", {k: m[k] for k in ("input_i", "input_tp", "input_lra", "input_thresh")})

    ln2 = (f"loudnorm={LOUDNORM}:measured_I={m['input_i']}:measured_TP={m['input_tp']}"
           f":measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}"
           f":offset={m['target_offset']}")

    # ---- pass 2: full composite ----
    vlines, cur = [], "[0:v]"
    for k, ((slug, start), d) in enumerate(zip(PARTS, durs), start=1):
        nxt = f"[v{k}]" if k < len(PARTS) else "[vout]"
        vlines.append(f"[{k}:v]setpts=PTS-STARTPTS+{start}/TB[o{k}]")
        vlines.append(f"{cur}[o{k}]overlay=0:0:eof_action=pass:"
                      f"enable='between(t,{start},{start + d})'{nxt}")
        cur = f"[v{k}]"

    cmd2 = ["ffmpeg", "-y", "-i", MASTER]
    for mv in movs: cmd2 += ["-i", mv]
    for f in afiles: cmd2 += ["-i", f]
    fg2 = ";".join(vlines + alines + [f"[mix]{ln2}[aout]"])
    cmd2 += ["-filter_complex", fg2, "-map", "[vout]", "-map", "[aout]",
             "-c:v", "libx264", "-preset", args.preset, "-crf", args.crf,
             "-pix_fmt", "yuv420p", "-movflags", "+faststart",
             "-c:a", "aac", "-b:a", "256k", args.output]
    print("pass 2: compositing…", flush=True)
    subprocess.run(cmd2, check=True)
    print("done:", args.output)


if __name__ == "__main__":
    main()
