---
id: creative-arts.animation.blender.lens-distortion-undistort
name: lens-distortion-undistort
category: creative-arts
field: animation
product: blender
tags: [blender, camera-tracking, lens-distortion-tracking, undistort, distortion-model, lens-distortion]
level: practitioner
status: docs-checked
description: "Handle lens distortion in Blender tracking: Polynomial, Division, Nuke and Brown models, manual calibration, Render Undistorted and the Movie Distortion node."
sources:
  - https://docs.blender.org/manual/en/latest/movie_clip/tracking/clip/sidebar/track/camera.html
  - https://docs.blender.org/manual/en/latest/compositing/types/transform/movie_distortion.html
  - https://docs.blender.org/manual/en/latest/movie_clip/tracking/introduction.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# lens-distortion-undistort

Goal: match CG to footage shot through a real lens.

## Distortion models (Sidebar > Track tab > Camera > Lens)

- **Polynomial**: radial, K1, K2, K3.
- **Division**: for high distortion such as fisheye lenses, K1 and K2.
- **Nuke**: the model used by the Nuke compositor, K1 and K2.
- **Brown**: Brown-Conrady, radial K1 to K4 and tangential P1, P2.

Positive radial coefficients give barrel distortion and negative ones pincushion. Tangential P1 and P2 compensate for a sensor that is not perpendicular to the lens. Pick the model your pipeline shares (Nuke if comp is done in Nuke).

## Getting values

- Refine them in the solve: Solve tab > Refine > Radial Distortion or Tangential Distortion (see `creative-arts.animation.blender.refine-solve-intrinsics`).
- By hand: the manual describes tweaking K1 until the solve is closest to the known focal length, using the Calibration tools (a grid deformed by the distortion model) and the Annotation tool, drawing a line that should be straight in the footage and adjusting until the annotation matches. For more accurate calibration the manual points to the OpenCV grid calibration tool, which uses the same distortion model.

## Undistorted view

Clip Display popover: **Render Undistorted** shows the footage undistorted; **Calibration** shows the manual calibration tools. Proxy panel: **Build Undistorted** makes undistorted proxies.

## CG integration (Movie Distortion node, Add > Transform)

The node has an Image input, a **Type** (*Undistort* for the raw movie clip, *Distort* for rendered images) and a Movie Clip property. The manual advises:

- If the clip bulges out, distort the render and leave the clip as it is.
- If the clip bulges in, undistort the clip and leave the render as it is.
- The wrong choice needs pixels Blender does not have and causes edge artefacts.

## Verify

Overlay a CG grid on the floor through your chosen distortion path: it follows real floor lines out to the frame edges.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (blender-v5.2-release branch: movie_clip/tracking/clip/sidebar/track/camera, movie_clip/tracking/introduction, compositing/types/transform/movie_distortion) and the 5.2 source (space_clip.py Clip Display and Proxy panels, node_add_menu_compositor.py). Fixed: model name is Division (not Divisions) and uses K1 K2, the Movie Distortion advice depends on the direction of the distortion (the old skill said undistorting the plate is always the most accurate), and there is no Clip Display > Grid item. Removed unconfirmed claims about shooting lens grids per zoom setting and rendering with overscan.
Method: documentation only; no commands were run.
