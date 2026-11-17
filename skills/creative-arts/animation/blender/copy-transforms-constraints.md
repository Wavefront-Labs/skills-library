---
id: creative-arts.animation.blender.copy-transforms-constraints
name: copy-transforms-constraints
category: creative-arts
field: animation
product: blender
tags: [blender, constraints, copy-location, copy-rotation, copy-scale, copy-transforms, mix-mode, rigging]
level: practitioner
status: docs-checked
description: "Use Blender's Copy Location, Copy Rotation, Copy Scale and Copy Transforms constraints: axes, invert, offset, mix modes, Euler order, Power and Head/Tail."
sources:
  - https://docs.blender.org/manual/en/5.2/animation/constraints/transform/copy_location.html
  - https://docs.blender.org/manual/en/5.2/animation/constraints/transform/copy_rotation.html
  - https://docs.blender.org/manual/en/5.2/animation/constraints/transform/copy_scale.html
  - https://docs.blender.org/manual/en/5.2/animation/constraints/transform/copy_transforms.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# copy-transforms-constraints

Goal: one thing follows another's transform channels — the building block of FK/IK blending, twist distribution and prop attachment.

## Copy Location

- **Axis** X/Y/Z, **Invert** per axis (10 becomes -10), **Offset** (adds the target's position to the owner's original position instead of copying it). For bone targets the **Head/Tail** slider and the Follow B-Bone button (follow the curved shape of a bendy bone) apply; for mesh targets a **Vertex Group** can be used.
- Spaces matter (see `constraint-spaces`): World to World sticks to a point regardless of parents.

## Copy Rotation

- **Axis** + **Invert**; **Order**: the Euler order used for the copy, defaulting to the owner's.
- **Mix**: *Replace*, *Add* (target angles added to the owner's), *Before Original* (owner behaves as a child of the target), *After Original* (target behaves as a child of the owner), *Offset (Legacy)* (deprecated; fails with multiple axes).
- Twist distribution: forearm twist bones Copy Rotation of the wrist, Y axis only, Local to Local, influence 0.25/0.5/0.75 along the chain.

## Copy Scale

- **Axis**, **Power** (raises the target's scales to a power before Offset), **Make Uniform** (one uniform scale giving the same overall volume change), **Offset** (multiplies the owner's scale instead of replacing it), **Additive** (kept for compatibility, the manual says not to use it).
- Tips from the manual: Power can give a better result than Influence; to copy one target axis to all owner axes, disable the other axes, enable Make Uniform and set Power to 3.

## Copy Transforms

Full transform copy. **Mix**: Replace, Before Original (Full / Aligned / Split Channels), After Original (Full / Aligned / Split Channels). Full can shear under non-uniform scale; Aligned scales along the owner's own axes (like Inherit Scale Aligned); Split Channels handles location, rotation and scale separately. **Remove Target Shear** strips shear from the target's transform before mixing. Useful for bones following other bones and for FK/IK blending with animated influence.

## Gotchas

- Constraints evaluate top to bottom; a Copy Location placed below a Limit Location overrides the limit.
- Before Original versus After Original changes whether the owner is treated as a child of the target or the target as a child of the owner; test both when a result rotates around the wrong axis.

## Verify

Move/rotate the target: owner follows on intended axes only; at influence 0.5 it lands halfway.

## Checked

2026-10-27, Blender 5.2 manual (blender-v5.2-release). Confirmed on the Copy Location, Copy Rotation, Copy Scale and Copy Transforms pages: Axis/Invert/Offset, Head/Tail, Mix mode lists, Power, Make Uniform, Additive, Remove Target Shear and the Power-3 tip. Removed the unconfirmed Rigify-pattern statement and the single-axis euler-flip claim.

Method: documentation only; no commands were run.
