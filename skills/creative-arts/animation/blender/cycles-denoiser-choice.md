---
id: creative-arts.animation.blender.cycles-denoiser-choice
name: cycles-denoiser-choice
category: creative-arts
field: animation
product: blender
tags: [blender, cycles, oidn-vs-optix, openimagedenoise, oidn, prefilter, denoise]
level: practitioner
status: docs-checked
description: "Choose and configure the Cycles denoiser: OpenImageDenoise vs OptiX, albedo/normal guide passes, prefilter None/Fast/Accurate, quality modes and GPU denoising."
sources:
  - https://docs.blender.org/manual/en/latest/render/cycles/render_settings/sampling.html
  - https://docs.blender.org/manual/en/latest/render/cycles/gpu_rendering.html
  - https://www.openimagedenoise.org/
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# cycles-denoiser-choice

Goal: pick the denoiser and settings that give the cleanest result without smearing detail.

## Render Properties > Sampling > Denoising

Separate Viewport and Render options exist: **Denoise (Viewport)**, **Denoise (Render)**, and viewport **Start Sample**.

- **Denoiser**: *Automatic* uses GPU-accelerated denoising if supported and prefers OpenImageDenoise over OptiX. *OpenImageDenoise* (Intel, an AI denoiser) typically gives the highest quality. *OptiX* (NVIDIA AI denoiser) supports GPU acceleration on some older NVIDIA GPUs where OpenImageDenoise does not, and is only available on NVIDIA GPUs when OptiX is configured in the Cycles user preferences.
- **Passes**: None (colour only), Albedo, or Albedo + Normal. More passes generally gives a better result; the manual recommends at least Albedo, since None can blur out details, especially at lower sample counts.
- **Prefilter** (OpenImageDenoise only): *None* keeps the most detail and is fastest but assumes noise-free input passes. *Fast* assumes noisy passes but applies no prefiltering (faster than Accurate, blurrier). *Accurate* prefilters the passes, usually more detailed than Fast but slower.
- **Quality** (OpenImageDenoise only): High (best quality, slowest), Balanced, Fast (ideal for viewport rendering).
- **Use GPU**: much faster than CPU but needs extra GPU memory; turn it off if large scenes run out of GPU memory.

GPU-accelerated denoising hardware (manual, GPU Rendering page): NVIDIA with compute capability 7.0+ (all RTX); AMD discrete Radeon RX 6000 and newer on Linux, RX 7000 and newer on Windows; all supported Intel Arc GPUs; Apple Silicon.

## Which and when

| Situation | Choice |
|---|---|
| Final frames | OpenImageDenoise with Albedo + Normal; Accurate prefilter if the guide passes are noisy |
| Viewport | Quality Fast on OpenImageDenoise, or OptiX where OIDN has no GPU support |
| Compositing control | Turn render denoise off, enable the Denoising Data pass, and denoise with the compositor Denoise node (see denoising-data-passes) |

## Gotchas

- Denoising cannot rescue badly under-sampled images. Too few samples gives blotches.
- Denoisers run per frame in animation, so leftover blotches can crawl between frames; test a short range.
- Check alpha edges when rendering with a transparent film.
- If the render runs out of GPU memory, disable Use GPU for denoising.

## Verify

Render one frame with Denoise off and with each denoiser, and compare a textured crop and a smooth gradient.

## Checked

Date: 2026-10-27. Documentation: Blender 5.2 manual (Cycles Sampling, GPU Rendering). Confirmed: denoiser options and descriptions, Passes, Prefilter, Quality and Use GPU semantics, GPU denoising hardware list. Removed unconfirmed: defaults, version gates, per-scene recommendations (4K memory, under-16-samples behaviour).
Method: documentation only; no commands were run.
