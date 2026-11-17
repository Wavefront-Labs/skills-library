---
id: creative-arts.animation.blender.gpu-realtime-compositor
name: gpu-realtime-compositor
category: creative-arts
field: animation
product: blender
tags: [blender, compositor, compositor-gpu, realtime-compositor, viewport-compositor, gpu]
level: practitioner
status: docs-checked
description: "Use the GPU compositor: Device and Precision settings, denoise device and quality, the viewport compositor option in the Shading popover, and when to fall back to CPU."
sources:
  - https://docs.blender.org/manual/en/latest/render/cycles/render_settings/performance.html
  - https://docs.blender.org/manual/en/latest/render/eevee/render_settings/performance.html
  - https://docs.blender.org/manual/en/latest/editors/3dview/display/shading.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---
# gpu-realtime-compositor

Goal: fast compositing on the GPU, both for final renders and live in the 3D viewport.

## Compositor settings (Render Properties > Performance > Compositor)

- **Device**: CPU or GPU.
- **Precision** (GPU only): Auto uses full precision for final renders and half precision otherwise; Full uses full precision for final renders and the viewport.
- **Denoise Nodes** subpanel: **Denoising Device** (Auto uses the compositor's device, CPU, or GPU with fallback to CPU), **Preview Quality** and **Final Quality** (High, Balanced, Fast), used by Denoise nodes whose quality is Follow Scene.

The same Device and Precision settings also appear in the Compositor sidebar.

## Viewport compositor

3D Viewport > Shading popover > **Compositor**: Disabled, Camera (only in Camera View) or Always. It previews the compositing result in the viewport, which suits tuning glare, lens effects and grading on the live view.

## Limits to test for

- Not every node and pass behaves the same on every device or in the viewport. Check the node's manual page and test the tree in both modes.
- Viewport resolution follows the viewport size, so pixel-sized blur and glare differ from the final output. Prefer relative sizes where nodes offer them.
- Large frames with many passes and heavy blurs use GPU memory. Switch Device to CPU for that shot if memory runs out.

## Gotchas

- CPU and GPU results can differ slightly, so do not change Device in the middle of a sequence.
- Set the Viewport Compositor to Disabled or Camera while navigating heavy scenes.

## Verify

Render a frame with Device CPU and again with GPU, compare timings, and use a Difference blend of the two outputs to check they match closely enough for the shot.

## Checked

Date 2026-10-27. Blender manual 5.2 (blender-v5.2-release RST).
Confirmed: Device (CPU, GPU), Precision (Auto, Full) and their definitions, Denoising Device, Preview Quality, Final Quality, the Shading popover Compositor values Disabled, Camera, Always.
Removed as unconfirmed: the version gates "4.2+" and "3.5+", speed-up claims, the claim that unsupported nodes pass through or show a warning icon, and the claim that the viewport compositor recomputes on every Cycles sample.
Method: documentation only; no commands were run.
