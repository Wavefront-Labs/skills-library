---
id: creative-arts.design-for-form-and-experience.experiential-design.mapping-projection-onto-surfaces
name: mapping-projection-onto-surfaces
category: creative-arts
field: design-for-form-and-experience
product: experiential-design
tags: [projection-mapping, video-mapping, projector-calibration, projection-blending, spatial-augmented-reality, immersive-installations]
level: advanced
status: draft
description: "Plan and calibrate projection mapping: choose projectors and lenses by throw ratio and brightness, build a surface model, warp and blend, and handle ambient light."
sources:
  - "Resolume documentation (resolume.com)"
  - "TouchDesigner documentation (derivative.ca)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Projection mapping

Projection mapping fits video to the shape of a surface (building, object, room). It uses projectors, a media server or software with warping and blending, and a model of the surface.

## Plan
1. **Surface:** measure it or get a 3D model; note colour, material, reflectivity (pale matte surfaces work best), gaps and angles.
2. **Projectors:** brightness (lumens), resolution and **lens throw ratio** (throw distance divided by image width: a ratio of 1.5 at 6 m distance gives a 4 m wide image). Choose lenses for the available throw distances; lens shift and keystone limits.
3. **Brightness budget:** image brightness depends on lumens, image area, surface gain and ambient light; low ambient light and pale surfaces need far fewer lumens than daylight or dark surfaces. Use manufacturer calculators and plan headroom.
4. **Positions:** place projectors to avoid shadows from visitors and objects, with overlap for blending and mounting that is stable and ventilated.

## Calibrate
- **Software or media server:** for example Resolume, MadMapper, TouchDesigner, Disguise or Watchout; many offer mesh warping, edge blending and masks.
- **Align** with a grid or 3D model: use point-based warping, a camera-based auto-calibration, or a 3D-model-based method.
- **Blend** overlapping projectors with edge-blend gradients and match brightness and colour between projectors.
- **Content:** make video to the mapped UV or an authored mask; test at full resolution and frame rate (see `...experiential-design.running-media-servers-and-content-playback`).

## Maintain
Lamp or laser ageing shifts brightness; re-check alignment after bumps or temperature changes; save projects and calibration.

## Verify
- [ ] The seams between projectors are invisible at the viewing distance.
- [ ] Brightness suits the actual ambient light.
- [ ] Calibration is saved and reproducible.
