---
id: creative-arts.animation.blender.sculpt-voxel-remesh
name: sculpt-voxel-remesh
category: creative-arts
field: animation
product: blender
tags: [blender, sculpting, sculpt-voxel-remesh, voxel-remesh-sculpt, fix-poles, quadriflow, quadriflow-remesh, voxel-size, remesh]
level: practitioner
status: verified
description: "Use Sculpt Mode voxel remesh (Ctrl-R): voxel size, R to set interactively, adaptivity, Fix Poles, preserve options, and when Quadriflow is the better remesher."
sources:
  - https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/tool_settings/remesh.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/retopology.html
  - https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/introduction/adaptive.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# sculpt-voxel-remesh

Goal: rebuild a sculpt's topology to even density so it can keep being sculpted, merged and stretched. For the modifier version see `creative-arts.animation.blender.remesh-modifier-modes`.

## Usage

- Panels: Sculpt Mode > Sidebar > Tool > Remesh, and Properties > Data > Remesh (Object and Sculpt Mode).
- **Voxel Size**: size of one voxel in object space; lower values keep finer detail but give much denser topology. Press **R** in the viewport to set it interactively with a grid overlay (Shift for precision). **Sample Voxel Size** matches the density of an area you pick.
- **Ctrl-R** runs the remesh (Voxel Remesh button).
- **Adaptivity** (`mesh.remesh_voxel_adaptivity`, default 0; `mesh.remesh_voxel_size` default 0.1): reduces face count where detail is not needed and introduces triangles (tested: 0.5 gave 20 triangles among 108 faces); a value above zero disables Fix Poles.
- **Fix Poles**: tries to produce fewer poles at a performance cost.
- **Preserve** (Sculpt panel): Volume (slower on complex meshes), Paint Mask, Face Sets, Color Attributes are reprojected onto the new mesh. The Properties panel has Volume and Attributes.
- The result is a new manifold mesh built from the volume (a UV sphere with 128 faces gave 366 all-quad faces at Voxel Size 0.25; the operator is `bpy.ops.object.voxel_remesh()` and it ran in Object Mode); other data layers are rebuilt by reprojection only when Properties > Data > Remesh > Attributes (`mesh.use_remesh_preserve_attributes`, default on) is on, and it only works on the original mesh data, ignoring modifiers, shape keys and rigging. Objects need an enclosed volume (fill holes larger than the voxel size first; Mask Slice with Fill Holes can fill all holes if nothing is masked).

## Workflow

1. Join separate parts and remesh to fuse them into one volume.
2. Remesh coarse while blocking, finer as forms settle.
3. Remeshing is not possible on an object with a Multires modifier that has subdivision levels (the operator poll fails with "The remesher cannot run with a Multires modifier in the modifier stack"; a Multires modifier with zero levels did not block it), so finish remeshing before adding Multires.

## Quadriflow (Properties > Data > Remesh > Quad)

Uses the Quadriflow algorithm: slower, can produce better results, but does not clean up intersecting geometry. Suited for creating a base mesh for Subdivision Surface or Multires. Options include Use Mesh Symmetry, Preserve Sharp, Preserve Mesh Boundary, Preserve Attributes, Smooth Normals, and a Mode for detail (Ratio, Edge Length or Faces) and a Seed (`bpy.ops.object.quadriflow_remesh`: `target_faces` defaults to 4000, `use_mesh_symmetry` to on, the preserve options and `smooth_normals` to off; a run with Faces 200 gave 193 quads and dropped the UV map because Preserve Attributes was off). The data property `mesh.remesh_mode` is VOXEL or QUAD. Neither remesher produces final topology for animated deformation; that is manual retopology.

## Gotchas

- Voxel remesh is for sculpting, 3D printing and simple stand-in meshes, not for characters that must deform, and not for reducing the face count of a healthy mesh (use Decimate).
- UVs and other layers survive only as a reprojection (tested: with Attributes on the UV map was kept but its coordinates are not the original ones; with it off the object had no UV map), so remesh before UV unwrapping.

## Verify

The wireframe overlay shows evenly spaced geometry; mask, face sets and colours are present when their Preserve options were enabled.

## Checked

2026-10-27, Blender 5.2 manual (blender-v5.2-release branch). Confirmed against sculpt_paint/sculpting/tool_settings/remesh, introduction/adaptive and meshes/retopology: panel locations, Voxel Size, R and Ctrl-R, Sample Voxel Size, Adaptivity disabling Fix Poles, Preserve options, known limitations, Quadriflow options and guidance. Removed unconfirmed voxel size examples, the two-voxel thinness claim and apply-scale advice.
Run check, 2026-11-01, Blender 4.5.14 LTS headless: `Mesh` properties `remesh_voxel_size` (0.1), `remesh_voxel_adaptivity` (0), `use_remesh_fix_poles` (off), `use_remesh_preserve_volume` (on), `use_remesh_preserve_attributes` (on), `remesh_mode`; voxel remesh of a 128-face UV sphere (0.25 gave 366 faces, 0.5 on the result gave 94); the Multires poll message; Quadriflow results above. Unrun (sculpt mode needs a GPU context; the sculpt-mode operators crashed the headless build): R and Ctrl-R, Sample Voxel Size, Fix Poles and Adaptivity interaction, Preserve panel in Sculpt mode (Paint Mask, Face Sets, Color Attributes), hole filling, panel locations.
Method: documentation checked against the manual and API pages; the code and operators were run headless in Blender 4.5.14.
