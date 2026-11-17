---
id: computing-software.game-programming.unreal-engine.smart-objects
name: smart-objects
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, ue5, unreal-ai, smart-objects, smart-object-definition, slots, claim-use-release, gameplay-behaviors, ambient-ai, game-programming]
level: advanced
status: draft
description: "Make world objects advertise interactions with Unreal Smart Objects: definitions and slots, finding/claiming/using/releasing slots from AI, gameplay behaviors and tag filtering."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/smart-objects-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/smart-objects-in-unreal-engine---quick-start", "https://dev.epicgames.com/documentation/en-us/unreal-engine/smart-objects-in-unreal-engine---overview"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Smart Objects

**Goal:** benches, vending machines, workstations and doors that tell AI how to use them, so ambient
behaviour scales by placing objects rather than scripting each NPC (the idea from The Sims, built into
UE5).

## Pieces
- Plugins: **SmartObjects**, **GameplayBehaviors** (and GameplayBehaviorSmartObjects for the bridge).
- **Smart Object Definition** (data asset): one or more **slots** (offset/rotation relative to the
  object), activity tags, user/object tag filters, and per-slot behavior definitions (e.g. a
  `GameplayBehaviorSmartObjectBehaviorDefinition` pointing to a GameplayBehavior that plays a montage).
- **SmartObjectComponent** on the actor references the definition and registers it with the
  `USmartObjectSubsystem` (world subsystem).

## AI flow: find -> claim -> move -> use -> release
```cpp
USmartObjectSubsystem* SO = GetWorld()->GetSubsystem<USmartObjectSubsystem>();
FSmartObjectRequest Request(FBox(PawnLoc - FVector(2000), PawnLoc + FVector(2000)),
                            FSmartObjectRequestFilter());
Request.Filter.ActivityRequirements = FGameplayTagQuery::MakeQuery_MatchTag(TAG_Activity_Sit);
TArray<FSmartObjectRequestResult> Results;
SO->FindSmartObjects(Request, Results);
if (Results.Num() > 0)
{
    FSmartObjectClaimHandle Claim = SO->MarkSlotAsClaimed(Results[0].SlotHandle, ESmartObjectClaimPriority::Normal);
    // move to SO->GetSlotTransform(Claim) ... then:
    const UGameplayBehaviorSmartObjectBehaviorDefinition* Def =
        SO->MarkSlotAsOccupied<UGameplayBehaviorSmartObjectBehaviorDefinition>(Claim);
    // run Def->GameplayBehaviorConfig; when finished:
    SO->MarkSlotAsFree(Claim);
}
```
(API names have changed across 5.x versions, e.g. `Claim`/`Use`/`Release` older names; check your
engine version.) Claiming reserves the slot so two NPCs do not walk to the same chair.

Higher-level use without C++: Behavior Tree tasks **Find and Use Smart Object** / StateTree tasks and
the `AITask_UseGameplayBehaviorSmartObject` handle find/claim/move/use/release.

## Filtering and state
- Activity tags on the definition/slot describe what it offers (`Activity.Sit`, `Activity.Eat`).
- User tag filter: who may use it (only `NPC.Worker`).
- Runtime tags on instances/slots to disable (broken machine), plus enable/disable per slot.

## Gotchas
- Always release claims on abort (AI killed, interrupted), or slots stay claimed forever. Handle
  `OnSlotInvalidated`/aborts in your task.
- Smart objects must be registered (component active, in a loaded level/partition cell) to be found.
- Debug: Gameplay Debugger Smart Objects category; `ai.debug.so` style cvars vary by version.

## Verify
- [ ] Two NPCs never occupy the same slot.
- [ ] Killing an NPC mid-use frees its slot.
- [ ] Placing a new bench in the level makes NPCs use it with no script changes.
