---
id: creative-arts.animation.encode-delivery.psnr-ssim-measurement
name: psnr-ssim-measurement
category: creative-arts
field: animation
product: encode-delivery
tags: [psnr-ssim, encode-quality, psnr, ssim, ms-ssim, quality-metric, ffmpeg, regression-test, render-diff]
level: practitioner
status: docs-checked
description: "Use PSNR and SSIM in ffmpeg for fast encode and render regression checks: per-frame logs, what values mean, and when to prefer VMAF or a pixel diff."
sources:
  - https://ffmpeg.org/ffmpeg-filters.html#psnr
  - https://ffmpeg.org/ffmpeg-filters.html#ssim
  - https://ece.uwaterloo.ca/~z70wang/research/ssim/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PSNR and SSIM measurement

**Goal:** cheap, deterministic similarity numbers for regression tests: did a pipeline change
(new encoder version, new colour transform, different renderer build) alter the output, and
by how much. PSNR and SSIM are ffmpeg filters (`psnr`, `ssim`); use them for "same or different" and VMAF for "how good".

## Commands

```bash
# PSNR with per-frame log
ffmpeg -i new.mp4 -i ref.mp4 -lavfi "[0:v][1:v]psnr=stats_file=psnr.log" -f null -
# SSIM with per-frame log
ffmpeg -i new.mp4 -i ref.mp4 -lavfi "[0:v][1:v]ssim=stats_file=ssim.log" -f null -
```

The averaged PSNR is printed through ffmpeg's logging at the end of the run; per-frame values go to the `stats_file`. The ssim manual documents the per-frame keys `Y`, `U`, `V`, `All` and `dB`.

## Interpreting

Treat the numbers as relative: record a baseline score for your content and flag a drop from it. Identical frames give an infinite PSNR (the formula divides by the MSE) and an SSIM of 1.0. Flat animation scores high PSNR easily, so even a small drop can be a real regression.

## Render regression use

Comparing two renders of the same frame range after a pipeline change:
```bash
ffmpeg -framerate 24 -i old/f_%04d.png -framerate 24 -i new/f_%04d.png -lavfi "[0:v][1:v]psnr" -f null - 2>&1 | tail -1
```
`inf` = bit-identical. For a visual of where frames differ:
```bash
ffmpeg -i old/f_0100.png -i new/f_0100.png -lavfi "blend=all_mode=difference,eq=contrast=8" diff.png
```

Find the worst frames from the per-frame log: each line holds `key:value` pairs for one frame pair, so sort or filter on the PSNR value with your own script.

## Gotchas

- Both inputs must have the same resolution, pixel format and frame count (psnr and ssim manuals); align them first.
- Chroma planes are scored separately; colour shifts can hide behind a good Y score; read u/v too.
- PSNR is a pixel-difference measure; do not use it alone to choose between denoisers or grain settings.

## Verify

Compare a file with itself (PSNR inf, SSIM 1.0), then with a one-frame offset version (big drop),
to confirm the alignment handling in your script.

## Checked

2026-10-28. Confirmed in the ffmpeg-filters manual: `psnr` and `ssim` take the main input first and the reference second, `stats_file` writes per-frame key:value pairs, the same-resolution, same-pixel-format, same-frame-count requirement, the PSNR formula, ssim keys `Y`, `U`, `V`, `All`, `dB`. Removed: the dB and SSIM threshold table, the literal summary line formats, the `sort -k6` command (field order not documented), the perception-correlation and blur claims.

Method: documentation only; no commands were run.
