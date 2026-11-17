---
id: creative-arts.animation.blender.denoising-data-passes
name: denoising-data-passes
category: creative-arts
field: animation
product: blender
tags: [blender, render-passes, denoising-data-passes, denoising-albedo, denoising-normal, denoise-node]
level: practitioner
status: docs-checked
description: "Render Cycles Denoising Data passes and denoise in the compositor: Noisy Image, albedo and normal passes, Denoise node inputs, and denoising light passes separately."
sources:
  - https://docs.blender.org/manual/en/latest/render/layers/passes.html
  - https://docs.blender.org/manual/en/latest/compositing/types/filter/denoise.html
  - https://docs.blender.org/manual/en/latest/render/cycles/render_settings/sampling.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---
# denoising-data-passes

Goal: control denoising after the render, per pass, instead of baking it into Combined.

## Render side (Cycles)

- View Layer Properties > Passes > Data > **Denoising Data**. Per the manual it adds: Noisy Image (the combined render before denoising), Denoising Albedo, Denoising Specular Albedo, Denoising Normal, Denoising Roughness and Denoising Depth.
- To let the compositor do the denoising, turn Render Properties > Sampling > Denoising > **Denoise (Render)** off, otherwise Combined is already denoised (Noisy Image still keeps the raw version).

## Compositor

Add the **Denoise** node (Filter category). It uses Open Image Denoise. Inputs:
- **Image**: the Noisy Image (or another noisy pass).
- **Albedo**: Denoising Albedo. **Normal**: Denoising Normal. Both optional but they preserve edges and fine detail.
- **HDR**: preserve colours outside the 0 to 1 range.
- **Prefilter**: None, Fast, Accurate (None assumes noise-free inputs and retains the most detail; Accurate prefilters the inputs for more detail than Fast at higher cost).
- **Quality**: Follow Scene, High, Balanced, Fast. Follow Scene uses the Compositor denoise quality in Render Properties > Performance.

## Per pass denoising

Denoising a light pass (for example Diffuse Direct and Indirect) separately before multiplying by its colour pass keeps texture detail, because the colour pass is not denoised. Recombine afterwards (see light-passes-recombine). This is a compositing practice, not a manual claim.

## Gotchas

- Denoising data must come from the same render as the image, so do not denoise a re-render using old albedo.
- Albedo and normal passes can be noisy with motion blur, depth of field and hair, so try Prefilter Accurate.
- In the Performance > Compositor panel, a Denoising Device setting (Auto, CPU, GPU) controls where Denoise nodes are processed.

## Verify

Compare render-time denoising with compositor denoising on the same frame and check texture detail in both.

## Checked

Date 2026-10-27. Blender manual 5.2 (blender-v5.2-release RST).
Confirmed: list of Denoising Data passes; Denoise node inputs, Prefilter and Quality values; Denoising Device in Performance > Compositor; Denoise (Render) setting name.
Removed as unconfirmed: the claim that the Denoise node is slow on CPU at 4K and above.
Method: documentation only; no commands were run.
