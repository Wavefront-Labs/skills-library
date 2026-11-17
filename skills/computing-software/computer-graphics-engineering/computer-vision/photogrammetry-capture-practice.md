---
id: computing-software.computer-graphics-engineering.computer-vision.photogrammetry-capture-practice
name: photogrammetry-capture-practice
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, image-based-rendering, photogrammetry, capture-planning, cross-polarization, ground-control-points, scale-bars, overlap, turntable-capture, realitycapture, metashape]
level: practitioner
status: draft
description: "Plan and shoot photogrammetry captures that reconstruct cleanly: overlap and angles, camera settings, lighting and cross-polarisation, scale bars/GCPs, turntables."
sources: ["https://szeliski.org/Book/", "https://www.agisoft.com/pdf/metashape-pro_2_1_en.pdf", "https://colmap.github.io/tutorial.html#data-structure", "https://dev.epicgames.com/community/learning/tutorials/realitycapture"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Photogrammetry capture practice

**Goal:** image sets that produce accurate, complete, texture-clean models the first time —
capture quality dominates software choice (Szeliski 2e §11, §13).

## 1. Coverage
- Overlap 60–80% between neighbouring shots; every surface point seen from ≥ 3 (ideally 5+)
  images with 10–20° angular separation.
- Rings around the object at several heights + top-down; move the camera, don't just rotate
  it in place (pure rotation gives no parallax).
- Fill the frame with the subject; add detail passes closer up, with transitional shots so
  close-ups connect.

## 2. Camera settings
- Manual exposure, fixed ISO (low), fixed white balance, **fixed focal length** (no zoom
  changes; disable stabilisation that shifts the optical centre if possible).
- f/8–f/11 for depth of field; shutter fast enough to avoid blur (tripod for slow shutter).
- RAW + consistent processing (same profile for all images; no per-image auto adjustments).

## 3. Lighting
- Diffuse, even light (overcast outdoors, softboxes indoors); avoid hard moving shadows.
- **Cross-polarisation** (polariser on light + rotated polariser on lens) removes specular
  highlights → clean albedo textures and better matching on shiny surfaces.
- Shiny/transparent/uniform objects: temporary matte scanning spray or projected texture.

## 4. Scale and accuracy
- Scale bars / coded targets in the scene, or measured distances between markers.
- Large sites/drones: ground control points (GCPs) surveyed with RTK GNSS; check points
  withheld for accuracy assessment.
- Turntable captures: mask the background (or the scene appears static while object rotates
  — confuses SfM); use a textured turntable top or markers.

## 5. Pre-flight check
Shoot a quick low-res set and align it on site (Metashape/RealityCapture/COLMAP) — discover
gaps before leaving the location.

## Gotchas
- Mixed cameras/lenses: separate camera calibration groups.
- Moving elements (foliage in wind, people, water) produce artefacts.
- Too many near-duplicate images slow processing without improving quality.

## Verify
- [ ] Alignment registers ≥ 95% of images with low reprojection error.
- [ ] Check-point error / scale-bar error within spec.
- [ ] Textures free of baked specular highlights (if albedo needed).
