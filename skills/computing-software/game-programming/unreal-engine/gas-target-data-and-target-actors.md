---
id: computing-software.game-programming.unreal-engine.gas-target-data-and-target-actors
name: gas-target-data-and-target-actors
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, target-data, gameplay-ability-system, gas, targeting, prediction, game-programming]
level: practitioner
status: draft
description: "Pass GAS targeting through FGameplayAbilityTargetDataHandle: WaitTargetData with target actors, custom target data structs, client-to-server replication and validation."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/gameplay-ability-tasks-in-unreal-engine", "https://docs.unrealengine.com/5.3/en-US/API/Plugins/GameplayAbilities/Abilities/FGameplayAbilityTargetData/", "https://github.com/tranek/GASDocumentation"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# GAS target data and target actors

**Goal:** an ability gets "what was aimed at" on the server, predicted from the client, without
custom RPCs.

## Target data
`FGameplayAbilityTargetDataHandle` holds one or more `FGameplayAbilityTargetData` structs:
`FGameplayAbilityTargetData_SingleTargetHit` (an `FHitResult`), `_ActorArray`, `_LocationInfo`.
Effects can be applied to all targets: `ApplyGameplayEffectToTarget(Handle, ...)`.

## Target actors with WaitTargetData
```cpp
UAbilityTask_WaitTargetData* Task = UAbilityTask_WaitTargetData::WaitTargetData(
    this, NAME_None, EGameplayTargetingConfirmation::UserConfirmed, AGameplayAbilityTargetActor_GroundTrace::StaticClass());
Task->ValidData.AddDynamic(this, &UMyAbility::OnTargetData);
Task->Cancelled.AddDynamic(this, &UMyAbility::OnTargetCancelled);
AGameplayAbilityTargetActor* TA;
if (Task->BeginSpawningActor(this, AGameplayAbilityTargetActor_GroundTrace::StaticClass(), TA)) {
    /* configure TA (range, reticle) */ Task->FinishSpawningActor(this, TA);
}
Task->ReadyForActivation();
```
Confirmation types: Instant, UserConfirmed (bound to ASC confirm/cancel input), Custom, CustomMulti.
Target actors are heavyweight (spawned actor, visuals); spawn and keep one for reuse
(`WaitTargetDataUsingActor`) for repeated targeting.

## Lightweight custom path
Many projects skip target actors: trace on the client in the ability, build the handle and send it:
```cpp
FScopedPredictionWindow W(ASC, IsPredictingClient());
ASC->ServerSetReplicatedTargetData(Handle, ActivationInfo.GetActivationPredictionKey(), Data,
    FGameplayTag(), ASC->ScopedPredictionKey);
```
Server listens with `AbilityTargetDataSetDelegate(Handle, Key).AddUObject(...)` and calls
`CallReplicatedTargetDataDelegatesIfSet` in case data arrived before binding; then
`ConsumeClientReplicatedTargetData`.

## Custom target data
Derive from `FGameplayAbilityTargetData`, implement `GetScriptStruct`, `NetSerialize`, and add
`TStructOpsTypeTraits` with `WithNetSerializer = true`.

## Validation
The server must sanity check client target data (distance, line of sight, cooldown) before applying
effects; clients can send anything.

## Verify
- [ ] With 150 ms simulated latency, the client sees immediate feedback and the server applies effects
  to the same target once.
