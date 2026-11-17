---
id: creative-arts.animation.blender.refine-solve-intrinsics
name: refine-solve-intrinsics
category: creative-arts
field: animation
product: blender
tags: [blender, camera-solve, refine-solve, refine-intrinsics, refine-focal-length, lens-distortion]
level: practitioner
status: docs-checked
description: "Refine camera intrinsics in a Blender solve: the Refine checkboxes for Focal Length, Optical Center, Radial and Tangential Distortion, and the need for good starting values."
sources:
  - https://docs.blender.org/manual/en/latest/movie_clip/tracking/clip/toolbar/solve.html
  - https://docs.blender.org/manual/en/latest/movie_clip/tracking/clip/sidebar/track/camera.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# refine-solve-intrinsics

Goal: correct lens values when the real focal length or distortion is unknown or slightly off.

## Camera data first (Sidebar > Track tab > Camera)

Enter what you know: **Sensor Width** (from the camera specification), **Pixel Aspect** (for example 1920 / 1280 = 1.5 when 1280 wide footage should be 1920 wide), **Focal Length** (millimetres or pixels), **Optical Center** and the lens distortion model with its coefficients. Camera presets in the panel header do not include distortion coefficients or the optical centre.

## Refine options (toolbar Solve tab > Solve > Refine)

Four checkboxes: **Focal Length**, **Optical Center**, **Radial Distortion** (K coefficients) and **Tangential Distortion** (P coefficients, Brown model). The manual says refining is useful when you are not sure of some intrinsics, but you still need approximate initial values: it will fail to find correct values if they were set completely incorrectly.

## Process

1. Solve without refine and note the solve error.
2. Enable one refine option and solve again; compare the error and the values in the Camera panel.
3. Keep the refinement only if the values are plausible (focal length near the real lens, small distortion) and the 3D result looks right.

## Gotchas

- Refining Optical Center and Tangential Distortion adds degrees of freedom; with few or poorly distributed tracks they can over-fit (practice, not from the manual).
- Refining happens only when solving camera motion; object solves share the camera data.

## Verify

Switch on **Render Undistorted** (Clip Display) on a frame with straight lines: they look straight. A test object stays locked to the footage, especially near the edges.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (blender-v5.2-release branch: movie_clip/tracking/clip/toolbar/solve, sidebar/track/camera, sidebar/track/objects) and the 5.2 source (space_clip.py Solve panel shows four Refine checkboxes). Fixed: removed the old dropdown version note (5.2 has four checkboxes) and the K1 to K3 only wording. Removed unconfirmed claims about absurd focal lengths and lens grid workflow.
Method: documentation only; no commands were run.
