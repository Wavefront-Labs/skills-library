---
id: computing-software.game-programming.unreal-engine.bt-decorators-services-and-observer-aborts
name: bt-decorators-services-and-observer-aborts
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, unreal-ai, bt-observer-aborts, bt-decorator, bt-service, game-programming]
level: practitioner
status: draft
description: "Use Unreal Behavior Tree decorators and services well: blackboard conditions, observer aborts Self/LowerPriority/Both, cooldowns, and service tick intervals."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/behavior-tree-node-reference-decorators-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/behavior-tree-node-reference-services-in-unreal-engine"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# BT decorators, services and observer aborts

**Goal:** event-driven behaviour trees that react immediately to blackboard changes instead of
polling.

## Decorators
Conditions attached to composites/tasks: Blackboard (key set / compare), Cooldown, Loop, Time Limit,
Cone Check, Does Path Exist, Gameplay Tag Condition, Is At Location, Force Success, Conditional Loop.
Custom: `UBTDecorator` with `CalculateRawConditionValue`, or Blueprint `BTDecorator_BlueprintBase`
with `PerformConditionCheckAI`.

## Observer aborts (UE's key BT feature)
On a Blackboard decorator, **Observer Aborts**:
- **None**: checked only when the branch is entered.
- **Self**: if the condition becomes false while this branch runs, abort it.
- **Lower Priority**: if the condition becomes true while a lower-priority (right-hand) branch runs,
  abort that branch and run this one.
- **Both**: Self + Lower Priority.
Notify Observer: On Result Change vs On Value Change (key compare decorators).

Typical: `Selector [ (BB: TargetActor Is Set, Aborts Both) -> Attack ; Patrol ]`. Patrol gets
interrupted the moment perception sets TargetActor, and Attack aborts when it clears.

## Services
Run on a composite while active, at Interval +/- Random Deviation: update blackboard (distance to
target, best cover), not perform actions. Custom: `UBTService` `TickNode`, `OnBecomeRelevant`.
Keep intervals 0.2-0.5 s for most; services firing every frame across 100 AIs show up in profiles.

## Tasks and abort handling
Custom tasks returning `InProgress` must implement `AbortTask` (stop movement, montages) and call
`FinishLatentAbort`; otherwise aborts hang or leave AI moving.

## Gotchas
- Observer aborts only react to **blackboard** changes; decorators reading other state (custom C++
  conditions) need `RequestExecution` / or be blackboard-driven.
- Lower Priority aborts require the decorator be on a node that is a child of a composite with
  lower-priority siblings to the right.
- Moving AI with `MoveTo` task aborted mid-path keeps velocity briefly; stop explicitly if needed.

## Verify
- [ ] Behavior Tree debugger (PIE, select AI) shows instant branch switch when the key changes.
- [ ] `stat AI` / Insights: services not dominating with full AI count.
