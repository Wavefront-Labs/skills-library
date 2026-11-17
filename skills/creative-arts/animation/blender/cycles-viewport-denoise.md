---
id: creative-arts.animation.blender.cycles-viewport-denoise
name: cycles-viewport-denoise
category: creative-arts
field: animation
product: blender
tags: [blender, cycles, viewport-denoise, viewport-samples, denoise, lookdev]
level: practitioner
status: docs-checked
description: "Make the Cycles rendered viewport fast and readable: viewport samples and noise threshold, denoiser choice, start sample, pixel size and Simplify viewport limits."
sources:
  - https://docs.blender.org/manual/en/latest/render/cycles/render_settings/sampling.html
  - https://docs.blender.org/manual/en/latest/render/cycles/render_settings/performance.html
  - https://docs.blender.org/manual/en/latest/render/cycles/render_settings/simplify.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# cycles-viewport-denoise

Goal: interactive Cycles viewport for lighting and lookdev without waiting.

## Render Properties > Sampling > Viewport

- **Max Samples** (Viewport (Max) Samples): paths per pixel in the Rendered shading mode. 0 samples indefinitely.
- **Noise Threshold** and **Min Samples**: viewport counterparts of the render settings; a higher threshold stops sampling clean pixels sooner.
- **Denoise** (Viewport): denoise in the Rendered shading mode. **Denoiser**: Automatic uses GPU-accelerated denoising if supported and prefers OpenImageDenoise over OptiX. **Passes**: None, Albedo, or Albedo + Normal (more passes generally better). For OpenImageDenoise, **Quality** Fast is described as ideal for viewport rendering, and **Prefilter** is available.
- **Start Sample**: the sample at which denoising starts in the viewport.
- **Use GPU** for denoising is faster than CPU but needs extra GPU memory.

## Performance (Render Properties > Performance > Viewport)

- **Pixel Size**: controls the resolution of viewport rendering; a larger pixel size speeds it up, especially on high-DPI displays.
- Render Properties > Simplify offers Max Subdivision and Child Particles limits (and Texture Resolution to scale down image textures) to lighten heavy scenes; the Simplify panel has Viewport and Render subsections so finals can stay untouched.

## Habits

- Use Material Preview (EEVEE) for layout and use Cycles rendered only for lighting decisions.
- Check final noise with a region render at final settings; viewport denoising can hide noise the final still has.
- The viewport uses the Viewport sample settings, not the final Render (Max) Samples.

## Verify

Orbit the camera; the viewport should refresh quickly and settle to a clean image. Then compare a final render of the same area.

## Checked

Date: 2026-10-27. Documentation: Blender 5.2 manual (Cycles Sampling, Performance, Simplify). Confirmed: viewport sampling and denoise options, Denoiser Automatic behaviour, Quality Fast for viewport, Start Sample, Pixel Size, Simplify limits. Removed unconfirmed: default values (0.1, 1024), start-sample advice, Texture Limit preference, render-region shortcut keys, pause-button note.
Method: documentation only; no commands were run.
