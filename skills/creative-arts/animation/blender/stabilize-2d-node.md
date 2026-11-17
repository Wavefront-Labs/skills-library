---
id: creative-arts.animation.blender.stabilize-2d-node
name: stabilize-2d-node
category: creative-arts
field: animation
product: blender
tags: [blender, stabilization, stabilize-2d-node, stabilize-2d, compositor]
level: practitioner
status: docs-checked
description: "Use the Stabilize 2D compositor node: Movie Clip, Frame, Invert and Filter, stabilise-comp-restore and shake-matching workflows, ordering with Movie Distortion."
sources:
  - https://docs.blender.org/manual/en/latest/compositing/types/tracking/stabilize_2d.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---
# stabilize-2d-node

Goal: render stabilised footage, or match CG to the original shake.

## Node (Tracking category > Stabilize 2D)

Applies the stabilisation set in Movie Clip Editor > Properties > Stabilization > 2D Stabilization.
- **Image**: standard colour input.
- **Frame**: the frame from which to evaluate the stabilisation data. By default the current scene frame; it can be driven separately when the image is time-remapped or offset.
- **Invert**: inverts the stabilisation (if it would move the clip up by 5 units, the inverse moves it down by 5).
- **Filter** (Sampling): Nearest, Bilinear, Bicubic or Anisotropic. Bicubic suits photographic images.
- **Movie Clip** (property): the clip whose stabilisation to use.
- Output: **Image**.

## Workflows

1. **Stabilised delivery**: clip image -> Stabilize 2D -> grade -> output.
2. **Stabilise, comp, de-stabilise**: stabilise the plate for easier roto and paint, comp elements, then use Stabilize 2D with Invert on to restore the original motion.
3. **Add shake to locked CG**: set up stabilisation on a handheld reference clip, then apply Stabilize 2D with Invert to the CG so it takes the same shake.

## Order

If the shot has lens distortion, undistort first (Movie Distortion node), stabilise, comp, then reverse the steps in opposite order.

## Gotchas

- Each transform resamples the image, so stabilising and inverting costs some sharpness; use a higher-quality filter.
- Check the result at the edges of the frame, where the stabilisation shift can reveal empty areas.

## Verify

Stabilise then invert in sequence: the result should match the original plate apart from resampling softness (a Mix Color node set to Difference shows the residual).

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch).
Confirmed: Stabilize 2D Image, Frame, Invert and Filter inputs, Movie Clip property, source settings location in the Movie Clip Editor. Removed the Autoscale claim and the Add > Transform menu path.
Method: documentation only; no commands were run.
