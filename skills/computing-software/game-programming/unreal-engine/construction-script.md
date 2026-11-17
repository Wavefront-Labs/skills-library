---
id: computing-software.game-programming.unreal-engine.construction-script
name: construction-script
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, blueprints, construction-script, onconstruction, editor-procedural-setup, game-programming]
level: practitioner
status: draft
description: "Use Unreal Blueprint construction scripts and C++ OnConstruction for editor-time procedural setup, knowing when they rerun and what must not go there."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/construction-script-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Runtime/Engine/GameFramework/AActor/OnConstruction"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Construction script

**Goal:** level designers see procedural setups (fences, spline meshes, randomised props) update live
in the editor, without runtime cost or surprises.

## When it runs
- In the editor: on placement, on every property change, on move (every drag frame unless
  `bRunConstructionScriptOnDrag = false`), on Blueprint compile, on level load.
- At runtime: when the actor is spawned (`SpawnActor`), before BeginPlay. For placed actors in cooked
  builds, results are serialized; the script does not rerun on load.
- C++: override `virtual void OnConstruction(const FTransform& Transform) override;` (Blueprint
  construction script runs after it).

## Good uses
- Adding instanced static mesh instances along a spline.
- Applying a material parameter from an exposed variable.
- Validating/clamping exposed properties.
- Setting up dynamic material instances (`CreateDynamicMaterialInstance`) — re-created on rerun.

## Bad uses
- Spawning actors (creates orphans every rerun; use child actor components cautiously or editor
  utilities).
- Reading other actors' state (order undefined, may not exist).
- Gameplay logic, timers, random without a seed (`RandomStream` with a seed property keeps results
  stable across reruns).
- Heavy work: it runs on every drag tick — designers will feel it.

## Components added in construction
`Add ... Component` nodes in construction create components owned by construction (destroyed and
recreated each run). Don't store references to them across runs; they are not editable per instance.

## Gotchas
- `bRunConstructionScriptOnDrag` false in class defaults for heavy scripts.
- Level Instance/World Partition: construction scripts run when actors load in editor.
- Changing a property from inside the construction script that itself triggers construction can loop
  (avoid writing exposed properties).

## Verify
- [ ] Drag the actor: editor stays responsive.
- [ ] Cook and run: placed actor matches what the editor showed.
