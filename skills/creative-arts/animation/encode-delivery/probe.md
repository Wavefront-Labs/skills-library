---
id: creative-arts.animation.encode-delivery.probe
name: probe
category: creative-arts
field: animation
product: encode-delivery
tags: [ffprobe, ffmpeg, filmcraft, media, qc, duration, codec, loudness, ebur128, volumedetect, frame-count]
level: advanced
status: draft
description: "Inspect media with ffprobe/ffmpeg before publishing: streams, codec, fps, resolution, exact duration, frame counts, ebur128/volumedetect loudness."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# probe — sanity-check a render/cut before you publish

**Goal:** never ship a silent file, a dropped-frame shot, a 23.976 clip in a 24fps
timeline, or a master that's 3 LUFS off target. Probing is cheap; a re-upload after
viewers have seen the broken cut is not. The rule is **probe after every
render/mux/concat**, before the file moves to the next stage.

## In this pipeline

Grounded in `series/production/build_audio.py` → `dur(path)`, which is exactly the
canonical duration probe: machine-readable, one number, no noise.

```bash
ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 input.mp4
```

- `-v error` silences the banner so stdout is *only* the answer (scriptable).
- `-show_entries format=duration` pulls the container duration.
- `-of default=nk=1:nw=1` = no key, no wrapper → bare `12.480000`.

`build_audio.py` uses this to read the input length and raise if it's `<= 0`
(a zero/garbage duration means a broken or truncated file — catch it before you
spend an encode on it). Every stage that joins A to V should assert the two
durations agree.

## Full inspection (what each render/mux must pass)

```bash
# human-readable: all streams + format, one screen
ffprobe -hide_banner input.mp4

# machine-readable: just the facts you QC on, per stream
ffprobe -v error -select_streams v:0 \
  -show_entries stream=codec_name,profile,pix_fmt,width,height,r_frame_rate,nb_frames,duration \
  -of default=nw=1 input.mp4
ffprobe -v error -select_streams a:0 \
  -show_entries stream=codec_name,sample_rate,channels,duration \
  -of default=nw=1 input.mp4
```

Confirm, every time:

- **An audio stream exists.** The single most common ship-breaker is a silent file —
  a mux that mapped no audio still plays, just mute. `a:0` returning nothing = stop.
- **Video codec/profile/pix_fmt**: want `h264` / `High` / `yuv420p` for delivery
  (see `creative-arts.animation.encode-delivery.youtube-master`).
- **Resolution** `1920x1080`.
- **Frame rate** `r_frame_rate = 24/1` (not `24000/1001` = 23.976, and not a VFR
  mess). A mismatch between render fps and encode fps = progressive A/V drift.
- **Audio** `aac`, `48000`, `2` channels.

## Duration & frame-count sanity

`duration × fps == frame count`. If it's off, a shot dropped or duplicated frames.

```bash
# count real video frames (decodes; authoritative when container nb_frames lies)
ffprobe -v error -select_streams v:0 -count_frames \
  -show_entries stream=nb_read_frames -of default=nk=1:nw=1 input.mp4
```

- A per-shot clip assembled from `f_0001.png…` must have exactly as many frames as
  PNGs rendered. Fewer = a missing/failed frame; the `cinematic_render` output dir
  is the source of truth for the expected count.
- Episode duration must equal the **sum of the shot durations** on the shotlist.
  Concat drift (a frame added at each boundary) shows up here first.

## Loudness & audio level (before and after the master)

Verify the `loudnorm=I=-14:TP=-1.5` master from `build_audio.py` actually landed:

```bash
# EBU R128 integrated loudness + true peak (the YouTube-relevant numbers)
ffmpeg -hide_banner -nostats -i input.mp4 -af ebur128=peak=true -f null -
```

Read the summary tail: **I:** should be ~ -14 LUFS, **Peak:** ≤ -1.5 dBTP, LRA ~11.
For a quick "is it clipping / is it dead silent" check:

```bash
ffmpeg -hide_banner -i input.mp4 -af volumedetect -f null -
```

`max_volume` near `0.0 dB` = clipping risk; `mean_volume` extremely low / `-91 dB`
= effectively silent (another way to catch a dead audio stream that technically
exists). Use `ebur128` for the delivery decision, `volumedetect` for a fast gut check.

## Container vs stream duration, and VFR

The `format=duration` and each `stream=duration` can disagree — a container that's
0.5s longer than its video stream usually means a trailing silent audio tail or a
bad concat. Compare them:

```bash
ffprobe -v error -show_entries format=duration:stream=duration \
  -of default=nw=1 input.mp4
```

To catch **variable frame rate** (which breaks sync on YouTube and in editors),
check that `r_frame_rate` equals `avg_frame_rate`; if they differ the file is VFR
and must be re-rendered/transcoded to CFR 24. Inspect the first frames' timestamps
to confirm an even 1/24s cadence:

```bash
ffprobe -v error -select_streams v:0 -read_intervals %+#5 \
  -show_entries frame=pkt_pts_time,pict_type -of csv=p=0 input.mp4
```

PTS should step by ~0.0417s and the first frame should be an `I` (keyframe).

## Colour range and the PNG-sequence check

- **Colour range**: confirm `color_range=tv` (limited/16–235) for delivery; a render
  tagged `pc`/full that a player reads as `tv` washes blacks/whites. `-show_entries
  stream=color_range,color_space` surfaces it.
- **Before assembly**, sanity-check the PNG sequence the render produced: the count
  of `f_*.png` must equal the shot's expected frame span (`end-start+1` from
  `cinematic_render`). A gap in the numbering = a frame that never rendered; assembling
  it silently shortens the shot.

## Filmcraft equivalent

`<CRAFT_BIN>/filmcraft-cli.exe probe out.mp4` wraps the same checks (streams, codec,
duration, fps, resolution, audio presence) in one call for the standard render→probe
→assemble loop. Use whichever is in reach; the numbers to confirm are identical.

## Quick QC checklist you can paste into a review

- [ ] `format=duration` > 0 and == expected shot/episode length.
- [ ] Video: `h264 / High / yuv420p`, `1920x1080`, `r_frame_rate = 24/1`.
- [ ] Audio stream present: `aac / 48000 / 2ch`.
- [ ] `nb_read_frames` == duration × 24 == PNGs rendered (no dropped frames).
- [ ] `ebur128`: I ≈ -14 LUFS, true peak ≤ -1.5 dBTP.
- [ ] `volumedetect`: not clipping (`max_volume` < 0), not silent.
- [ ] A/V durations agree (no end-of-file lip-sync drift).

## Verify

- [ ] Every render/mux/concat is probed before it advances a stage.
- [ ] A failing probe stops the pipeline (raise, like `dur()` does on `<= 0`), it is
      never ignored.
- [ ] The delivery master passes all seven checklist lines above.

status draft: the duration probe is verified in-pipeline (`build_audio.dur`); the
stream/frame-count/loudness commands are standard ffprobe/ffmpeg and correct, not
yet wired into an automated gate. See
`creative-arts.animation.encode-delivery.youtube-master`.
