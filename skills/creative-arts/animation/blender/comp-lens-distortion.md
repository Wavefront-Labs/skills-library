---
id: creative-arts.animation.blender.comp-lens-distortion
name: comp-lens-distortion
category: creative-arts
field: animation
product: blender
tags: [blender, lens-distortion, lens-distortion-node, dispersion, chromatic-aberration, compositor]
level: practitioner
status: docs-checked
description: "Add or match lens distortion in the compositor: Lens Distortion node Type, Distortion, Dispersion, Jitter and Fit, and when to use Movie Distortion for plates."
sources:
  - https://docs.blender.org/manual/en/latest/compositing/types/transform/lens_distortion.html
  - https://docs.blender.org/manual/en/latest/compositing/types/transform/movie_distortion.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---
# comp-lens-distortion

Goal: make clean CG look shot through a real lens, or match plate distortion.

## Node (Transform category > Lens Distortion)

- **Type**: **Radial** (barrel or pincushion distortion) or **Horizontal** (horizontal distortion giving a channel or colour shifting effect).
- **Distortion** (Radial only): bulging or pinching effect from the image centre.
- **Dispersion**: simulates chromatic aberration, a rainbow-coloured fringe.
- **Jitter**: adds jitter to the distortion; faster but noisier.
- **Fit** (Radial only): scales the image so black areas are not visible. Only works for positive distortion.

## Matching a plate

For plate work, use the Movie Distortion node with the movie clip's solved camera lens model (see movie-distortion-node). Lens Distortion is an artistic approximation.

## Taste

- Keep barrel distortion subtle on wide shots, and none for long lenses.
- Chromatic aberration: tiny amounts, mostly at the edges, and consistent per lens across a sequence.
- Distort before adding grain so the grain is not distorted.

## Gotchas

- Fit hides the empty edges by scaling up, so you lose resolution. Render with overscan and crop for the best edge quality.
- Strong dispersion on text or UI elements makes them hard to read.

## Verify

Overlay a grid render (a plane with a checker in camera) through the node. Lines should bend gently at the edges and colour fringes appear only toward the frame edges.

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch).
Confirmed: Lens Distortion Type (Radial, Horizontal), Distortion, Dispersion, Jitter and Fit (positive distortion only). Removed the -1 to 1 range, the sign-to-shape mapping, the Projector option, the numeric Dispersion and Distortion amounts, and the node-ordering claim relative to glare and vignette.
Method: documentation only; no commands were run.
