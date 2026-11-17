---
id: creative-arts.animation.blender.denoise-samples-tradeoff
name: denoise-samples-tradeoff
category: creative-arts
field: animation
product: blender
tags: [blender, render-optimization, denoise-samples-tradeoff, samples-tradeoff, denoise, cycles]
level: practitioner
status: docs-checked
description: "Find the cheapest Cycles sample count that denoises cleanly: a ladder test with Noise Threshold, denoiser input passes, animation flicker checks and locking settings per sequence."
sources:
  - https://docs.blender.org/manual/en/latest/render/cycles/render_settings/sampling.html
  - https://docs.blender.org/manual/en/latest/render/cycles/optimizations/reducing_noise.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---
# denoise-samples-tradeoff

Goal: lowest render time that still looks clean in motion after denoising.

## The ladder test

1. Choose 2 to 3 hard frames (dark interior, hair close-up, glass or volume).
2. Render with denoising on at Noise Threshold 0.1, 0.05, 0.02 and 0.01 (the manual says typical values run from 0.1 to 0.001, lower meaning better quality and longer renders), or at fixed Render (Max) Samples such as 64, 128, 256, 512. Enable the Denoising Data pass so the Noisy Image is saved too.
3. Compare 100 percent crops of fine texture, skin or subsurface, glossy reflections, hair and dark corners.
4. The first step where nothing smears, blotches or loses texture is the minimum. Add one step of safety for animation.

## Denoiser settings that change the result

Render Properties > Sampling > Denoising:
- **Denoise (Render)** and **Denoise (Viewport)** switch denoising for final and viewport.
- **Denoiser**: Automatic, OpenImageDenoise or OptiX. OpenImageDenoise typically gives the highest quality per the manual.
- **Passes**: None, Albedo, Albedo + Normal. The manual recommends at least Albedo, since None can blur out details, especially at lower sample counts.
- With OpenImageDenoise: **Prefilter** (None, Fast, Accurate) and **Quality** (High, Balanced, Fast).

## What to look for at low samples

- Fine texture painted smooth (use Albedo or Albedo + Normal passes).
- Low-frequency blotches in dark indirect areas that crawl in animation.
- Hair and thin geometry clumped.
- Caustics and glints lost.
These are common denoiser artefacts to inspect, not figures from the manual.

## Animation check

Render a short run of consecutive frames at the chosen setting and play it looping, because blotches that move from frame to frame show more than static noise. The manual advises enabling **Use Animated Seed** (Sampling > Advanced > Seed) for animations, since a varying noise pattern is less noticeable. Raise samples or lower the threshold if flicker remains.

## Lock it

Agree on the setting per sequence and store it in the lighting template, so shots do not jump in quality across cuts.

## Gotchas

- Grading after denoise: pushing exposure or contrast reveals blotches, so test with the grade applied.
- Adaptive sampling: Noise Threshold 0 makes Cycles pick a value from the sample count, and Min Samples 0 picks one from the threshold.

## Verify

Show the chosen setting beside a high-sample reference in motion and sign off on that comparison, not on a still.

## Checked

Date 2026-10-27. Blender manual 5.2 (blender-v5.2-release RST).
Confirmed: Noise Threshold typical range and the 0 meaning; Min Samples 0 meaning; Denoise (Viewport/Render), Denoiser, Passes, Prefilter, Quality names and values; the Albedo recommendation; Use Animated Seed advice and location.
Removed as unconfirmed: the claim that denoising cost is a fixed per-frame amount, and the claim that more samples with animated seed beats fewer without it.
Method: documentation only; no commands were run.
