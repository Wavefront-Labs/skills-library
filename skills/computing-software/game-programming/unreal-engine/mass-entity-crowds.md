---
id: computing-software.game-programming.unreal-engine.mass-entity-crowds
name: mass-entity-crowds
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, mass-entity, mass-ai, ecs, crowds, data-oriented, game-programming]
level: practitioner
status: draft
description: "Simulate large crowds with Unreal Mass Entity: fragments, tags, processors and queries, entity configs and traits, LOD and representation via ISM and actors."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/overview-of-mass-entity-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/mass-entity-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/mass-avoidance-in-unreal-engine"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mass Entity crowds

**Goal:** thousands of agents (pedestrians, swarms) simulated data-oriented, rendered cheaply.

## Concepts
- **Entity**: ID. **Fragments**: plain structs of data (`FMassVelocityFragment`). **Tags**: fragments with no data; their presence or absence is used for filtering. **Shared fragments**: one instance of parameter data shared by many entities. **Chunk fragments**: data per chunk (for example LOD calculations). Chunks store entities of the
  same archetype contiguously.
- **Processors** (`UMassProcessor`): run queries over matching entities each frame, in configured
  phases and order.
- **Traits** in a **Mass Entity Config** asset bundle fragments and processors for designers;
  **Mass Spawner** actors spawn entities from configs.

## Processor
```cpp
USTRUCT() struct FWanderFragment : public FMassFragment { GENERATED_BODY() FVector Target; };

UCLASS() class UWanderProcessor : public UMassProcessor { GENERATED_BODY()
public:
    UWanderProcessor() : Query(*this) { ExecutionOrder.ExecuteInGroup = UE::Mass::ProcessorGroupNames::Movement; }
protected:
    void ConfigureQueries() override {
        Query.AddRequirement<FTransformFragment>(EMassFragmentAccess::ReadWrite);
        Query.AddRequirement<FWanderFragment>(EMassFragmentAccess::ReadOnly);
    }
    void Execute(FMassEntityManager& EM, FMassExecutionContext& Ctx) override {
        Query.ForEachEntityChunk(EM, Ctx, [](FMassExecutionContext& C) {
            auto Transforms = C.GetMutableFragmentView<FTransformFragment>();
            auto Wander = C.GetFragmentView<FWanderFragment>();
            const float Dt = C.GetDeltaTimeSeconds();
            for (int32 i = 0; i < C.GetNumEntities(); ++i) {
                FTransform& T = Transforms[i].GetMutableTransform();
                T.AddToTranslation((Wander[i].Target - T.GetLocation()).GetSafeNormal() * 100.f * Dt);
            }
        });
    }
    FMassEntityQuery Query;
};
```
(API names shift between 5.x versions. Current API docs list `FMassEntityQuery::ForEachEntityChunk` overloads both with and without the `FMassEntityManager&` argument, and a newer simplified processor/query API exists; confirm against `MassEntityQuery.h` for your engine version. The code above was not compiled.)

## Representation and LOD
MassRepresentation traits switch per LOD: high-res Actor near the camera, ISM far away, nothing when
culled. Mass LOD processors compute LOD from viewer distance and reduce processing frequency for far
entities. MassCrowd, MassAvoidance, MassNavigation, ZoneGraph and StateTree integrations give
pedestrians lanes, avoidance and behaviour.

## Gotchas
- Structural changes (adding fragments/tags) inside processors must be deferred via
  `Ctx.Defer()` commands (the MassCommandBuffer; changes apply at the end of the processing batch).
- Epic's overview page does not state a maturity level; treat parts as experimental, pin to an engine version and follow City Sample patterns.
- Debug with the Mass Debugger (Epic has a Mass Debugger Overview page); the `mass.debug` console commands and the 5.2+ window claim were not confirmed.

## Verify
- [ ] Insights shows Mass processors scaling with entity count and far entities ticking less often.
