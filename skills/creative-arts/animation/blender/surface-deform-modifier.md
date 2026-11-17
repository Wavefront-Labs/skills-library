---
id: creative-arts.animation.blender.surface-deform-modifier
name: surface-deform-modifier
category: creative-arts
field: animation
product: blender
tags: [blender, surface-deform-modifier, surface-deform-bind, sparse-bind, surface-deform, modifiers, proxy-sim, cloth-proxy, bind-errors]
level: advanced
status: verified
description: "Bind a detailed mesh to a simulated or animated proxy with Blender's Surface Deform modifier: bind requirements, falloff, sparse bind and the bind error messages."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/deform/surface_deform.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/selecting/all_by_trait.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# surface-deform-modifier

Goal: drive a dense costume, accessory set or hair-card mesh from a low-res mesh that is simulated (cloth) or animated by anything, without rigging the dense mesh.

## Setup

On the **dense (driven) mesh**: *Modifiers → Deform → Surface Deform* → *Target* = the proxy mesh → **Bind**. After binding, the driven mesh follows every deformation of the target's evaluated result (armature, cloth, shape keys, other modifiers).

Fields:
- **Interpolation Falloff** (range 2 to 16, default 4): how much a vertex bound to one target face is affected by the surrounding faces; the manual notes lower values give smoother deformations but may introduce slight artifacts. Unavailable after binding.
- **Strength**: the overall amount of influence.
- **Vertex Group** (with invert): per-vertex influence.
- **Sparse Bind**: only records bind data for vertices with nonzero weights in the group at bind time; adding vertices to the group later requires a rebind.
- **Bind / Unbind**: until Bind is executed the modifier has no effect; once bound the button becomes Unbind, which resets the mesh to its original shape. *Target* is unavailable after binding.

The meshes are bound in global coordinates and later object transforms are ignored; only changes to the target's mesh itself are picked up. The further the driven mesh deviates from the target surface, the more likely artifacts become, so use reasonably well matching meshes.

## Bind requirements (the error messages)

The manual lists what the target mesh must not contain; the modifier reports these messages in the source:

| Error on Bind | Cause | Fix on the **target** |
|---|---|---|
| *Target has edges with more than two polygons* | edges shared by more than two faces | Select → Select All by Trait → Non Manifold to locate them, then repair |
| *Target contains concave polygons* | concave faces | split or triangulate the concave faces |
| *Target contains overlapping vertices* | doubles | Merge by Distance (Mesh, Clean Up) |
| *Target contains invalid polygons* | the manual lists faces with collinear edges | Degenerate Dissolve (Mesh, Clean Up) collapses short edges and small faces |

There are no restrictions on the modified (driven) mesh. In Blender 4.5.14 a quad with a collinear vertex reported *Target contains concave polygons* rather than the invalid-polygons message (that string comes from the source and was not reproduced), and a polygon with two coincident vertices reported *Target contains overlapping vertices*.

## Recipes

- **Cloth proxy**: low-poly shirt with Cloth sim → high-poly shirt with buttons, seams, Subdivision gets Surface Deform (target: low shirt). Bind where the two meshes match (rest pose).
- **Many accessories on one body**: belts, straps, badges each get Surface Deform → body. The body's Armature drives all without weight painting.
- **Hair cards on scalp**: cards follow the scalp mesh's armature/shape keys.
- **Sculpt detail on a blendshape head**: sculpt a dense head, bind to the low-res rigged head.

Bind is recorded against the modified mesh as it is at that moment, so keep generate modifiers consistent between binding and use (practice).

## Gotchas

- Bind where the two meshes coincide; the bind records the current state of both (binding in a posed frame carries that pose into the result).
- Parts of the driven mesh that sit far from the target surface are more likely to show artifacts.
- Where two target surfaces are close together (a collar), a vertex can bind to the wrong one; splitting the driven mesh by vertex group and using Sparse Bind per modifier is a practice workaround.

## Verify

- Scrub: driven mesh follows the proxy through the whole range, no popping at the bind frame.
- The modifier panel shows *Unbind* after a successful bind; an error message in the panel names the target problem.

## Checked

2026-10-27, Blender manual, branch blender-v5.2-release (raw RST, projects.blender.org/blender/blender-manual). Confirmed against modeling/modifiers/deform/surface_deform.rst and Blender source (MOD_surfacedeform.cc error strings; rna_modifier.cc falloff range 2 to 16, as of main on this date): target validity rules, bind/unbind/sparse-bind behaviour, global-coordinate note. Wrong claim fixed: higher Falloff does not mean smoother (the manual says lower is smoother). Removed the unconfirmed silent-unbind row, library-override, evaluated-target and hidden-target claims.

Run check, 2026-11-01, Blender 4.5.14 LTS headless: Surface Deform with Python: Bind and Unbind through the bind operator toggle Bound; the driven grid followed target vertex edits (z up to 0.5 after tilting the target) and ignored moving the target object by 5; Interpolation Falloff is clamped to 2 to 16 (99 became 16, default 4); Strength 0.5 halved the follow; Sparse Bind with a vertex group moved only grouped vertices (1.0 against 0.0); a target with an edge on three faces reported Target has edges with more than two polygons, a concave target reported Target contains concave polygons, and coincident vertices in one polygon reported Target contains overlapping vertices. Not run: the invalid-polygons message, hidden-target behaviour and the recipes (practice).

Method: manual text confirmed from documentation; behaviour run headless in Blender 4.5.14.
