---
id: creative-arts.animation.blender.normal-edit-modifier
name: normal-edit-modifier
category: creative-arts
field: animation
product: blender
tags: [blender, normal-edit, modifiers, custom-normals, shading, foliage, toon]
level: practitioner
status: verified
description: "Bend shading normals in Blender with the Normal Edit modifier: Radial and Directional modes, Target, Mix Mode and Factor, Max Angle, Offset, vertex group."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/normals/normal_edit.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# normal-edit-modifier

Goal: generate custom normals with simple parametric methods and mix them with the existing ones: soft foliage shading, toon-style face shading, without changing geometry.

## Settings

- **Radial**: aligns normals with the vector from the origin to each vertex, so they radiate from a centre as if from an ellipsoid.
- **Directional**: makes all normals converge towards a target object.
- **Target**: object whose origin is the reference point. Optional in Radial, mandatory in Directional.
- **Parallel Normals** (Directional only): normals parallel to the line between both origins instead of converging.
- **Mix Mode**: how generated normals combine with existing ones (Copy, Add, Subtract or Multiply in the 4.5.14 API). Multiply is a component-by-component multiplication, not a cross product.
- **Mix Factor**: how much of the generated normals is mixed in. **Vertex Group** gives per-vertex control (invertible).
- **Max Angle**: forbids generated normals deviating from the original by more than the threshold; prevents extreme changes and inverted faces.
- **Lock Polygon Normals**: prevents flipping polygons whose normal no longer matches their corners' custom normals.
- **Offset**: offsets the modified object's origin before generating normals; relevant only in Radial mode with no Target, and in Directional mode with Parallel Normals.

## Uses

The manual cites quick radial normals for low-poly tree foliage and fixing toon-style shading by partially bending default normals. Bending normals toward the camera fakes light scattering in vegetation.

For copying normals between meshes use the Data Transfer modifier; the Weighted Normal modifier covers other shading effects.

## Verify

Rotate a light: shading on the affected region changes smoothly with no black patches or flipped faces.

## Checked

Date: 2026-10-27. Documentation release: Blender manual, 5.2 release branch (Normal Edit modifier page). Confirmed: modes, Target rules, Parallel Normals, Mix options, Max Angle, Lock Polygon Normals, Offset conditions. Removed unconfirmed recipe values, stack-placement and export claims, and the "Copy/Add/Subtract/Multiply" list (mix mode names not shown on the page).

Run check, 2026-11-01, Blender 4.5.14 LTS headless: Normal Edit with Python on a smooth-shaded grid: modes Radial (default) and Directional; Mix Mode Copy (default), Add, Subtract, Multiply; Mix Factor 1.0 and Max Angle 180 degrees defaults; Radial gave normals pointing away from the origin ((-0.71,-0.71,0) at a corner); Directional with no Target changed nothing and with a Target at (0,0,5) normals converged on it; Parallel Normals gave the single direction (0,0,1); Radial with a Target used the Target as the centre; Offset (1,0,0) with no Target moved the radiating centre; Mix Factor 0 kept the existing normals; Max Angle 10 degrees limited the deviation; Multiply of existing (0,0.6,0.8) with radial normals gave (0,-1,0) (component by component, not a cross product). Not run: Lock Polygon Normals effect and Offset in the Directional Parallel case.

Method: manual text confirmed from documentation; behaviour run headless in Blender 4.5.14.
