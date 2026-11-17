---
id: computing-software.game-programming.unreal-engine.gas-asc-replication-mode-and-attribute-onrep
name: gas-asc-replication-mode-and-attribute-onrep
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, gas-replication-mode, gameplay-ability-system, attributes, replication, game-programming]
level: practitioner
status: draft
description: "Choose the GAS AbilitySystemComponent replication mode (Full, Mixed, Minimal), place the ASC on PlayerState or Pawn, and write attribute OnRep with GAMEPLAYATTRIBUTE_REPNOTIFY."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/gameplay-attributes-and-attribute-sets-for-the-gameplay-ability-system-in-unreal-engine", "https://docs.unrealengine.com/5.3/en-US/API/Plugins/GameplayAbilities/EGameplayEffectReplicationMode/", "https://github.com/tranek/GASDocumentation"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ASC replication mode and attribute OnRep

**Goal:** abilities, effects and attributes replicate correctly at sensible bandwidth.

## Replication modes
`ASC->SetReplicationMode(EGameplayEffectReplicationMode::Mixed);`
| Mode | Gameplay Effects replicate to | Use |
|---|---|---|
| Full | everyone | single player / small co-op |
| Mixed | owner gets full GEs; others get only tags and cues | player-controlled characters |
| Minimal | nobody (tags and cues only) | AI-controlled characters |
Mixed requires the ASC owner's Owner to be the Controller (PlayerState owner is the controller by
default; for a Pawn-owned ASC, `SetOwner(Controller)` happens on possess).

## Where the ASC lives
- **PlayerState**: survives respawn, keeps attributes/cooldowns. Raise PlayerState
  `NetUpdateFrequency` (default very low; 100 in GAS docs) or attribute changes lag.
- **Pawn**: simpler for AI and characters that do not respawn.
Init on both server and client: `ASC->InitAbilityActorInfo(OwnerActor, AvatarActor)` in
`PossessedBy` (server) and `OnRep_PlayerState` (client) for PlayerState-owned ASCs.

## Attribute replication
```cpp
UPROPERTY(BlueprintReadOnly, ReplicatedUsing = OnRep_Health) FGameplayAttributeData Health;
ATTRIBUTE_ACCESSORS(UMyAttributeSet, Health)
UFUNCTION() void OnRep_Health(const FGameplayAttributeData& Old) { GAMEPLAYATTRIBUTE_REPNOTIFY(UMyAttributeSet, Health, Old); }

void UMyAttributeSet::GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& Out) const {
    Super::GetLifetimeReplicatedProps(Out);
    DOREPLIFETIME_CONDITION_NOTIFY(UMyAttributeSet, Health, COND_None, REPNOTIFY_Always);
}
```
`REPNOTIFY_Always` matters: client prediction may already have set the same value; the macro informs
the ASC so attribute-change delegates fire and predicted values reconcile.

## Gotchas
- Listen for UI updates with `GetGameplayAttributeValueChangeDelegate(Attr)`, not OnRep directly.
- Attributes that only the owner needs (ammo, mana) can use `COND_OwnerOnly`.
- Minimal mode with abilities that need GE spec data on simulated proxies breaks those features.

## Verify
- [ ] Network profiler shows attribute traffic proportional to changes; clients see correct values.
