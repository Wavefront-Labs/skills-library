---
id: computing-software.game-programming.unreal-engine.environment-query-system
name: environment-query-system
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, ue5, unreal-ai, eqs, environment-query-system, generators, tests, contexts, cover-selection, run-eqs-query, game-programming]
level: practitioner
status: draft
description: "Use Unreal EQS to pick positions and targets: generators, tests, scoring vs filtering, custom contexts, running from Behavior Trees, and the EQS testing pawn."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/environment-query-system-overview-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/eqs-node-reference-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/environment-query-system-quick-start-in-unreal-engine"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Environment Query System (EQS)

**Goal:** let AI choose "the best place to stand / thing to target" by generating candidates and
scoring them, instead of hand-coding spatial search.

## Anatomy of a query
1. **Generator** creates items: Points: Grid, Circle, Donut, Cone, Pathing Grid; Actors Of Class;
   Current Location; composite.
2. **Contexts** give reference points: Querier (the AI), custom contexts (e.g. current target from the
   blackboard).
3. **Tests** per item, each set to **Filter**, **Score**, or both:
   - Distance (to context), Dot (facing), Trace (visibility to context), Pathfinding (path exists /
     path length), Overlap, Gameplay Tags, Project (onto navmesh).
   - Scoring equation (linear, square, inverse, constant), clamping, weight (score factor).
4. Result: best item, or all items sorted (`Run Mode`: Single Best Item, Single Random Best 5%/25%, All
   Matching).

## Example: find cover from the target
Generator: Pathing Grid around Querier (radius 1500, spacing 150). Tests: Trace to Target context
(Filter: must be blocked = hidden), Distance to Target (Score: prefer 800-1200 via clamp), Distance
to Querier (Score: inverse, prefer close), Pathfinding (Filter: path exists). Run Mode: Single Best.

## Custom context (target from blackboard)
```cpp
UCLASS()
class UEnvQueryContext_Target : public UEnvQueryContext
{
    GENERATED_BODY()
    virtual void ProvideContext(FEnvQueryInstance& Q, FEnvQueryContextData& Data) const override
    {
        AActor* Querier = Cast<AActor>(Q.Owner.Get());
        const AAIController* C = UAIBlueprintHelperLibrary::GetAIController(Querier);
        AActor* Target = C ? Cast<AActor>(C->GetBlackboardComponent()->GetValueAsObject("TargetActor")) : nullptr;
        if (Target) UEnvQueryItemType_Actor::SetContextHelper(Data, Target);
    }
};
```

## Running
- Behavior Tree: **Run EQS Query** task writes the result to a blackboard key (vector or actor).
- C++: `FEnvQueryRequest(QueryAsset, Querier).Execute(EEnvQueryRunMode::SingleResult, this, &AMyAI::OnQueryDone);`
- Blueprint: Run EQS Query node -> bind to OnQueryFinishedEvent.

## Performance
Order tests cheap-to-expensive (distance/dot before traces and pathfinding); filters early to cut items;
traces and pathfinding on hundreds of points are costly. EQS time-slices queries
(`EnvQueryManager` MaxAllowedTestingTime) so results may arrive frames later: design for latency.

## Debugging
- **EQS Testing Pawn** (place `EQSTestingPawn` in the level, assign the query): shows item scores as
  spheres in the editor without playing.
- Gameplay Debugger category EQS during play.

## Verify
- [ ] Testing pawn shows the expected best points in representative spots.
- [ ] Query time per run is within budget (Insights / `stat ai`).
- [ ] AI never selects unreachable points (pathfinding filter in place).
