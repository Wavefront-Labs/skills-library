---
id: creative-arts.animation.encode-delivery.full-vs-limited-range
name: full-vs-limited-range
category: creative-arts
field: animation
product: encode-delivery
tags: [video-range, pixel-format, full-range, limited-range, tv-range, pc-range, yuvj420p, crushed-blacks, washed-out, ffmpeg]
level: practitioner
status: verified
description: "Diagnose and fix full vs limited (TV/PC) range errors: crushed blacks, washed-out greys, yuvj formats, ffmpeg in_range/out_range and range tags."
sources:
  - https://ffmpeg.org/ffmpeg-scaler.html#scale-1
  - https://ffmpeg.org/ffmpeg-codecs.html#Codec-Options
  - https://www.itu.int/rec/R-REC-BT.709
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Full vs limited range

**Goal:** blacks at black and whites at white in every player. Video Y'CbCr normally uses
limited ("TV", "MPEG") range: 8-bit 16-235. Computer RGB and JPEG use full
("PC", "JPEG") range 0-255. Mismatches show as two classic symptoms:

| Symptom | Cause |
|---|---|
| Washed out, blacks look grey (16 shown as dark grey) | limited data shown as full |
| Crushed shadows, clipped highlights, too contrasty | full data shown as limited |

## Correct conversion from RGB renders

```bash
ffmpeg -framerate 24 -i f_%04d.png \
  -vf "scale=out_color_matrix=bt709:out_range=tv" -pix_fmt yuv420p \
  -c:v libx264 -crf 18 -color_range tv -colorspace bt709 -color_primaries bt709 -color_trc bt709 out.mp4
```

`out_range=tv` squeezes 0-255 RGB into 16-235 Y'; `-color_range tv` labels it. Both are needed.

## Fixing a file already wrong

Mislabelled (data correct, tag wrong) - retag without re-encoding:
```bash
ffmpeg -i in.mp4 -c copy -bsf:v h264_metadata=video_full_range_flag=0 fixed.mp4
```

Data wrong (full-range data tagged limited, e.g. from a `yuvj420p` JPEG/MJPEG pipeline):
```bash
ffmpeg -i in.mp4 -vf "scale=in_range=pc:out_range=tv" -pix_fmt yuv420p -color_range tv -c:v libx264 -crf 18 out.mp4
```

## Gotchas

- If the input is full-range YUV (for example from a JPEG/MJPEG pipeline), check `pix_fmt` and `color_range` first, then convert with `in_range=pc:out_range=tv` to limited-range `yuv420p`.
- A grade that leaves levels outside limited range (above 235 or below 16 at 8-bit) can clip on some devices. Legalise in the grade or with `-vf limiter` and check on a waveform.
- Do not "fix" range in a single player's settings; fix the file.

## Verify

```bash
ffprobe -v error -select_streams v:0 -show_entries stream=pix_fmt,color_range -of default=nw=1 out.mp4
ffmpeg -i out.mp4 -vf "signalstats,metadata=print" -frames:v 50 -f null - 2>&1 | grep -E "YMIN|YMAX" | tail -4
```

`metadata=print:key=` takes one key (a second `key=` replaces the first, so only YMAX printed); plain `print` lists all stats. Range tag `tv`; a frame with true black and white reads YMIN about 16 and YMAX about 235.

## Checked

2026-10-28. Confirmed: `scale` `in_range`/`out_range` values `tv`, `mpeg`, `pc`, `jpeg` and `out_color_matrix` (ffmpeg-filters); 8-bit limited range 16-235 and full 0-255 (ffmpeg colorspace wiki); `h264_metadata` `video_full_range_flag` (ffmpeg bitstream filters source); `limiter` and `signalstats` YMIN/YMAX exist. Removed: chroma 16-240, the yuvj420p deprecation claim, super-white 236-254, 10-bit 64-940.

2026-11-01 run check: the RGB-to-limited command, the `h264_metadata=video_full_range_flag=0` retag, the `in_range=pc:out_range=tv` fix and `-vf limiter` all ran; a black|white test image encoded with the first command measured YMIN=16 and YMAX=235; an `out_range=pc` / `yuvj420p` file probed as `yuvj420p`, `color_range=pc`. Fixed: the original `metadata=print:key=...:key=...` verify command printed only YMAX.

Method: commands run with ffmpeg 8.0.1 (Windows build) on synthetic lavfi inputs, plus the ffmpeg manuals for the options above.
