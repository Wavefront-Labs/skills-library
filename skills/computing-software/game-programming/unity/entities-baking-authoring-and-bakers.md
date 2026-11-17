---
id: computing-software.game-programming.unity.entities-baking-authoring-and-bakers
name: entities-baking-authoring-and-bakers
category: computing-software
field: game-programming
product: unity
tags: [unity, dots, unity-dots, entities-baking, baker, authoring-component, subscene, icomponentdata, transformusageflags, entities, game-programming]
level: advanced
status: docs-checked
description: "Unity Entities 1.3 baking: authoring versus runtime data, live and full baking, Baker<T> statelessness and DependsOn, CreateAdditionalEntity, and TransformUsageFlags values."
sources: ["https://docs.unity3d.com/Packages/com.unity.entities@1.3/manual/baking-overview.html", "https://docs.unity3d.com/Packages/com.unity.entities@1.3/manual/baking-baker-overview.html", "https://docs.unity3d.com/Packages/com.unity.entities@1.3/manual/transforms-usage-flags.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Entities baking: authoring components and bakers

**Goal:** convert authoring GameObjects into entities with bakers (Entities 1.3 manual).

## Baking overview
- Baking converts authoring data (GameObjects in authoring scenes; their components are "authoring
  components") into entities written to Entity Scenes (runtime data). It is non-reversible and happens only
  in the Editor, never in-game, like asset importing.
- Any change to authoring data triggers it. Subscene open: live baking, incremental (only modified data)
  or full. Subscene closed: asynchronous full bake in the background asset importer process, so a scene may
  take a few seconds to appear on first load; later loads reuse baked entity scenes.
- Full baking runs when the entity scene is missing or outdated, the baking code assembly has no
  `[BakingVersion]` attribute (assembly modified) or a `[BakingVersion]` changed, the Entities Project
  Settings changed, a reimport is requested from the subscene Inspector (for troubleshooting), or the
  baking cache is cleared in Editor Preferences. Output is files on disk.
- Incremental baking happens in memory on top of the earlier pass and only re-bakes entities depending on
  changed GameObjects. Results can differ from a full bake (entity order, entity size, chunk layout), so
  baking code must stay consistent and not affect the user experience.

## Baker
- Inherit `Baker<TAuthoringType>` (managed generic class; authoring type is usually a MonoBehaviour) and
  override `Bake`. Unity calls it on every authoring component it needs to bake: all of them in full
  baking, only modified ones or those with modified dependencies in incremental baking.
- A baker is instantiated once and `Bake` is called many times in non-deterministic order; bakers must be
  stateless and access data through methods. Caching any value in the baker makes baking misbehave.
- Unity records everything a baker produces (to undo it before a rebake) and everything it accesses (to
  trigger rebakes), through the baker's own member functions.
- A baker can only add components to the primary entity and to additional entities it creates itself.
- Page example: `var entity = GetEntity(TransformUsageFlags.Dynamic); AddComponent(entity, new
  RotationSpeed { RadiansPerSecond = math.radians(authoring.DegreesPerSecond) });` plus
  `CreateAdditionalEntity(TransformUsageFlags.Dynamic, entityName: "Additional A")`.
- Dependencies: fields on the authoring component are tracked automatically. Other sources (other
  components, GameObjects, assets) need the Baker methods (`GetComponent<T>()`, `GetComponent<T>(other)`)
  instead of the GameObject ones, and `DependsOn(reference)` for external references (declare it before
  any early out, since a null can be a "fake null" that returns). `GetComponent` returning null still
  registers a dependency, so adding the component later re-triggers the baker. Needed only when data is
  read through the reference; a reference carried over unread needs no dependency.

## TransformUsageFlags
- `None`: no specific requirement (other bakers may add flags). `Renderable`: needs transform components
  to render, not to move. `Dynamic`: moves at runtime. `WorldSpace`: must be in world space even with a
  dynamic parent. `NonUniformScale`. `ManualOverride`: ignore flags from other bakers on the same
  GameObject; no transform components added.
- Required whenever an entity is accessed in a baker. Default component bakers add flags (the
  `MeshRenderer` baker adds `Renderable`). Multiple flags are combined. Entity prefabs are automatically
  marked Dynamic.
- Page example: a building and its window, both `Renderable`, need no hierarchy and are combined into a
  `LocalToWorld` in world space, without `LocalTransform` or `Parent`. With a Dynamic ship parent and a
  Renderable window, the window gets `LocalToWorld`, `LocalTransform` and `Parent` at runtime to follow it.

## Checked
Date: 2026-11-07

Read in full: the Baking overview, Baker overview (including both code examples) and Transform usage flags
pages. The Baker API, TransformUsageFlags API, baking systems, `TemporaryBakingType` and subscene pages
were not opened.

Removed because the three pages do not confirm it: the "GameObject > New Sub Scene" menu, the streaming
claim, `SpinnerAuthoring` / `ProjectileSpawner` sample and `GetEntity(prefab, flags)`, per-flag component
lists (`Renderable` gets only `LocalToWorld`, `WorldSpace` flattening, `None` for config singletons),
"static level geometry should be Renderable" and "Dynamic everywhere wastes transform time", the
`a.transform` advice, the `[WorldSystemFilter(BakingSystem)]` and `[TemporaryBakingType]` post-processing
paragraph, the Entities Hierarchy / Baking Preview / Clear Entity Cache debugging steps, and the Verify
list. Not on the page: "Preferences > Entities" menu path (the page only says Editor Preferences).

Method: documentation only; no commands were run.
