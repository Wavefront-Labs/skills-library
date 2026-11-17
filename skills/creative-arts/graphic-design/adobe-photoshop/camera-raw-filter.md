---
id: creative-arts.graphic-design.adobe-photoshop.camera-raw-filter
name: camera-raw-filter
category: creative-arts
field: graphic-design
product: adobe-photoshop
tags: [graphic-design, adobe-photoshop, photoshop, adjustment-layers, tonal-correction, camera-raw-filter, adobe-camera-raw, white-balance, texture-clarity-dehaze, masking-ai, lens-corrections, presets, raw-smart-object]
level: practitioner
status: draft
description: "Correct photos with Camera Raw as a smart filter or raw smart object: white balance, tone, texture/clarity/dehaze, AI masks, lens fixes and presets for sets."
sources:
  - https://helpx.adobe.com/camera-raw/using/camera-raw-filter.html
  - https://helpx.adobe.com/camera-raw/using/masking.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Camera Raw filter

**Goal:** fast, high-quality global and local photo correction that stays editable inside the PSD.

## Getting in
- Raw files (CR3, NEF, ARW, DNG) open in Camera Raw automatically. Click **Open** with
  Shift (or set "Open as Object" in the workflow options) to place as a **raw smart object** -
  double-click later to re-edit with full raw data.
- For JPEG/TIFF or any layer: convert to smart object, then **Filter > Camera Raw Filter**
  (Shift+Ctrl/Cmd+A). It becomes a smart filter.

## Edit order (Basic/Light, Color, Effects panels)
1. **Profile:** Adobe Color/Adobe Landscape/Portrait for raw.
2. **White balance:** eyedropper on a neutral, then Temp/Tint by eye.
3. **Exposure, Contrast**, then **Highlights** down / **Shadows** up to recover detail,
   **Whites/Blacks** to set end points (Alt/Option+drag shows clipping).
4. **Texture** (fine detail, good for skin at negative values), **Clarity** (midtone contrast),
   **Dehaze** (haze/contrast; strong values look fake).
5. **Vibrance** before Saturation.
6. **Optics / Lens:** Remove Chromatic Aberration, Use Profile Corrections; **Geometry** Upright for verticals.
7. **Detail:** sharpening and noise reduction (AI Denoise on raw files in recent versions).

## Masking (local adjustments)
Masking panel: **Select Subject, Select Sky, Background, People** (faces, skin, eyes, hair separately),
Objects, plus Brush, Linear and Radial gradients, Range masks. Each mask gets its own sliders - e.g.
lift a face, darken the sky, warm the background.

## Consistency across a set
Edit one image, save a **preset** (Presets panel) or in Bridge/Lightroom sync settings across
the set. In Photoshop, copy the Camera Raw smart filter (Alt/Option+drag) to other layers.

## Gotchas
- Camera Raw Filter on a non-smart layer is destructive - convert first.
- Big exposure lifts on 8-bit JPEGs show noise and banding; raw has far more headroom.
- Upright/geometry crops the image; check that edges are not lost.

## Verify
- [ ] Applied as a smart filter or raw smart object (re-editable).
- [ ] No clipped highlights/shadows except speculars; neutrals neutral.
- [ ] Set of images matched via preset or synced settings.
