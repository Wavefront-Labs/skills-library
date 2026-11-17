---
id: creative-arts.animation.blender.eevee-volume-probe
name: eevee-volume-probe
category: creative-arts
field: animation
product: blender
tags: [blender, eevee, light-probes, irradiance-volume, eevee-volume-probe, volume-probe, probe-bake]
level: practitioner
status: docs-checked
description: "Bake EEVEE light probe volumes for indirect lighting: resolution, bake samples, surfel resolution, capture contributions, clamping, validity and dilation, plus bleed fixes."
sources:
  - https://docs.blender.org/manual/en/latest/render/eevee/light_probes/volume.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# eevee-volume-probe

Goal: baked bounce lighting (indirect diffuse light) for EEVEE interiors and sets.

## What it is

A light probe volume records the light incoming from all directions at many locations inside a volume; only the diffuse light is kept. Objects outside any volume, or with no baked indirect lighting, are shaded with the world's diffuse lighting. Add it with Add > Light Probe > Volume.

Manual tips: align grids with the room shape; avoid high resolution in empty areas or areas with little lighting variation; fix bad samples by adding a smaller grid near the problem; large scenes may need many volumes at different levels of detail.

## Object Data > Probe

- **Intensity**: scales the recorded lighting; anything other than 1.0 is not physically correct.
- **Sampling Bias**: Normal Bias (offsets sampling along the surface normal; too high can make diffuse surfaces look specular), View Bias (offsets along the view direction; too high gives view-dependent results; preferred if the camera is static), Facing Bias (at zero, avoids capture points behind the shaded surface; raising it smooths interpolation but adds bleeding).
- **Validity & Dilation**: each capture point gets a validity score from the back-faces it hits. Only materials with Single Sided turned on for light probe volumes (material Backface Culling > Light Probe Volume) reduce validity. **Validity Threshold**: points below it are ignored in interpolation (removes points trapped in closed geometry). **Dilation Threshold**: points below it get data from valid neighbours; **Radius** is the search radius in capture points.
- **Resolution X, Y, Z**: grid dimensions per probe; lighting is captured per cell.
- **Bake Samples**: ray directions evaluated when baking; bake time grows with the scene representation size.
- **Surfel Resolution**: surfels per local unit distance; higher quality but a huge memory impact. The manual suggests a value of twice the maximum Resolution.
- **Capture Distance**: distance around the volume captured during the bake (0 = inside only). **Contributions**: World (bake incoming world light, but lose correct blending to neighbouring volumes), Indirect Light, Emission.
- **Clamping** Direct / Indirect: 0.0 disables. A very small non-zero Clamp Indirect effectively records only the first bounce.
- **Offset**: Surface Offset (distance to move capture points off surfaces) and Search Distance (for points near the back-face of a single-sided object).
- Viewport Display: Data, Clipping, Influence.

## Bake

Light data is static and must be baked manually (bake button on the probe). The data is stored in the object data-block and can be moved, animated and linked between files. Baking uses the render visibility of objects.

The bake converts the scene into a memory-heavy representation and fails if it does not fit in GPU memory. Remedies: split larger scenes into sections or LODs, reduce Surfel Resolution, or turn off light probe volume visibility on objects that barely affect the bake.

## Verify

Compare with and without the bake: corners should get bounce colour from nearby lit walls, with no light seeping under walls.

## Checked

Date: 2026-10-27. Documentation: Blender 5.2 manual, EEVEE Light Probe Volume. Confirmed: all properties above, static baking and storage, memory remedies. Removed unconfirmed: version gate, resolution-per-metre suggestion, "turn off World for sealed interiors", rebake advice for moving objects, farm advice.
Method: documentation only; no commands were run.
