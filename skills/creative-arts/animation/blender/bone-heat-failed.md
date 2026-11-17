---
id: creative-arts.animation.blender.bone-heat-failed
name: bone-heat-failed
category: creative-arts
field: animation
product: blender
tags: [blender, rigging, skinning, bone-heat-failed, bone-heat, heat-weighting, automatic-weights, troubleshooting]
level: practitioner
status: draft
description: "Fix Blender's 'Bone Heat Weighting: failed to find solution for one or more bones': merge doubles, remove interior faces, scale up tiny meshes, apply transforms, and split problem parts."
sources:
  - https://docs.blender.org/manual/en/latest/animation/armatures/skinning/parenting.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# bone-heat-failed

Goal: Ctrl P > With Automatic Weights succeeds and gives clean weights.

## Why it fails

Bone heat diffuses weight across the surface from each bone. It fails (some bones get no weights) when the mesh is non-manifold, has overlapping/duplicate vertices, disconnected interior geometry, is tiny in world scale, or bones lie outside the mesh.

## Fix checklist (on a copy)

1. **Merge by Distance** (Edit Mode, M > By Distance, 0.0001).
2. **Apply transforms**: Ctrl A > All Transforms on mesh and armature; mesh scale 1.
3. **Scale up tiny meshes**: if the character is a few cm tall, scale mesh+armature ×10-100, parent, then scale back (known precision issue).
4. **Remove interior faces/loose geometry**: Select > Select All by Trait > Interior Faces, Loose Geometry; delete.
5. **Separate problem parts**: eyes, teeth, buttons, hair cards — skin them separately (parent to a single bone or weight transfer), then join back.
6. **Bones inside the mesh**: move bones fully inside the volume.
7. Non-manifold check: Select All by Trait > Non-Manifold; fix holes or self-intersections (voxel-remeshed proxy).

## Proxy workaround

Make a voxel-remeshed (watertight) copy, auto-weight it, then **Data Transfer** (Vertex Data > Vertex Groups, Nearest Face Interpolated) from the proxy to the real mesh, apply.

## After success

- Normalize All (Weights > Normalize All, lock active off), Limit Total 4 for games, Clean.
- Check deformation with test poses before painting.

## Verify

No warning in the status bar; every deform bone has a non-empty vertex group; a test pose deforms all parts.
