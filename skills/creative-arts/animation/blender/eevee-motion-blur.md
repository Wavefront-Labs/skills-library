---
id: creative-arts.animation.blender.eevee-motion-blur
name: eevee-motion-blur
category: creative-arts
field: animation
product: blender
tags: [blender, eevee, eevee-motion-blur, motion-blur, shutter]
level: practitioner
status: docs-checked
description: "Set EEVEE motion blur: position, shutter, steps and how they interact with render samples, bleeding bias, max blur, and the compositor vector blur alternative."
sources:
  - https://docs.blender.org/manual/en/latest/render/eevee/render_settings/motion_blur.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# eevee-motion-blur

Goal: correct motion blur in EEVEE renders.

## Render Properties > Motion Blur

- **Position**: Start on Frame (shutter starts opening at the current frame), Center on Frame (fully open at the current frame), End on Frame (fully closed at the current frame).
- **Shutter**: time in frames between shutter open and close.
- **Bleeding Bias**: used by the post-process blur to avoid blurring the background over the foreground; lower values reduce background bleeding onto foreground elements.
- **Max Blur**: an optimisation limiting the number of pixels across which the blur is calculated.
- **Steps**: number of steps used by the accumulation blur, and thus its accuracy; more steps mean longer render time. EEVEE renders multiple time steps and accumulates them (precise, but needs many steps for clean gradients), combined with the post-process blur to handle gaps between steps. Each step is a full scene re-evaluation and can add a lot of render time. More steps allow a lower Max Blur.
- **Shutter Curve**: use a custom shutter curve.

When using multiple time steps the render sample count is rounded up to the next multiple of the step count, which can lower the quality of Jitter Camera depth of field; increasing viewport or render samples restores it.

## Viewport

Motion blur is only visible in the viewport during animation playback, and uses a simpler algorithm than the final render (the same applies to Viewport Renders). Check with a final render.

## Alternative

Render without blur plus a Vector pass and use the compositor Vector Blur node (see comp-vector-blur).

## Verify

Render a frame with fast motion. The blur length should match shutter times movement per frame; raise Steps if curved motion shows visible segments, then compare render time.

## Checked

Date: 2026-10-27. Documentation: Blender 5.2 manual (EEVEE Motion Blur). Confirmed: Position, Shutter, Bleeding Bias, Max Blur, Steps and sample-rounding note, Shutter Curve, viewport behaviour. Removed unconfirmed: Center as default, 180-degree shutter equivalence and shutter presets, 64-sample guidance, camera-cut and constant-interpolation gotchas, deformation cost claim.
Method: documentation only; no commands were run.
