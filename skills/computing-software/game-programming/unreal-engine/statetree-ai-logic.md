---
id: computing-software.game-programming.unreal-engine.statetree-ai-logic
name: statetree-ai-logic
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, ue5, unreal-ai, statetree, state-tree-task, evaluators, transitions, schema, mass-ai, game-programming]
level: advanced
status: draft
description: "Build AI and gameplay logic with Unreal StateTree: schemas, states with tasks, enter conditions and transitions, evaluators/global tasks, C++ task structs and debugging."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/state-tree-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/state-tree-quick-start-guide", "https://dev.epicgames.com/documentation/en-us/unreal-engine/overview-of-state-tree-in-unreal-engine"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# StateTree

**Goal:** AI or object logic as a hierarchical state machine with behaviour-tree-like selection,
running efficiently (also usable for Mass entities and smart object interactions).

## Concepts
- **Schema**: what the tree runs on (`StateTree AI Component` schema for AIControllers,
  `StateTree Component` for any actor, Mass schemas). Defines available context (Actor, AIController).
- **States** are hierarchical. Selection starts at the root and descends into the first child whose
  **Enter Conditions** pass (like a selector). Leaf states are active along with their parents.
- **Tasks** run while a state is active (`EnterState`, `Tick`, `ExitState`); a task completing
  (Succeeded/Failed) can trigger transitions.
- **Transitions**: On State Completed / Succeeded / Failed / On Event (gameplay tag events) / On Tick
  with conditions; targets: a state, Next State, Parent, Tree Succeeded/Failed.
- **Global tasks and evaluators** run for the whole tree (gather data such as current target, expose it
  to bindings).
- **Property binding**: task inputs bind to evaluator outputs, context, or parameters, no blackboard.

## Example layout
```
Root
  Dead            (enter: Health <= 0)            task: PlayDeath
  Combat          (enter: HasTarget)
     Reload       (enter: Ammo == 0)              task: Reload -> on completed: Combat
     Attack                                       tasks: FaceTarget, Fire
  Investigate     (enter: HeardNoise)             task: MoveTo(NoiseLocation)
  Patrol                                          task: MoveAlongSpline
```

## C++ task
```cpp
USTRUCT()
struct FMyFireTaskInstanceData
{
    GENERATED_BODY()
    UPROPERTY(EditAnywhere, Category=Input) TObjectPtr<AActor> Target = nullptr;
    UPROPERTY(EditAnywhere, Category=Parameter) float Interval = 0.2f;
    float Cooldown = 0.f;
};

USTRUCT(meta=(DisplayName="Fire At Target"))
struct FMyFireTask : public FStateTreeTaskCommonBase
{
    GENERATED_BODY()
    using FInstanceDataType = FMyFireTaskInstanceData;
    virtual const UStruct* GetInstanceDataType() const override { return FInstanceDataType::StaticStruct(); }

    virtual EStateTreeRunStatus Tick(FStateTreeExecutionContext& Context, const float DeltaTime) const override
    {
        FInstanceDataType& D = Context.GetInstanceData(*this);
        if (!D.Target) return EStateTreeRunStatus::Failed;
        if ((D.Cooldown -= DeltaTime) <= 0.f) { /* fire */ D.Cooldown = D.Interval; }
        return EStateTreeRunStatus::Running;
    }
};
```
Tasks are const structs; per-instance state lives in instance data (like BT node memory).

## StateTree vs Behavior Tree
StateTree: explicit states and transitions, cheaper, data binding, good for both simple actors and AI.
BT: mature tooling (EQS integration, decorators with observer aborts). Many UE5 projects use StateTree
for new AI.

## Debugging
StateTree debugger (Window > StateTree Debugger, UE 5.2+): record a session, scrub the timeline of
active states and transitions per instance. Visual Logger also records StateTree events.

## Verify
- [ ] Debugger shows expected state changes for scripted test scenarios.
- [ ] No state lacks an exit path (completed/failed transitions defined).
- [ ] Per-instance data used for all mutable task state (multiple AI do not interfere).
