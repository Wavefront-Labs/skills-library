---
id: creative-arts.animation.blender.volume-render-settings
name: volume-render-settings
category: creative-arts
field: animation
product: blender
tags: [blender, volume-object, openvdb, volume-render-settings, volume-step-size, volume-space, clipping, precision]
level: practitioner
status: docs-checked
description: "Render OpenVDB volumes in Blender: volume object Render settings (Space, Step Size, Clipping, Precision, velocity), Cycles Volumes panel (Biased), EEVEE Volumes panel."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/volumes/properties.html
  - https://docs.blender.org/manual/en/latest/render/cycles/render_settings/volumes.html
  - https://docs.blender.org/manual/en/latest/render/eevee/render_settings/volumes.html
  - https://docs.blender.org/manual/en/latest/modeling/volumes/introduction.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---
# volume-render-settings

Goal: clean volume renders at sane render times and memory.

## Volume object > Object Data > Render
- **Space**: *Object* keeps density and detail the same regardless of object scale; *World* specifies Step Size and Density in world space.
- **Step Size**: distance between volume samples; lower values render more detail at a performance cost; 0 means it is determined automatically from voxel size.
- **Clipping** (Cycles only): value under which voxels are treated as empty space to speed up rendering. Range 0 to 1.
- **Precision** (Cycles only): *Full* (32-bit float), *Half* (16-bit), *Variable* (less precision in less noticeable areas); lower precision reduces memory at the cost of detail.
- **Velocity Grid** (Cycles only): grid name holding voxel velocities for motion blur, either one 3D-vector grid or a prefix of three scalar grids with x, .x or _x suffixes (same for Y and Z); **Velocity Unit** (per frame or per second) and **Velocity Scale** multiplier.

## Cycles: Render Properties > Volumes
Default volume rendering is based on null scattering (unbiased, fewer artifacts, possibly noisier). The **Biased** option switches to ray marching, and only then do these apply: **Step Rate Render**, **Viewport** and **Max Steps** (default 1024; protects against extremely long renders). Cycles estimates step size from voxel size in volume objects and smoke simulations; increasing it saves time but may lose detail. Volume scattering depth is set in Light Paths > **Volume** bounces (default 0).

## EEVEE: Render Properties > Volumes
EEVEE evaluates volume objects inside the view frustum using 3D textures with high video memory use. Settings: **Resolution**, **Steps** (samples along view depth), **Distribution** (blend of linear and exponential; higher puts more samples near the camera), **Max Depth** (accurate intersection method; artifacts if exceeded), and **Custom Range** (Start, End) to restrict the computed depth range, useful for World volumes or many volume objects.

## Shader
Volume objects render with Principled Volume by default, using grids named `density`, `color` and `temperature`; if absent, pick another grid name in the shader nodes. Check names in the object's Grids list.

## Limitations
OpenVDB sparse volumes are still rendered as dense volumes in Blender, so memory and time scale with the bounding box.

## Gotchas
- Banding or stepping points to a step size that is too large; faint wisps disappear when Clipping is raised.

## Verify
Render a small region with Step Rate 1 and 2 (Biased on); if visually identical, keep the faster one.

## Checked
Date: 2026-10-27. Documentation: Blender manual (Volume Properties, Volume Introduction, Cycles Volumes, EEVEE Volumes), branch blender-v5.2-release; property names, defaults and ranges from rna_volume.cc and the Cycles add-on properties.py on the Blender main branch. Confirmed: all items above. Removed unconfirmed claims: Clipping default 0.001, Half precision recommendation, EEVEE Volume Shadows setting, and Max Steps and Step Rate recommendations that ignored the Biased switch.
Method: documentation only; no commands were run.
