---
id: creative-arts.animation.blender.lod-generation
name: lod-generation
category: creative-arts
field: animation
product: blender
tags: [blender, lod-generation, lod-chain, game-lods, lod, game-export, decimate, fbx]
level: practitioner
status: docs-checked
description: "Generate an LOD chain in Blender for game engines: Decimate modes, vertex-group protection, _LODn naming for Unity, Unreal LOD import."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/decimate.html
  - https://docs.unity3d.com/Manual/importing-lod-meshes.html
  - https://dev.epicgames.com/documentation/en-us/unreal-engine/fbx-static-mesh-pipeline-in-unreal-engine
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# lod-generation

Goal: a hero mesh plus progressively cheaper versions the engine swaps by distance, all aligned and sharing the same pivot.

## Choosing ratios

Pick a Ratio per LOD by eye and by triangle count; there is no universal table. For characters keep deformation loops (elbows, knees) longer; for props be aggressive. The Decimate Ratio counts triangles, so with Triangulate off a mesh containing quads keeps more faces than the ratio suggests (quads whose edges are not collapsed stay unchanged).

## Workflow

1. Finish LOD0 (applied modifiers, final UVs, custom normals).
2. Duplicate it once per extra LOD and name the copies `MyProp_LOD0`, `MyProp_LOD1`, and so on. Unity reads the `_LODX` suffix (X is the LOD index, LOD0 the most detailed) when importing an FBX and creates a LOD Group automatically; a LOD Group accepts at most eight levels.
3. On each lower copy add a **Decimate** modifier. Collapse merges vertices progressively and offers Symmetry (one axis), Triangulate, and a Vertex Group with a Factor to control which parts are decimated. Un-Subdivide reverses a subdivide on grid-like topology (Iterations: two equal one subdivide, so use even numbers). Planar dissolves geometry under an Angle Limit and can delimit on Normal, Material, Seam, Sharp or UVs, which helps hard-surface props.
4. Decimate does not preview in Edit Mode; check the result in Object Mode, and inspect UVs and normals in the viewport and the UV editor.
5. Export all LODs (plus the armature for skinned meshes) as FBX with modifiers applied.
6. Unity: import the single FBX with the `_LODn` suffixes. Unreal: the FBX pipeline can import LOD meshes made in a DCC tool; make sure *Import LODs* is enabled in the import dialog. LOD meshes should be aligned, occupy the same space and share a pivot point. LODs can also be imported individually through the Static Mesh Editor, or generated inside Unreal with its LOD autogeneration tool (faster for simple meshes; manual is slower but gives the best results on complex ones).

## Gotchas

- Unreal allows different materials, even a different number of materials, on lower LODs; keep slots identical only if your pipeline needs it.
- Check shading after decimating, especially thin parts.
- In Unity, project-wide Quality settings include Maximum LOD Level (exclude meshes above a LOD level from the build) and LOD Bias.

## Checked

2026-11-09. Confirmed against the Blender Decimate manual page (Collapse, Un-Subdivide, Planar options, triangle-based Ratio, no Edit Mode preview), the Unity LOD import page (`_LODX` suffix, automatic LOD Group, eight-level maximum, Quality settings) and the Unreal FBX static mesh page (Import LODs, aligned meshes with shared pivot, per-LOD materials, autogeneration). Removed: fixed percentage table, Data Transfer and Triangulate (Keep Normals) steps, the claim that Blender's FBX exporter writes no LOD group nodes, and the Statistics overlay hint, none of which the pages state.
Method: documentation only; no commands were run.

## Verify

Triangle counts decrease per LOD; in-engine the LOD Group transitions without popping silhouette or shading seams.
