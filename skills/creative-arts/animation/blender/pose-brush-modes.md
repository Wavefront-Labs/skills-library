---
id: creative-arts.animation.blender.pose-brush-modes
name: pose-brush-modes
category: creative-arts
field: animation
product: blender
tags: [blender, sculpting, pose-brush-modes, pose-brush-ik, pose-origin, elastic-deform-settings, poisson-ratio, elastic-deform]
level: practitioner
status: docs-checked
description: "Re-pose sculpts with Blender's Pose brush (topology or face set origins, IK segments, rotate, scale, squash) and tune Elastic Deform modes and volume preservation."
sources:
  - https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/brushes/pose.html
  - https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/brushes/elastic_deform.html
  - https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/brushes/boundary.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# pose-brush-modes

## Pose brush

The Pose brush deforms a model like an armature, for posing without a rig or adjusting proportions. It determines an origin automatically, shown as a white line on the brush cursor. Only Size and Auto-Masking in the general settings affect it.

- **Deformation**: *Rotate/Twist* (rotates around the pose origin; Ctrl applies a twist instead and disables any IK segments), *Scale/Translate* (Ctrl moves the mesh instead), *Squash/Stretch* (different scale per axis).
- **Rotation Origins**: *Topology* sets the origin from the mesh topology and shape; *Face Sets* creates one pose segment per face set starting from the active one, which the manual says can give the most accurate results; *Face Sets FK* simulates a forward-kinematics deformation using the face set under the cursor as control.
- **Pose Origin Offset**: offset of the pose origin relative to the brush radius; useful for complex shapes like fingers.
- **Smooth Iterations**: smoothness of the deformation falloff.
- **Pose IK Segments**: number of IK segments created (shown as a divided line on the cursor); useful for curved deformations like tails and hair clumps.
- **Keep Anchor Point**: keeps the last segment of the IK chain fixed; off lets the mesh drag around freely for snake-like shapes. **Lock Rotation when Scaling** applies only scaling in Scale/Translate.
- **Connected Only**: affects only topologically connected elements. Turning it off lets disconnected meshes (character with clothing) deform together, with a performance cost reduced by keeping **Max Element Distance** low.
- Changing Deformation Target to Cloth Simulation lets the brush do cloth sculpting.

Workflow: initialize face sets from loose parts, materials or sharp edges, or paint them per limb (see `creative-arts.animation.blender.face-set-edit`), then pose with Face Sets or Face Sets FK origins. Expand Face Set from a boundary is a quick way to create pivot-defining sets.

## Elastic Deform

Simulates realistic deformation of elastic objects, such as grabbing or twisting; good for the shape of organic objects. With Ctrl the brush deforms along the normal of the active vertex.

- **Deformation**: *Grab*, *Bi-scale Grab* (falloff more local to the centre), *Tri-scale Grab* (more local still), *Scale* (displaces vertices away from the active vertex), *Twist* (rotates vertices around the active vertex).
- **Volume Preservation**: higher values preserve volume more but cause more bulging (it sets the Poisson ratio).

## Verify

Joints bend at the intended location without collapsing; elastic grabs keep the surrounding volume smooth.

## Checked

2026-10-27, Blender 5.2 manual (blender-v5.2-release branch). Confirmed against sculpt_paint/sculpting/brushes/pose, elastic_deform and boundary: Deformation modes and Ctrl behaviour, Rotation Origins descriptions, Pose Origin Offset, Smooth Iterations, IK Segments, Keep Anchor Point, Connected Only and Max Element Distance, Elastic Deform modes, Volume Preservation meaning. Removed unconfirmed claims: Topology as default, IK segment range, Kelvinlet and resolution-independence wording, the 0.5 Poisson limit, and the symmetry and performance gotchas.
Method: documentation only; no commands were run.
