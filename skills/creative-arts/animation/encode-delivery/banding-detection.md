---
id: creative-arts.animation.encode-delivery.banding-detection
name: banding-detection
category: creative-arts
field: animation
product: encode-delivery
tags: [banding, encode-quality, debanding, gradfun, deband, contouring, gradients, dither, grain, ffmpeg]
level: advanced
status: verified
description: "Find and prevent gradient banding in animation encodes: where it comes from, how to spot it, deband/gradfun filters, dither and grain strategy before the final encode."
sources:
  - https://ffmpeg.org/ffmpeg-filters.html#deband
  - https://ffmpeg.org/ffmpeg-filters.html#gradfun
  - https://github.com/Netflix/vmaf
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Banding detection and prevention

**Goal:** smooth skies, glows, fog and vignettes in the delivered file. Banding (contouring) is
the top visual complaint on animated content: large smooth gradients with few code values, then
an encoder that flattens the subtle noise that hid the steps.

## Where banding is born (fix the earliest)

1. **Render/comp in 8-bit**: steps baked in. Render 16-bit or float.
2. **Grade pushes a gradient** (contrast up on a sky) in 8-bit: steps stretched. Grade in float.
3. **Final quantise to 8-bit without dither**. Dither once (`sws_dither=ed`).
4. **Encoder** removes dither noise at low bitrates.
5. **Platform re-encode** of your upload (out of your control; give it a clean 10-bit mezzanine).

## Spotting it

- View gradient shots at 100-200% on a calibrated display with brightness raised slightly;
  steps show as concentric rings or vertical bars.
- Exaggerate: `ffmpeg -i out.mp4 -vf "eq=contrast=4:brightness=0.1" -frames:v 1 -ss 30 check.png`
  makes banding obvious in a still.
- Compare 8-bit H.264 vs 10-bit HEVC of the same shot side by side.

## Fixes at encode

```bash
# deband (replaces banded pixels with the average of referenced pixels), then encode
ffmpeg -i master.mov -vf "deband=1thr=0.02:2thr=0.02:3thr=0.02:range=16:blur=1,format=yuv420p" \
  -c:v libx264 -crf 16 -tune animation out.mp4
```
- `deband` replaces banded pixels with the average value of referenced pixels; `1thr`/`2thr`/`3thr` default to 0.02, `range` to 16 and `blur` is enabled by default (ffmpeg-filters).
- Better: switch delivery to 10-bit HEVC/AV1 (`creative-arts.animation.encode-delivery.ten-bit-encoding`).

## Grain as protection

Adding fine grain, animated per frame, in comp can mask steps. It costs bitrate; test on the target platform.

## Gotchas

- Deband blurs fine texture; limit to shots that need it or use a mask.
- VMAF is not a banding detector (the libvmaf README mentions a separate banding metric, CAMBI); do not use VMAF alone as the gate for this fault.

## Verify

Exaggerated-contrast stills of the three worst gradient shots show no visible steps in the final
deliverable, and after a private test upload to the target platform.

## Checked

2026-10-28. Confirmed: ffmpeg `deband` option names and defaults, `scale` `sws_dither=ed` (error diffusion), libx264 `-tune animation`, libvmaf README banding-metric mention (CAMBI). Removed: `-aq-mode 3` and its description (the fetched manual lists aq-mode only for other encoders), the grain percentages, the claim that banding is worst at 8-bit 4:2:0 H.264, the 'barely notices' VMAF claim.

Run 2026-11-01 with ffmpeg and ffprobe 8.0.1 on Windows (Git Bash), scripts in a scratch folder: the `deband` command (`ffmpeg -h filter=deband` shows 1thr/2thr/3thr default 0.02, range 16, blur true), the `eq` exaggeration still, `gradfun`, `-tune animation` and `sws_dither=ed` (listed by `-h filter=scale`) all ran without error. Not run: the visual judgement of banding itself, the CAMBI metric and platform re-encodes.

Method: documentation plus commands run (ffmpeg 8.0.1).
