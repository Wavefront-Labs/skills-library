---
id: creative-arts.animation.blender.sculpt-cloth-pose-brushes
name: sculpt-cloth-pose-brushes
category: creative-arts
field: animation
product: blender
tags: [blender, cloth-brush, pose-brush, elastic-deform, sculpt-cloth, cloth-filter, boundary-brush, snake-hook, sculpt, posing-sculpts, wrinkles, ipose]
level: advanced
status: docs-checked
description: "Blender sculpt posing and simulation tools: Cloth brush and Cloth Filter for folds, Pose brush with face-set posing, Elastic Deform and Boundary brushes, with their settings."
sources:
  - https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/brushes/cloth.html
  - https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/tools/cloth_filter.html
  - https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/brushes/pose.html
  - https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/brushes/boundary.html
  - https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/brushes/elastic_deform.html
  - https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/brushes/brushes.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# sculpt-cloth-pose-brushes

Goal: use the physics-flavoured sculpt tools to pose a sculpt and lay in cloth folds quickly instead of rigging or simulating.

## Cloth brush and Cloth Filter

Cloth runs a simplified cloth simulation under the brush. Settings (Deformation, Simulation Area Local/Global/Dynamic, Simulation Limit and Falloff, Pin Simulation Boundary, Force Falloff, Cloth Mass, Cloth Damping, Soft Body Plasticity, Persistent, Use Collisions) are in `creative-arts.animation.blender.cloth-brush-settings`.

- Masked vertices are pinned in the simulation, and auto-masked face set boundaries also hold. The Sculpt gravity factor applies.
- **Cloth Filter** (Toolbar) simulates all vertices at once: drag away from the object for a positive effect, toward it for negative. Types: Gravity, Inflate, Expand, Pinch, Scale (a soft body scale that makes folds, steered by Force Axis and Orientation). **Use Face Sets** restricts it to the face set under the mouse; **Use Collisions** needs the collider to have Collision physics.
- Pose and Boundary brushes can do cloth sculpting if Deformation Target is switched to Cloth Simulation.

## Pose brush

Armature-like posing of a sculpt without a rig. The brush finds a pose origin automatically (white line on the cursor); only Size and Auto-Masking affect its general behaviour.

- Deformation: Rotate/Twist (Ctrl twists and disables IK segments), Scale/Translate (Ctrl moves), Squash/Stretch.
- Rotation Origins: Topology (from mesh topology and shape), Face Sets (one pose segment per face set starting from the active set), Face Sets FK (forward kinematics using the set under the cursor).
- Pose Origin Offset, Smooth Iterations, Pose IK Segments, Keep Anchor Point, Lock Rotation when Scaling, Connected Only and Max Element Distance (details in `creative-arts.animation.blender.pose-brush-modes`).
- Masks stop the deformation from reaching masked areas; face sets work best for predictable pivots (see `creative-arts.animation.blender.face-set-edit`).

## Elastic Deform

Simulates grabbing or twisting of elastic objects. Deformation: Grab, Bi-scale Grab, Tri-scale Grab, Scale, Twist. Volume Preservation sets the Poisson ratio (higher keeps volume but bulges more). Ctrl deforms along the normal of the active vertex.

## Boundary brush

Like Pose but deforms the open boundaries of a mesh (boundaries to hidden geometry count too). Deformation: Bend (rotates around local Y, for sleeves), Expand (local X), Inflate, Grab, Twist (local Z, for skirt folds), Smooth. **Boundary Falloff**: Constant, Brush Radius, Loop, Loop and Invert. **Boundary Origin Offset** is relative to the brush radius. Even quad topology gives the best results.

## Related brush assets

Grab (G), Grab 2D, Grab Silhouette, Elastic Grab, Snake Hook (K), Pull, Thumb, Nudge, Twist, Relax Slide (Shift smooths) and Relax Pinch move or redistribute geometry. Snake Hook works much better with Dyntopo enabled.

## Workflow: posing a sculpt

1. Finish the neutral pose, then keep a copy of the unposed mesh.
2. Paint or initialize face sets per limb segment and mask the parts that should stay fixed.
3. Use the Pose brush with Face Sets origins and a few IK segments; Ctrl for twist.
4. Use Relax Slide and Smooth at the joints to clean up topology and shape.
5. Use Cloth Filter on garment shells with collision from the body, and the Cloth brush for art-directed folds.

## Gotchas

- Cloth quality depends on even, well-distributed topology.
- Collisions only work with objects that have Collision physics enabled.

## Verify

The Pose brush bends the forearm only, at the face set boundary; Cloth Filter drape rests on the collision body without intersections when orbited.

## Checked

2026-10-27, Blender 5.2 manual (blender-v5.2-release branch). Confirmed against sculpt_paint/sculpting/brushes (cloth, pose, boundary, elastic_deform, brushes list), tools/cloth_filter and introduction/cloth_sculpting: all settings and options named above, shortcuts G, K and Shift smoothing for Relax Slide. Removed unconfirmed numeric claims (damping range, simulation limit default, IK segment range, vertex counts, Poisson values), the Shift-menu tool access note, Grab 2D elastic variant, Snake Hook sub-settings and symmetry remarks.
Method: documentation only; no commands were run.
