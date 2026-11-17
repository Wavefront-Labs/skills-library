---
id: creative-arts.animation.blender.comp-vector-blur
name: comp-vector-blur
category: creative-arts
field: animation
product: blender
tags: [blender, vector-blur, speed-vector, motion-blur, compositor, render-passes]
level: practitioner
status: docs-checked
description: "Add post motion blur with the Vector Blur node: render Vector and Depth passes with Motion Blur off, Samples and Shutter, and fixing artefacts with separate render layers."
sources:
  - https://docs.blender.org/manual/en/latest/compositing/types/filter/blur/vector_blur.html
  - https://docs.blender.org/manual/en/latest/render/layers/passes.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---
# comp-vector-blur

Goal: cheap, adjustable motion blur after rendering.

## Render

- Turn **Motion Blur** off in the render settings: the Vector pass is disabled when Motion Blur is enabled.
- In View Layer properties > Passes > Data, enable **Vector** and **Depth** (Z). The Vector pass is available in Cycles and EEVEE and holds 2D screen-space motion based on the next and previous frames.
- The Depth pass is noisy if the render itself uses depth of field or motion blur.

## Node (Filter > Blur > Vector Blur)

Inputs: **Image** (the Combined pass), **Speed** (the Vector pass), **Z** (the Depth pass), **Samples** (quality factor) and **Shutter** (duration of the blur in seconds, the simulated exposure time per frame).

## Where it breaks

2D passes carry no 3D information, so what is behind a moving object or outside the camera view is lost, and artefacts can remain even with a correct setup. The manual's suggestions:
- Render into multiple render layers (for example an animated character separate from the background), vector blur each, then composite the results. This matters especially with hair or transparency.
- Slightly blur the Speed pass or set a maximum speed limit to smooth the motion; too much blurring causes its own problems.

## Verify

Compare a fast-motion frame with render motion blur and with vector blur. Blur length should match, and check the edges of moving objects over moving backgrounds.

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch).
Confirmed: Vector Blur inputs Image, Speed, Z, Samples, Shutter; the Vector pass is disabled when Motion Blur is on; Depth pass noise with DOF or motion blur; multi-layer workflow and speed-smoothing hints. Removed the Blur, Speed Min/Max and Curved settings (not in 5.2), the shutter-angle equivalences and the 32-sample recommendation.
Method: documentation only; no commands were run.
