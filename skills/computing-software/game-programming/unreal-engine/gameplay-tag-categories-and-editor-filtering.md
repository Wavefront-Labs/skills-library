---
id: computing-software.game-programming.unreal-engine.gameplay-tag-categories-and-editor-filtering
name: gameplay-tag-categories-and-editor-filtering
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, gameplay-tag-categories, gameplay-tags, meta-categories, editor-ux, game-programming]
level: practitioner
status: draft
description: "Restrict Unreal gameplay tag pickers with Categories meta on UPROPERTY and UFUNCTION params, category remapping, and restricted tag sources so designers pick valid tags."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/using-gameplay-tags-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-uproperties", "https://docs.unrealengine.com/5.3/en-US/API/Runtime/GameplayTags/UGameplayTagsSettings/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Gameplay tag categories and editor filtering

**Goal:** a "damage type" field only offers `Damage.*` tags.

## Categories meta
```cpp
UPROPERTY(EditAnywhere, meta = (Categories = "Damage"))
FGameplayTag DamageType;

UPROPERTY(EditAnywhere, meta = (Categories = "Status,Ability.State"))
FGameplayTagContainer BlockedBy;

UFUNCTION(BlueprintCallable, meta = (GameplayTagFilter = "Event"))
void SendEvent(FGameplayTag EventTag);
```
- `Categories` filters the picker to the listed roots (comma separated).
- On UFUNCTION parameters use `meta=(GameplayTagFilter="...")` or per-parameter
  `UPARAM(meta=(Categories="Event"))`.
- Works on `FGameplayTagQuery` too.

## Category remapping
Project Settings > GameplayTags > **Category Remapping**: map a base category name used in code (for
example `AbilityTagCategory`) to the project's real roots, so plugin code can declare
`meta=(Categories="AbilityTagCategory")` and each project chooses which tags appear.

## Restricted tag sources
Restricted Config Files (`Config/Tags/` restricted ini with owners) stop arbitrary tag creation under
critical roots; editing them warns or requires permission. Use for engine-level tags designers should
not add to.

## Struct-wide defaults
A `USTRUCT` wrapper with a filtered tag field gives reuse:
```cpp
USTRUCT(BlueprintType) struct FDamageTag { GENERATED_BODY()
    UPROPERTY(EditAnywhere, meta=(Categories="Damage")) FGameplayTag Tag; };
```

## Gotchas
- Categories filter the editor only; code must still validate (`Tag.MatchesTag(DamageRoot)`).
- Misspelled categories show an empty picker; native tag constants for roots avoid typos.

## Verify
- [ ] Every designer-facing tag field shows only its relevant subtree.
