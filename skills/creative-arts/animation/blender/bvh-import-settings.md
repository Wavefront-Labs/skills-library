---
id: creative-arts.animation.blender.bvh-import-settings
name: bvh-import-settings
category: creative-arts
field: animation
product: blender
tags: [blender, motion-capture, bvh-import-settings, bvh-rotation-mode, bvh-import, bvh, bvh-export, mocap]
level: practitioner
status: docs-checked
description: "Import and export BVH motion in Blender: scale, start frame, scene FPS/duration, rotation mode, forward/up axes, looping, and BVH export from an armature."
sources:
  - https://docs.blender.org/manual/en/latest/files/import_export/bvh.html
  - https://docs.blender.org/api/current/bpy.ops.import_anim.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# bvh-import-settings

Goal: BVH mocap that arrives at the right size, speed and orientation, ready for retargeting.

## Import (File > Import > Motion Capture (.bvh))

- **Target**: Armature (creates a skeleton with animation) or Object.
- **Scale**: factor to increase the physical size of the BVH; BVH files often use centimetres or inches (practice), so check the skeleton height after import and adjust.
- **Start Frame**, **Scale FPS** (scales the file's frame rate to the scene's; otherwise each BVH frame maps to one Blender frame) or **Update Scene FPS** (set the scene to the BVH rate), **Update Scene Duration** (extends the scene; never shortens it).
- **Loop**: cycles the animation playback.
- **Rotation**: operator default `NATIVE` (Euler in the file's rotation order); `QUATERNION` converts to quaternions (often easier to retarget, practice); fixed Euler orders are also offered.
- **Forward/Up** axes: operator defaults -Z forward, Y up.

## Export (File > Export > Motion Capture (.bvh))

- Select the armature; **Start/End** frames, **Scale**, **Rotation** order (the operator offers `NATIVE` and the fixed Euler orders), **Root Translation Only** (only write the translation channels for the root bone).

## Gotchas

- Without *Scale FPS*, each BVH frame maps to one Blender frame, so a 120 Hz capture in a 24 fps scene plays 5x too slow.
- Retargeting needs a matching rest pose on the target (see `bone-mapping-retarget`).
- Euler imports can contain 360-degree flips; the Discontinuity (Euler) Filter is the usual fix (see `clean-channels`).

## Verify

Skeleton height plausible; playback at scene fps matches the real-time motion; feet on the ground plane (Z ≈ 0) during contacts.

## Checked

Blender 5.2 manual (files/import_export/bvh) and Python API 5.2 (`bpy.ops.import_anim.bvh`, `bpy.ops.export_anim.bvh`), read 2026-10-27.
- Import options (Target Armature/Object, Scale, Rotation, Forward/Up, Start Frame, Scale FPS, Loop, Update Scene FPS/Duration) and export options (Scale, Rotation, Root Translation Only, Start/End): manual BVH page. Defaults rotate_mode='NATIVE', axis_forward='-Z', axis_up='Y', "never shortens the scene": API 5.2.
- Removed as unconfirmed: the CMU scale value, the Y-up and T-pose generalisations and the constraint-baking claim.

Method: documentation only; no commands were run.
