---
id: creative-arts.animation.blender.movie-distortion-node
name: movie-distortion-node
category: creative-arts
field: animation
product: blender
tags: [blender, movie-distortion-node, movie-distortion, undistort, lens-distortion, compositor]
level: practitioner
status: docs-checked
description: "Match lens distortion in comp with the Movie Distortion node: Type Undistort or Distort, Movie Clip, K1 K2 K3 setup, and which direction to use for bulging in or out."
sources:
  - https://docs.blender.org/manual/en/latest/compositing/types/transform/movie_distortion.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---
# movie-distortion-node

Goal: apply the real lens distortion from a camera solve in comp, so CG lines bend like the plate.

## Node (Transform category > Movie Distortion)

Removes distortion from a movie or adds it to a render so the render blends with the clip. It is usually used while motion tracking.
- **Image**: standard colour input.
- **Type**: **Undistort** (usually used on the raw distorted clip) or **Distort** (usually used on rendered images).
- **Movie Clip** (property): the clip whose distortion is used; useful when several clips have different distortion settings.
- Output: **Image**.

Calculate the distortion first by adjusting the K1, K2 and K3 values in Movie Clip Editor > Properties > Lens (or by solving them in the tracking tools; see lens-distortion-undistort).

## Which direction to use

The manual distinguishes two kinds of distortion:
- Clip bulging out: distort the render and leave the clip as is, because undistorting the clip needs extra pixels that Blender does not have.
- Clip bulging in: undistort the clip and leave the render as is, because distorting the render would need those missing pixels.
Using the wrong method gives odd results around the edges.

## Gotchas

- The node uses the clip's current lens values. Changing them after a comp is approved changes the result.
- Undistorting and redistorting resamples the plate; distorting only the CG leaves the plate untouched.

## Verify

Overlay CG lines that should match real straight edges (for example a floor grid along a wall base). After Distort, they should line up with the plate's straight edges.

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch).
Confirmed: Movie Distortion Image, Type (Undistort, Distort), Movie Clip, output, K1/K2/K3 location in the Lens panel, and the bulge-in versus bulge-out guidance. Removed the two pipeline diagrams, the overscan percentages and the proxy-resolution remark.
Method: documentation only; no commands were run.
