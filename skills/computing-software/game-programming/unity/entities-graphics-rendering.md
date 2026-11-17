---
id: computing-software.game-programming.unity.entities-graphics-rendering
name: entities-graphics-rendering
category: computing-software
field: game-programming
product: unity
tags: [unity, entities-graphics, dots, ecs, brg, rendering, game-programming]
level: practitioner
status: docs-checked
description: "Entities Graphics 1.4: RenderMeshUtility.AddComponents, RenderMeshArray, MaterialMeshInfo, instancing a prototype entity, built-in and custom Shader Graph material overrides."
sources: ["https://docs.unity3d.com/Packages/com.unity.entities.graphics@1.4/manual/index.html", "https://docs.unity3d.com/Packages/com.unity.entities.graphics@1.4/manual/runtime-entity-creation.html", "https://docs.unity3d.com/Packages/com.unity.entities.graphics@1.4/manual/material-overrides-code.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Entities Graphics rendering

**Goal:** create rendered ECS entities at runtime and override material properties per entity.

## What it is
Provides systems and components for rendering ECS entities. It is not a render pipeline: it collects the
data needed and sends it to Unity's existing rendering architecture. URP and HDRP author the content and
define the rendering passes. (Requirements and compatibility are on a separate page, not opened.)

## Runtime entity creation
- Rendering needs a substantial set of components that may change between versions, so use
  `RenderMeshUtility.AddComponents(entity, entityManager, RenderMeshDescription, RenderMeshArray,
  MaterialMeshInfo)`. The `RenderMesh` overload is only used during GameObject baking; at runtime use the
  `RenderMeshArray` version.
- `RenderMeshDescription` describes when and how to draw, containing `RenderFilterSettings` (layering,
  shadowing, motion vectors, light probe usage). Page example:
  `new RenderMeshDescription(shadowCastingMode: ShadowCastingMode.Off, receiveShadows: false)`.
- `RenderMeshArray`: meshes and materials shared by a collection of entities. An entity selects from it
  with `MaterialMeshInfo.FromRenderMeshArrayIndices(...)` (page example `(0, 0)`).
  In baking, all meshes and materials in a subscene are packed into one shared `RenderMeshArray` to
  minimise chunk fragmentation.
- `MaterialMeshInfo`: Burst-compatible plain data; refers either to array indices in a `RenderMeshArray`
  on the same entity or directly to mesh and material IDs registered beforehand.
- `AddComponents` is main-thread only and not suitable for creating many entities. Best practice: build a
  base (prototype) entity (baked from a prefab or created with `AddComponents`; same instantiation
  performance) and clone it with Instantiate, then `SetComponent` values such as `LocalToWorld`.
  Reasons given: no resource-intensive structural changes, usable from Burst jobs with
  `EntityCommandBuffer.ParallelWriter`, and internal components are pre-created.
- Page example: an `IJobParallelFor` calls `Ecb.Instantiate(index, Prototype)` then
  `Ecb.SetComponent(index, e, new LocalToWorld { Value = float4x4.Translate(...) })`, with the prototype
  also given `AddComponentData(prototype, new LocalToWorld())`; schedule, `Complete`, then
  `ecb.Playback(entityManager)` and `Dispose`.

## Material overrides
- Built-in `IComponentData` overrides exist; supply colours in linear space (no automatic gamma
  conversion). URP list: BaseColor, BumpScale, Cutoff, EmissionColor, Metallic, OcclusionStrength,
  Smoothness, SpecColor. HDRP has a longer list (for example AlphaCutoff, BaseColor, EmissiveColor,
  Metallic, Smoothness, SpecularColor, Thickness, UnlitColor). For properties not listed, use custom Shader
  Graph overrides.
- Custom Shader Graph property: in the Graph Inspector Node Settings tab enable Override Property
  Declaration and set Shader Declaration to Hybrid Per Instance. Then a struct with
  `[MaterialProperty("_Color")]` (name must match the Reference exactly) holding the value, e.g.
  `public float4 Value;`.
- A matching `IComponentData` is needed for every Hybrid Per Instance property; otherwise Entities
  Graphics zero fills it.

## Checked
Date: 2026-11-07

Read in full: the Entities Graphics index page, the Runtime entity creation page including the full
example, and the Material overrides using C# page. The Requirements, Getting started, baking and
`RenderMeshArray` pages were not opened.

Removed because the three pages do not confirm it: the URP/HDRP requirement statements (built-in pipeline
unsupported, Forward+), `DOTS_INSTANCING_ON` pragma and `UNITY_DOTS_INSTANCING` blocks, the list of
components added when baking MeshRenderers (`RenderBounds`, `WorldRenderBounds`, `MeshLODComponent`), the
Entities Hierarchy checks, the "ecb.Instantiate(prefab)" one-liner, the structural-change gotcha for
changing `RenderMeshArray`, the Scene View Mode preference, and the Verify list. Corrected the draft's
claim that `AddComponents` per call is "slow": the page says it is main-thread only and unsuited to
creating many entities. `MaterialMeshInfo.FromRenderMeshArrayIndices` argument meaning beyond the
example `(0, 0)` is not stated on the page.

Method: documentation only; no commands were run.
