---
id: creative-arts.fashion-design.clo-3d.render-settings-lighting-and-hdri
name: render-settings-lighting-and-hdri
category: creative-arts
field: fashion-design
product: clo-3d
tags: [fashion-design, clo-3d, clo-render, garment-rendering, clo-render-settings, clo-hdri, render-lighting, vray-clo]
level: practitioner
status: draft
description: "Set up CLO 3D renders: interactive vs final render, image size, sampling quality, HDRI environment and lights, backgrounds, and saving reusable render presets."
sources:
  - https://support.clo3d.com/hc/en-us
  - https://www.clo3d.com/en/
  - https://support.clo3d.com/hc/en-us/categories/360000059787
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Render settings, lighting and HDRI in CLO

**Goal:** consistent, realistic product images from CLO for reviews, line sheets and
e-commerce previews.

## Render window
- Open the **Render** window (Render menu). **Interactive render** updates as you
  change settings; use it to set up. **Final render** for output.
- Settings: **image size** (e.g. 2000-4000 px long edge), **quality/sampling** (higher =
  less noise, longer), number of images (current view, multiple views, turntable).

## Lighting
- **HDRI environment**: choose a studio HDRI for soft even light (product shots) or an
  outdoor HDRI for lifestyle; rotate for key light direction; adjust intensity.
- Add lights (directional, spot, area) for rim light and shadows.
- Ground/shadow catcher for a soft floor shadow on plain backgrounds.

## Background
Solid colour (white/grey for e-commerce), image, or transparent PNG for compositing.

## Materials and camera
- Make sure fabric textures have proper normal maps and roughness; set **particle distance**
  low enough before render (fine detail).
- Camera: set focal length (e.g. 50-85 mm equivalent for minimal distortion), save camera
  views for front, side, back, 3/4.

## Presets
Save render settings and camera views as presets; reuse across a collection for consistent
images.

## Gotchas
- Rendering at coarse particle distance shows faceted fabric.
- HDRI too bright blows out whites; check histogram.
- Different render settings across styles make line sheets inconsistent.

## Verify
- [ ] Render preset and camera views saved and reused.
- [ ] No noise or blown highlights at final size.
- [ ] Colour checked against standards on a calibrated monitor.
