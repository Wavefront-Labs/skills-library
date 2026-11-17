---
id: creative-arts.animation.blender.skin-modifier-roots
name: skin-modifier-roots
category: creative-arts
field: animation
product: blender
tags: [blender, skin-modifier-roots, skin-radius, skin-armature, skin-modifier, modifiers, base-mesh, blockout, create-armature]
level: practitioner
status: docs-checked
description: "Block out characters, trees and tubes from vertex skeletons with Blender's Skin modifier: mark root, Skin Resize radii, loose branches, symmetry and Create Armature."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/skin.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# skin-modifier-roots

Goal: a quad base mesh (and optionally a rig) in minutes from a stick-figure of vertices and edges — the fastest way to a sculpt-ready creature, tree or cable bundle.

## Workflow

1. Start from a single vertex (for example a primitive reduced to one vertex in Edit Mode). In Edit Mode extrude vertices (`E`) into a skeleton: spine, limbs, fingers. Branch freely; faces in the input geometry are ignored.
2. *Modifiers → Generate → Skin*. The modifier uses vertices and edges with a per-vertex radius; the output is mostly quads, with some triangles around intersections.
3. Select vertices and press `Ctrl A` (Mesh → Transform → Skin Resize) to change their X and Y skin radii; press `X` or `Y` during the operator to change only one radius, or edit the radii in the Transform panel of the Sidebar. If the modifier is deleted the radii are lost.
4. **Mark Root** (modifier button) on the pelvis/trunk vertex: that vertex is used to calculate rotations for connected limbs and is the origin for the root bones. Each set of connected vertices has one root (one is chosen by default); Mark Root enforces one root per set.
5. Add *Subdivision Surface* after Skin for the smooth blockout. The manual places Mirror above Skin when mirrored geometry is wanted.

Buttons/fields: *Branch Smoothing* (a branch point is a vertex with three or more edges; the setting relaxes the surface there and shrinks it), *Smooth Shading*, *Symmetry X/Y/Z* (keeps the output topology symmetrical on that axis; it does not add mirrored geometry, use the Mirror modifier for that), *Mark Loose / Clear Loose* (by default a branch vertex generates extra edge loops to keep output tight; loose lets the output stretch between all adjacent vertices), *Mark Root*, *Equalize Radii* (makes the X and Y radii of selected vertices equal), *Add Skin Data* (regenerates the skin data if it was lost), **Create Armature**.

## Create Armature

Creates an armature on top of the object where each edge becomes a bone (if the root vertex has more than one adjacent edge, an extra bone serves as the root). It adds a new armature object with bones matching the input mesh, adds weight groups to the input mesh (the Skin modifier propagates them to the output) and adds an Armature modifier directly below the Skin modifier, so it deforms only the Skin output.

## Recipes

These recipes are practice, not from the manual.

- **Creature blockout for sculpting**: skeleton, radii, Subdivision Surface, apply the stack, then sculpt (with Dyntopo or Voxel Remesh if you need to even out the topology).
- **Tree**: a trunk vertex chain with branch vertices and decreasing radii, with Branch Smoothing raised.
- **Cable bundle / pipes**: equal radius along chains; no subdivision for hard-edged pipes.
- **Hand**: palm vertex with five chains; mark the wrist as root.

## Gotchas

- Branch points (three or more edges) tend to produce more complicated topology, some of which may overlap; try *Branch Smoothing* or *Mark Loose*.
- Faces in the input are ignored by the modifier, so they only add clutter; delete them (practice).
- Radii are stored per vertex; very small or large skeletons need their radii resized with Skin Resize.
- With a Mirror modifier above Skin, keep the centre vertices on the mirror axis so the spine merges (practice).
- Overlapping geometry at tight bends is a known side effect; remesh before sculpting (practice).

## Verify

- `Ctrl A` in Edit Mode changes the radius of the selected vertices and the output updates.
- Create Armature: posing a bone moves its limb.
- Subdivided result has no inverted faces (Face Orientation overlay).

## Checked

2026-10-27, Blender manual, branch blender-v5.2-release (raw RST, projects.blender.org/blender/blender-manual). Confirmed against modeling/modifiers/generate/skin.rst and modeling/meshes/editing/mesh/transform/skin_resize.rst: options (Branch Smoothing, Symmetry, Smooth Shading, Create Armature behaviour and modifier order, Add Skin Data, Mark/Clear Loose, Mark Root, Equalize Radii), Ctrl A shortcut for Skin Resize. Wrong claim fixed: the Armature modifier sits below Skin, not above it. Removed unconfirmed Extra Objects step, default radius value and the Branch Smoothing figure.

Method: documentation only; no commands were run.
