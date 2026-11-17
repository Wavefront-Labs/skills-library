---
id: computing-software.game-programming.unity.static-editor-flags
name: static-editor-flags
category: computing-software
field: game-programming
product: unity
tags: [unity, static-editor-flags, static-batching, lightmapping, occlusion, navigation, game-programming]
level: practitioner
status: docs-checked
description: "Set Unity Static Editor Flags correctly per object (Contribute GI, Occluder/Occludee, Batching, Navigation, Reflection Probe) instead of ticking Static on everything."
sources: ["https://docs.unity3d.com/Manual/StaticObjects.html", "https://docs.unity3d.com/ScriptReference/StaticEditorFlags.html", "https://docs.unity3d.com/Manual/static-batching.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Static editor flags

**Goal:** each non-moving object opts into exactly the precomputations it benefits from.

## The flags (Inspector Static dropdown)
| Flag | Used by | Tick when |
|---|---|---|
| Contribute GI | global illumination at bake time | the Mesh Renderer should take part in baked GI; only takes effect if the Scene enables a GI setting (Baked GI or Enlighten Realtime GI) |
| Occluder Static | occlusion culling | large blockers |
| Occludee Static | occlusion culling | objects that may be hidden |
| Batching Static | static batching | meshes that can be combined with other eligible meshes |
| Navigation Static | legacy navigation bake | deprecated: cannot be set in the menu, only in code via `StaticEditorFlags.NavigationStatic`; use NavMesh Modifier with NavMesh Surfaces instead |
| Off Mesh Link Generation | legacy navigation bake | deprecated in the same way (`StaticEditorFlags.OffMeshLinkGeneration`) |
| Reflection Probe | Reflection Probes whose Type is Baked | the object should appear in baked probe data |

The checkbox sets the value to Everything or Nothing. Include an object only in systems that need it: the
Manual warns that extra inclusion can cause wasted calculations, unnecessarily large data files, or
unexpected behaviour.

## Scripted setup
```csharp
var f = StaticEditorFlags.ContributeGI | StaticEditorFlags.OccludeeStatic | StaticEditorFlags.ReflectionProbeStatic;
GameObjectUtility.SetStaticEditorFlags(go, f);
```
Read flags back with `GameObjectUtility.GetStaticEditorFlags`. The Manual also names `GameObject.isStatic`
for setting the property in code.

## Static batching
Static batching combines meshes that use the same material into one vertex buffer and one index buffer in
world space. Each buffer holds up to 64,000 vertices, but Unity can create multiple batches. Limits:
Mesh Renderers only (no Skinned Mesh Renderers); batching of transparent objects may be limited because
Unity sorts meshes back-to-front before batching. Combined meshes cannot be culled individually.

## Gotchas
- Setting Static Editor Flags at runtime has no effect on these systems.
- Flags are consumed by editor-time precomputation; change them in the Editor and re-bake.

## Checked
Date 2026-11-09. Confirmed against the Unity Manual pages Static GameObjects and Introduction to static
batching, and the StaticEditorFlags script reference (read in full as fetched text): flag meanings, Contribute GI
precondition, deprecated navigation flags and their code-only access, runtime-no-effect, 64,000 vertex limit,
Mesh Renderer only, transparent sorting note. Removed unconfirmed claims: memory duplication of high-poly
batched meshes, SRP Batcher and GPU Resident Drawer comparisons, lightmap UV requirement, "cannot move"
behaviour of batched objects, and the Frame Debugger verification checklist.
Method: documentation only; no commands were run.
