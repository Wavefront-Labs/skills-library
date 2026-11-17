---
id: creative-arts.animation.blender.comp-performance-precision
name: comp-performance-precision
category: creative-arts
field: animation
product: blender
tags: [blender, compositor, comp-performance, compositor-precision, compositing, optimization]
level: practitioner
status: docs-checked
description: "Make big compositor trees fast: GPU device, precision Auto vs Full, the 8k GPU limit, TDR resets on Windows, resolution percentage while building, and the render cache."
sources:
  - https://docs.blender.org/manual/en/latest/compositing/sidebar.html
  - https://docs.blender.org/manual/en/latest/compositing/limitations.html
  - https://docs.blender.org/manual/en/latest/render/cycles/render_settings/performance.html
  - https://docs.blender.org/manual/en/latest/render/output/properties/output.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# comp-performance-precision

Goal: interactive comp work on 4K multi-pass shots.

## Settings

- Render Properties > Performance > Compositor (also in the Compositor sidebar, Options tab > Performance): **Device** is CPU or GPU. GPU is usually faster for blur, glare and defocus style nodes.
- **Precision** (GPU only): **Auto** uses full precision for final renders and half precision otherwise (viewer, interactive). **Full** uses full precision for the final render and the viewport. Switch to Full when interactive results show banding or when Depth, Position or ID data looks quantised.
- **Denoise nodes** have their own settings in the same panel: Denoising Device (Auto, CPU, GPU), Preview Quality and Final Quality (High, Balanced, Fast) used by Denoise nodes set to *Follow Scene*.

## Working habits

- **Saving > Cache Result** in Output Properties > Output stores the rendered view layers and passes in a multi-layer EXR in the Render Cache folder, so the Compositor can reuse them without re-rendering. Image > Open Cached Render (Ctrl R in the Image Editor) reloads it in a later session.
- Work at a reduced **Resolution %** (Output Properties > Format) while building the tree. Pixel-based sizes such as blur radius are in pixels, so recheck at 100 percent.
- **Mute** heavy nodes while adjusting upstream nodes. Unmute before rendering.

## Limits

- GPU compositing does not support images larger than 8k; they are cropped or scaled.
- On Windows, a GPU task longer than the default 2 second Timeout Detection Recovery limit resets the GPU driver. Slow nodes such as Bokeh Blur on older GPUs trigger it; the manual recommends raising the TDR timeout.
- Blender uses the same GPU for the interface and the compositor, so the UI can become unresponsive on slower GPUs.

## Gotchas

- Muted nodes stay muted at render time. Check the tree before submitting.
- The manual notes that the Viewer region of interest (Ctrl B) is currently removed from the UI, so do not plan on it.

## Verify

Time the frame's compositing step before and after a change, using the render window or the console. Interactive feedback should be quicker with Device GPU on a supported card.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (blender-v5.2-release branch): sidebar.rst, limitations.rst, render/eevee performance.rst (Compositor section, included in the sidebar and Cycles pages) and output.rst (Cache Result). Confirmed: Device CPU/GPU, Precision Auto and Full wording, Denoise node settings, 8k limit, TDR text, Viewer region removal. Removed unconfirmable claims (version gates, per-node timings, proxies, ROI shortcut). Method: documentation only; no commands were run.
