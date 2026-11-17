---
id: computing-software.game-programming.unreal-engine.actor-lifecycle-and-initialization-order
name: actor-lifecycle-and-initialization-order
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, uclass, actor-lifecycle, beginplay, endplay, game-programming]
level: practitioner
status: docs-checked
description: "Know Unreal's AActor lifecycle: load from disk, PIE, SpawnActor and deferred spawn paths, then Destroy, EndPlay and garbage-collection callbacks, per Epic's Actor Lifecycle page."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-actor-lifecycle", "https://dev.epicgames.com/documentation/en-us/unreal-engine/actors-in-unreal-engine"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Actor lifecycle and initialisation order

**Goal:** know which callback runs at which point of an Actor's life, so setup and cleanup go in the right one.

## Load from disk (actors already in a level)
Applies to `UEngine::LoadMap` and level streaming (`UWorld::AddToWorld`). Order on the page:
1. Actor loaded from the package, then `PostLoad` (custom versioning and fixup go here). `PostLoad` is mutually
   exclusive with `AActor::PostActorCreated`.
2. `UAISystemBase::InitializeActorsForPlay`, then `ULevel::RouteActorInitialize` for non-initialised Actors and
   seamless-travel carry-over.
3. `AActor::PreInitializeComponents`, `UActorComponent::InitializeComponent` per component,
   `AActor::PostInitializeComponents`.
4. `AActor::BeginPlay` "when the level is started".

Play in Editor copies Actors from the editor into a new World (`UObject::PostDuplicate`), then follows the same
initialisation steps.

## Spawning (`UWorld::SpawnActor`)
`UWorld::SpawnActor` -> `AActor::PostSpawnInitialize` -> `AActor::PostActorCreated` (the page says constructor-style
behaviour for spawned Actors goes here) -> `AActor::ExecuteConstruction` (`AActor::OnConstruction`, where Blueprint
Actors get their components and variables initialised) -> `AActor::PostActorConstruction`
(`PreInitializeComponents`, `InitializeComponent`, `PostInitializeComponents`) -> `UWorld::OnActorSpawned` broadcast ->
`AActor::BeginPlay`.

## Deferred spawn
The page says an Actor is deferred-spawned when properties are set to "Expose on Spawn", and that
`UWorld::SpawnActorDeferred` is meant for procedural Actors and allows extra setup before the Blueprint construction
script. Everything in `SpawnActor` happens, but after `PostActorCreated` you do setup with a valid but incomplete
instance, then `AActor::FinishSpawning` resumes at `ExecuteConstruction`.

## End of life
- `AActor::Destroy` marks the Actor pending kill and removes it from the level's array of Actors.
- `AActor::EndPlay` is called from: an explicit `Destroy`, end of Play in Editor, level transitions (seamless travel or
  load map), unload of a streaming level containing the Actor, expiry of the Actor's lifetime, and application shutdown.
- Actors may survive `EndPlay`: the page's example is `s.ForceGCAfterLevelStreamedOut` false with a quickly reloaded
  sublevel, where the same Actor can be "resurrected" with its non-reset local variables.
- `AActor::OnDestroyed` is described as a legacy response to `Destroy`; Epic recommends moving that logic into
  `EndPlay`.
- Rather than checking pending kill manually, the page suggests an `FWeakObjectPtr<AActor>`.

## Garbage collection callbacks
`UObject::BeginDestroy` (free memory and multithreaded resources such as graphics-thread proxies; most gameplay
cleanup should already be in `EndPlay`), `UObject::IsReadyForFinishDestroy` (returning false defers destruction to a
later GC pass), `UObject::FinishDestroy` (last call before memory is freed). The page also notes GC builds clusters of
objects destroyed together, and that Project Settings > Garbage Collection > Create Garbage Collector UObject Clusters
can be set false; Epic recommends that only when performance testing shows a benefit.

## Checked
Date: 2026-11-07. Read in full: the Actor Lifecycle page (sections Load from Disk, Play in Editor, Spawning, Deferred
Spawn, End of Actor Lifecycle, Garbage Collection, Advanced Garbage Collection) and the Actors page (Ticking,
Lifecycle, Destroying Actors), as served at the unversioned en-us URLs; the pages state no engine version. The flow
chart image on the lifecycle page is not readable as text.
Trimmed as not confirmed by either page: the constructor/CDO advice, `bWantsInitializeComponent`, the `EEndPlayReason`
value list, `Super::BeginPlay` advice, network `OnRep_`/`PostNetInit` nuance, `ConstructorHelpers`, `RegisterComponent`,
BeginPlay ordering between actors, and the invented Verify checklist.
Method: documentation only; no commands were run.
