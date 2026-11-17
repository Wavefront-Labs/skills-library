---
id: creative-arts.animation.blender.cycles-noise-threshold
name: cycles-noise-threshold
category: creative-arts
field: animation
product: blender
tags: [blender, cycles, noise-threshold, min-samples, max-samples, adaptive-sampling, samples]
level: practitioner
status: docs-checked
description: "Set Cycles adaptive sampling well: the Noise Threshold checkbox and value, Min Samples 0 behaviour, Time Limit interplay, and checking the threshold against the graded result."
sources:
  - https://docs.blender.org/manual/en/latest/render/cycles/render_settings/sampling.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# cycles-noise-threshold

Goal: let Cycles stop sampling clean pixels early, so the time goes to the noisy ones.

## Settings (Render Properties > Sampling)

- **Noise Threshold** checkbox: when enabled, Cycles uses adaptive sampling, cutting short sampling in areas that have become less noisy than the threshold value. The manual's example: hair on a character may need many samples while the background needs few.
- **Noise Threshold** value: the threshold deciding whether to continue sampling a pixel. Typical values range from 0.1 to 0.001; lower means better quality and longer renders. Setting the value to 0 makes Cycles guess an automatic value from the total sample count (it does not switch adaptive sampling off; untick the checkbox for that).
- **Min Samples**: minimum samples a pixel receives before adaptive sampling is applied. 0 (default) lets Cycles pick a value determined by the Noise Threshold.
- **Max Samples** (Render (Max) Samples): the ceiling for the final render. **Time Limit** stops rendering when exceeded, 0 disables it (see cycles-time-limit).
- Viewport and Render have separate threshold, min and max samples. Viewport (Max) Samples set to 0 samples indefinitely.

## Workflow

1. Pick a threshold for the shot type (higher for look development, lower for hero stills), render, and compare crops at 200%.
2. Raise Min Samples if small bright features such as caustics, tiny highlights or thin hair are missed and freeze into black or blotchy patches while the pixel looked converged early.
3. If wide areas still reach the ceiling, look for a firefly or caustic source (see cycles-clamping-fireflies) rather than raising Max Samples.
4. With denoising on, check the threshold on the denoised result.

## Animation

Per-pixel stopping can vary from frame to frame. Use the same threshold on every shot of a sequence, an animated seed policy (see cycles-seed-pattern), and judge a short sequence rather than one still.

## Gotchas

- Post exposure or grading multiplies residual noise, so set the threshold for the graded result.
- Per-view-layer sample overrides are controlled by Sampling > Advanced > Layer Samples (Use, Bounded, Ignore).

## Verify

Render the same frame at two thresholds, compare render time and a crop of the darkest area, and keep the cheaper one if the difference is invisible after the grade.

## Checked

Date: 2026-10-27. Documentation: Blender 5.2 manual, Cycles Sampling. Confirmed: adaptive sampling checkbox, threshold range and value 0 behaviour, Min Samples 0, Time Limit, Layer Samples. Wrong claim fixed: a threshold of 0 does not turn adaptive sampling off. Removed unconfirmed: default values (0.01, 4096, 0.1, 1024), per-shot-type values, Debug Sample Count pass instructions, denoise threshold suggestions.
Method: documentation only; no commands were run.
