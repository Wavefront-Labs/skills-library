---
id: creative-arts.animation.blender.recalculate-normals
name: recalculate-normals
category: creative-arts
field: animation
product: blender
tags: [blender, normals, recalculate-normals, flip-normals, recalculate-outside, face-orientation, mesh-cleanup]
level: practitioner
status: verified
description: "Fix flipped Blender faces: Recalculate Outside (Shift N) and Inside (Shift Ctrl N), Flip, the Face Orientation overlay, and why custom split normals can still look wrong."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/meshes/editing/mesh/normals.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# recalculate-normals

Goal: all faces pointing outward, which matters for backface culling, Solidify, booleans, exports and printing.

## Commands (Edit Mode, Mesh > Normals or `Alt N` popover)

- **Recalculate Outside** (`Shift N`) and **Recalculate Inside** (`Shift Ctrl N`): flip the selected faces where necessary so all point outward or inward. The mesh does not need to be a closed volume. Neither affects custom split normals.
- **Flip**: reverses the orientation of the selected faces (front becomes back). In Blender 4.5.14 it also flips existing custom split normals ((0,0,1) became (0,0,-1)), and its *Custom Normals Only* option flips only those. Use it for manual fixes.

## Workflow

1. Turn on Overlays > **Face Orientation** to spot faces oriented the wrong way (blue front, red back in the default theme).
2. Select all (`A`) and run Recalculate Outside.
3. For remaining wrong patches, select the region (`L` for linked) and Flip, or fix the topology.

## Why it can look wrong

- Custom split normals are separate data: Recalculate does not change them; Flip does (see above). The Custom Data panel of the mesh Properties is where custom normals are cleared; do that if shading still looks inverted.
- Interior faces, non-manifold edges and nested shells make "outside" ambiguous; clean them first with Select All by Trait (Non Manifold, Interior Faces).

## Verify

Face Orientation overlay is entirely blue from outside; a Solidify modifier thickens outward as expected.

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch, projects.blender.org/blender/blender-manual). Confirmed against the Editing Normals page: Recalculate Outside/Inside shortcuts, no closed-volume requirement, Flip and custom split normals not affected, Face Orientation overlay and Custom Data panel for clearing. Removed unconfirmed claims about negative scale and Apply Scale, theme colours, a scripting equivalent and open-mesh direction.

Run check, 2026-11-01, Blender 4.5.14 LTS headless: Normals with Python: flipping every face of a cube made the normals point inward; Recalculate Outside restored outward normals (dot with face centre positive) and Recalculate Inside made them inward; on an open grid Recalculate made all normals consistent without a closed volume; with custom split normals set to (0,0,1), Recalculate left them unchanged and Flip reversed them; the default keymap has Shift N (Outside), Shift Ctrl N (Inside) and Alt N for the Normals menu; Preferences theme Face Orientation front is blue and back is red (alpha 0 and 0.7); the Clear Custom Split Normals Data operator exists. Corrected: Flip does change custom split normals in 4.5.14. Not run: the A and L selection steps and Custom Data panel clicking (UI).

Method: manual text confirmed from documentation; behaviour run headless in Blender 4.5.14.
