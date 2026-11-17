---
id: creative-arts.animation.encode-delivery.image-sequence-encode
name: image-sequence-encode
category: creative-arts
field: animation
product: encode-delivery
tags: [image-sequence-encode, image-sequence, image2, png-sequence, frame-padding, start-number, framerate, ffmpeg, glob, render-frames]
level: practitioner
status: verified
description: "Encode numbered render frames to video with ffmpeg image2: -framerate vs -r, padding patterns, start_number, globs, alpha, and frame-count checks."
sources:
  - https://ffmpeg.org/ffmpeg-formats.html#image2-1
  - https://trac.ffmpeg.org/wiki/Slideshow
  - https://ffmpeg.org/ffmpeg.html#Video-Options
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Encoding an image sequence

**Goal:** turn `shot010_v003.0001.png ... .0240.png` into a movie with exactly 240 frames at
the right rate, starting on the right frame.

## The command

```bash
ffmpeg -framerate 24 -start_number 1001 -i shot010_v003.%04d.png \
  -c:v libx264 -crf 16 -preset slow -pix_fmt yuv420p \
  -vf "scale=out_color_matrix=bt709" -colorspace bt709 -color_primaries bt709 -color_trc bt709 \
  shot010_v003.mp4
```

- `-framerate 24` is an **input** option: it tells image2 how to time the frames. Without it image2
  assumes 25 fps (ffprobe reported 25/1 for a 48-frame sequence). Set the rate with `-framerate`, not an output `-r`, which resamples: `-framerate 24` plus output `-r 30` turned 48 frames into 60.
- `%04d` matches zero-padded 4-digit numbers. Match your renderer's padding exactly (`%05d`,
  or `%d` for unpadded).
- `-start_number 1001` is needed when the first frame number is not 0-4 (image2 checks `start_number` through `start_number + start_number_range - 1`, default range 5). VFX convention starts shots at 1001 to leave handles.

Globs (not available on Windows builds, per the FFmpeg wiki):
```bash
ffmpeg -framerate 24 -pattern_type glob -i 'renders/*.png' ...
```
Glob order is not numeric, so check that unpadded names (`f_10.png`, `f_2.png`) come out in the right order; rename to padded first.

## Alpha and intermediates

```bash
# keep alpha for comp/edit
ffmpeg -framerate 24 -i f_%04d.png -c:v prores_ks -profile:v 4444 -pix_fmt yuva444p10le out.mov
# lossless archival of 8-bit frames
ffmpeg -framerate 24 -i f_%04d.png -c:v ffv1 -level 3 out.mkv
```

## Add audio while encoding

```bash
ffmpeg -framerate 24 -i f_%04d.png -i mix.wav -map 0:v -map 1:a -c:v libx264 -crf 18 \
  -pix_fmt yuv420p -c:a aac -b:a 192k -shortest out.mp4
```

## Gotchas

- A gap in numbering ends the movie at the gap (a sequence of 47 files missing number 10 gave a 9-frame movie). Check counts first
  (`creative-arts.animation.encode-delivery.missing-frame-detection`).
- When converting 16-bit frames to 8-bit, dither in the scaler (`sws_dither=ed`, error diffusion).
- `yuv420p` needs even dimensions. ffmpeg 8.0.1 cropped a 321x241 PNG to 320x240 without an error (other builds or encoders may refuse), so pad or scale to even yourself.

## Verify

```bash
ls shot010_v003.*.png | wc -l
ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames,r_frame_rate -of default=nw=1 shot010_v003.mp4
```

Frame counts equal, rate `24/1`.

## Checked

2026-10-28. Confirmed: image2 `start_number` and `start_number_range` (default 5) and default frame rate 25 (ffmpeg-formats); `-pattern_type glob` and its Windows limitation (ffmpeg Slideshow wiki); `scale` `sws_dither=ed`; prores_ks profile `4444` (ffmpeg-codecs); ffprobe `-count_frames` and `nb_read_frames`. Removed: the lexical-sort claim, the silent-stop wording for gaps, the rgb48 statement.

Run 2026-11-01 with ffmpeg and ffprobe 8.0.1 on Windows (Git Bash), scripts in a scratch folder: the main command on a 48-frame sequence numbered 1001 to 1048 (48 frames at 24/1), the same without `-framerate` (25/1), numbering that starts at 1001 without `-start_number` (fails: no such file), `-pattern_type glob` (fails on this Windows build: Function not implemented), prores_ks 4444 with `yuva444p10le`, ffv1 level 3, audio muxing with `-shortest`, the numbering gap and the odd-size input. Not run: 16-bit sources and the `ls | wc -l` count.

Method: documentation plus commands run (ffmpeg 8.0.1).
