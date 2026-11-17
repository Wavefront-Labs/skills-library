---
id: computing-software.game-programming.unreal-engine.gas-ability-costs-and-cooldowns
name: gas-ability-costs-and-cooldowns
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, gameplay-ability-system, ability-cooldown, ability-cost, activation-policy, game-programming]
level: practitioner
status: draft
description: "Implement GAS ability costs and cooldowns with Cost/Cooldown Gameplay Effects, SetByCaller durations, activation policies, instancing, and querying remaining cooldown for UI."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/using-gameplay-abilities-in-unreal-engine", "https://github.com/tranek/GASDocumentation"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# GAS ability costs and cooldowns

**Goal:** abilities that check and pay costs, enforce cooldowns, and expose remaining time to UI —
all predicted on the client.

## Cost
- Create a Gameplay Effect `GE_Cost_Mana`: Instant, modifier on `Mana` Add -20 (or a magnitude
  calculation scaling with level).
- Set the ability's **Cost Gameplay Effect Class**. `CommitAbility()` (or `CommitAbilityCost`) checks
  and applies it; `CanActivateAbility` calls `CheckCost` first.
- Custom cost logic: override `CheckCost`/`ApplyCost` in a base ability class.

## Cooldown
- `GE_Cooldown_Fireball`: **Has Duration**, Granted Tags `Cooldown.Skill.Fireball`. No modifiers needed.
- Set as **Cooldown Gameplay Effect Class**. The ability is blocked while the ASC has any tag from
  the cooldown GE's granted tags.
- One GE per ability gets tedious; common pattern is a single generic cooldown GE with a
  SetByCaller duration and tags supplied by the ability:
```cpp
void UMyAbility::ApplyCooldown(const FGameplayAbilitySpecHandle H, const FGameplayAbilityActorInfo* AI,
                               const FGameplayAbilityActivationInfo Act) const {
    if (UGameplayEffect* CD = GetCooldownGameplayEffect()) {
        FGameplayEffectSpecHandle Spec = MakeOutgoingGameplayEffectSpec(CD->GetClass(), GetAbilityLevel());
        Spec.Data->DynamicGrantedTags.AppendTags(CooldownTags);
        Spec.Data->SetSetByCallerMagnitude(TAG_Data_Cooldown, CooldownDuration.GetValueAtLevel(GetAbilityLevel()));
        ApplyGameplayEffectSpecToOwner(H, AI, Act, Spec);
    }
}
const FGameplayTagContainer* UMyAbility::GetCooldownTags() const { /* return CooldownTags merged with parent */ }
```
  `GetCooldownTags` must be overridden too, or the check uses the generic GE's (empty) tags.

## UI remaining time
```cpp
FGameplayEffectQuery Q = FGameplayEffectQuery::MakeQuery_MatchAnyOwningTags(CooldownTags);
TArray<TPair<float,float>> TimeRemDur = ASC->GetActiveEffectsTimeRemainingAndDuration(Q);
```
Listen to `ASC->RegisterGameplayTagEvent(Tag, EGameplayTagEventType::NewOrRemoved)` for start/end
instead of polling.

## Activation and instancing
- Instancing Policy: Instanced Per Actor (default choice; can hold state), Instanced Per Execution
  (expensive), Non-Instanced (CDO, no state).
- Net Execution Policy: Local Predicted for player skills; Server Only for AI.
- Retrigger Instanced Ability, Activation Blocked/Required Tags for stuns and states.

## Gotchas
- Calling `CommitAbility` late (after a montage) lets players spam during wind-up; commit at start
  unless design says otherwise.
- Predicted cooldown GE on the client can briefly disagree with server time; UI should read the ASC
  effect, not a local timer.

## Verify
- [ ] Ability fails to activate with insufficient mana (CanActivate false, no montage).
- [ ] Cooldown UI matches server under 200 ms simulated latency.
