---
id: creative-arts.animation.blender.volume-object-settings
name: volume-object-settings
category: creative-arts
field: animation
product: blender
tags: [blender, volume-object-settings, volume-interpolation, homogeneous, volume-step, volumetrics, cycles]
level: practitioner
status: docs-checked
description: "Tune volume objects and materials in Blender: Grids, VDB sequence settings, Render settings (Space, Step Size, Clipping, Precision), Cycles material volume options."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/volumes/properties.html
  - https://docs.blender.org/manual/en/latest/render/cycles/material_settings.html
  - https://docs.blender.org/manual/en/latest/render/eevee/material_settings.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---
# volume-object-settings

Goal: correct-looking volumes at the lowest cost.

## Volume object (Object Data Properties)
- **Grids**: a list of the grids in the OpenVDB file with name and data type; click a grid to make the volume object display it.
- **OpenVDB File**: **File Path**; **Sequence** loads one file per frame (numeric suffix, for example smoke-000.vdb, smoke-001.vdb) with **Frames**, **Start**, **Offset** and **Mode** (Clip shows nothing outside the range, Extend holds the first or last frame, Repeat, Ping-Pong).
- **Viewport Display**: see volume-display-settings.
- **Render**: Space, Step Size, Clipping, Precision, velocity settings (see volume-render-settings). Step Size 0 means automatic from voxel size.

## Material settings (Material Properties > Settings > Volume)
Cycles:
- **Sampling Method**: Distance, Equiangular, Multiple Importance (default).
- **Interpolation**: Linear (good for thin volumes) or Cubic (smoother, needed for denser volumes, slower).
- **Step Rate** (Biased only): see volume-step-rate.
EEVEE: **Intersection** decides which inner part of a mesh produces the volumetric effect: *Fast* treats each face as a medium interface (correct for manifold geometry with no inner parts); *Accurate* treats faces as interfaces only when consecutive facing differs, is correct until the max ray depth is exceeded, and uses significantly more memory.

## Limitations
Volume objects do not support the material Pass Index.

## Gotchas
- A material Step Rate does nothing unless Render Properties > Volumes > Biased is on (Cycles).
- Closest-style display interpolation is only for viewing raw voxels; it does not change the render.

## Verify
Change Step Size or Interpolation on a smoke cache and compare render time against the visible difference.

## Checked
Date: 2026-10-27. Documentation: Blender manual (Volume Properties, Cycles and EEVEE Material Settings), branch blender-v5.2-release. Confirmed: Grids list, sequence settings and modes, Render settings, material Sampling Method, Interpolation, Step Rate (Biased only), EEVEE Intersection, Pass Index limitation. Removed the Homogeneous material option (no longer in the manual), Max Bounces recommendations, the sequence-mode wording about grids, and older-version ray visibility remarks.
Method: documentation only; no commands were run.
