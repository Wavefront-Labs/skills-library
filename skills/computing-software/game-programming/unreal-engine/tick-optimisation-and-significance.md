---
id: computing-software.game-programming.unreal-engine.tick-optimisation-and-significance
name: tick-optimisation-and-significance
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, ue5, performance, tick-optimization, significance-manager, tick-interval, tick-groups, aggregate-ticking, game-programming]
level: advanced
status: draft
description: "Cut game-thread tick cost: disable ticks by default, tick intervals, tick groups and prerequisites, timers and events over Tick, and the Significance Manager for logic LOD."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/actor-ticking-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/significance-manager-in-unreal-engine"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Tick optimisation and significance

**Goal:** hundreds of actors in the world without the game thread drowning in Tick calls.

## Default to not ticking
```cpp
AMyActor::AMyActor()
{
    PrimaryActorTick.bCanEverTick = false;              // most actors never need Tick
}
// Components:
PrimaryComponentTick.bCanEverTick = false;
```
- Blueprint actors: Class Defaults > Start with Tick Enabled off; an empty Event Tick node still costs.
  Project Settings > Engine > General > "Can Blueprints Tick by Default" off for new projects.
- Replace polling with events: overlaps, delegates, `FTimerManager` (`SetTimer(Handle, this, &AX::Check, 0.5f, true)`),
  latent actions, animation notifies.
- Enable/disable dynamically: `SetActorTickEnabled(false)` when idle, on when needed.

## Tick less often
- `PrimaryActorTick.TickInterval = 0.2f;` (use `DeltaSeconds`; it accumulates correctly).
- Tick groups: `TG_PrePhysics` (default), `TG_DuringPhysics`, `TG_PostPhysics`, `TG_PostUpdateWork`.
  Use `AddTickPrerequisiteActor/Component` for ordering instead of reading stale data.
- Animation: `VisibilityBasedAnimTickOption = OnlyTickPoseWhenRendered`, URO (Update Rate Optimisations)
  on skeletal meshes, Animation Budget Allocator plugin for crowds.
- Movement components: `CharacterMovement` is costly; NPC crowds can use simpler movement or
  `bEnableUpdateRateOptimizations`.

## Significance Manager
Plugin `SignificanceManager`: rank objects by a significance function (distance, on-screen, gameplay
importance) and get callbacks when significance changes, to scale tick rate, VFX, animation, AI think rate.
```cpp
USignificanceManager* SM = FSignificanceManagerModule::Get(GetWorld());
SM->RegisterObject(this, TEXT("Enemy"),
    [](USignificanceManager::FManagedObjectInfo* Info, const FTransform& View)
    { return -FVector::DistSquared(CastChecked<AActor>(Info->GetObject())->GetActorLocation(), View.GetLocation()); },
    USignificanceManager::EPostSignificanceType::Sequential,
    [](USignificanceManager::FManagedObjectInfo* Info, float Old, float New, bool bFinal)
    { /* set TickInterval / anim URO / AI rate from New */ });
// Each frame (e.g. in a world subsystem/GameState tick): SM->Update(TArrayView<FTransform>(ViewTransforms));
// On EndPlay: SM->UnregisterObject(this);
```

## Batch instead of N ticks
One manager ticking an array of lightweight structs beats 500 actor ticks (cache-friendly, no per-actor
overhead). Mass Entity takes this further for crowds.

## Measure
`stat game` (Tick time), `dumpticks` (lists all registered tick functions, enabled state), Insights
for per-class tick cost.

## Verify
- [ ] `dumpticks` count drops; no unexpected ticking Blueprints.
- [ ] Distant enemies tick at reduced rate without visible behaviour bugs.
