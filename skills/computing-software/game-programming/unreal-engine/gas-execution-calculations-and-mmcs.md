---
id: computing-software.game-programming.unreal-engine.gas-execution-calculations-and-mmcs
name: gas-execution-calculations-and-mmcs
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, gameplay-ability-system, execution-calculation, modifier-magnitude-calculation, damage-formula, game-programming]
level: practitioner
status: draft
description: "Write GAS damage formulas with UGameplayEffectExecutionCalculation and Modifier Magnitude Calculations: capturing attributes, snapshotting, SetByCaller and meta attributes."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/gameplay-effects-for-the-gameplay-ability-system-in-unreal-engine", "https://github.com/tranek/GASDocumentation#concepts-ge-ec"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# GAS execution calculations and MMCs

**Goal:** damage/heal formulas that read source and target attributes correctly, predict where
possible, and keep attribute sets clean.

## Pick the tool
| Need | Use |
|---|---|
| A magnitude from attributes for one modifier (cost scaling with level and Intelligence) | **MMC** `UGameplayModMagnitudeCalculation` — predictable, works with all GE durations |
| Multi-attribute formula changing several attributes (armour, crits, shields) | **Execution** `UGameplayEffectExecutionCalculation` — Instant/Periodic only, **not predicted** |
| Value supplied by the ability at runtime | SetByCaller magnitude (tag or name keyed) |

## Execution calculation skeleton
```cpp
struct FDamageStatics {
    DECLARE_ATTRIBUTE_CAPTUREDEF(AttackPower); DECLARE_ATTRIBUTE_CAPTUREDEF(Armor);
    FDamageStatics() {
        DEFINE_ATTRIBUTE_CAPTUREDEF(UCombatSet, AttackPower, Source, /*Snapshot*/ true);
        DEFINE_ATTRIBUTE_CAPTUREDEF(UCombatSet, Armor, Target, false);
    }
};
static const FDamageStatics& DS() { static FDamageStatics S; return S; }
UDamageExec::UDamageExec() { RelevantAttributesToCapture.Add(DS().AttackPowerDef); RelevantAttributesToCapture.Add(DS().ArmorDef); }
void UDamageExec::Execute_Implementation(const FGameplayEffectCustomExecutionParameters& P,
                                         FGameplayEffectCustomExecutionOutput& Out) const {
    const FGameplayEffectSpec& Spec = P.GetOwningSpec();
    FAggregatorEvaluateParameters EP;
    EP.SourceTags = Spec.CapturedSourceTags.GetAggregatedTags();
    EP.TargetTags = Spec.CapturedTargetTags.GetAggregatedTags();
    float AP = 0, Armor = 0;
    P.AttemptCalculateCapturedAttributeMagnitude(DS().AttackPowerDef, EP, AP);
    P.AttemptCalculateCapturedAttributeMagnitude(DS().ArmorDef, EP, Armor);
    float Base = Spec.GetSetByCallerMagnitude(TAG_Data_Damage, false, 0.f);
    float Dmg = FMath::Max(0.f, (Base + AP) * (100.f / (100.f + Armor)));
    Out.AddOutputModifier(FGameplayModifierEvaluatedData(UCombatSet::GetIncomingDamageAttribute(),
                          EGameplayModOp::Additive, Dmg));
}
```

## Meta attributes
Output to a transient `IncomingDamage` attribute; in the attribute set's `PostGameplayEffectExecute`,
consume it: subtract shields, then health, fire death events, reset IncomingDamage to 0. Keeps the
formula and the application of results separate.

## Snapshotting
Snapshot = capture value when the spec is created (source attack power at firing time for a
projectile). Non-snapshot = value at application time (target armour on hit).

## Gotchas
- Executions don't run client-side prediction; health bars update after server confirmation — show
  predicted hit feedback via cues instead.
- Forgetting to add capture definitions to `RelevantAttributesToCapture` returns 0 silently.
- SetByCaller missing logs an error unless `WarnIfNotFound` false and a default is given.

## Verify
- [ ] Unit/automation test applies the GE with known attributes and checks resulting health.
- [ ] `showdebug abilitysystem` shows expected attribute changes.
