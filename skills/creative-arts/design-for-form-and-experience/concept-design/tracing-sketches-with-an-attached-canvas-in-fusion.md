---
id: creative-arts.design-for-form-and-experience.concept-design.tracing-sketches-with-an-attached-canvas-in-fusion
name: tracing-sketches-with-an-attached-canvas-in-fusion
category: creative-arts
field: design-for-form-and-experience
product: concept-design
tags: [fusion-360, autodesk-fusion, attached-canvas, canvas-image, calibrate-canvas, t-splines, sketch-to-cad, form-workspace]
level: intro
status: draft
description: "Bring side and top sketches into Fusion as attached canvases, calibrate them to real size, and use them as underlays for sketches and T-spline forms."
sources:
  - "Autodesk Fusion help - Insert Canvas, Calibrate a canvas, Canvas opacity and display through (help.autodesk.com/view/fusion360/ENU)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Attached canvas in Fusion

**Goal:** your 2D sketches (side, front, top) placed accurately in 3D so CAD follows the design
intent instead of drifting.

## Prepare the images
- Export each orthographic view as a separate image, cropped tight, with a known dimension
  drawn on it (overall length or a scale bar).
- Same scale and the same centreline/ground line across views makes alignment easy.

## Insert and calibrate
1. Insert > **Canvas**. Choose the image, then select the plane (XY, XZ, YZ or a face).
2. Set **Opacity** around 50% and enable **Display through** so geometry shows over it.
3. Right-click the canvas in the browser > **Calibrate**. Click two points on the image whose
   real distance you know and type the value. The image scales to true size.
4. Edit Canvas to move/rotate so the image centreline sits on the origin axis and the ground
   line on the base plane.
5. Repeat for the other views; check that heights line up across side and front.

## Using them
- Trace profiles with splines in a sketch, or switch to Create Form and pull the T-spline cage
  to match the outlines in each view.
- Lock canvases (right-click > Lock) after calibration so you do not move them by accident.

## Gotchas
- Perspective sketches cannot be traced; only orthographic drawings align.
- Views drawn by hand rarely agree perfectly; decide which view rules each dimension.
- Canvas visibility toggles per view; hide them before rendering.

## Verify
Measure the calibrated known dimension with Inspect > Measure: it matches the real value; side
and front views agree on overall height at the same datum.
