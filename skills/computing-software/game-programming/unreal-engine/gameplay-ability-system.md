---
id: computing-software.game-programming.unreal-engine.gameplay-ability-system
name: gameplay-ability-system
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, ue5, gas, gameplay-ability-system, attribute-set, gameplay-effect, gameplay-tag, ability-system-component, gameplay-cue, gameplay-attribute, predicted-ability, abilitytask, asc, mmc, game-programming]
level: advanced
status: draft
description: "Structure abilities, stats, and status effects in Unreal with GAS: AttributeSets, GameplayEffects, tags, and where its replication/prediction actually helps."
sources: ["https://github.com/tranek/GASDocumentation", "https://dev.epicgames.com/documentation/en-us/unreal-engine/gameplay-ability-system-for-unreal-engine"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Unreal's Gameplay Ability System (GAS)

**Goal:** use GAS for what it's actually for — networked abilities, stats, and
status effects with built-in prediction — without drowning in its plumbing for
a game that doesn't need any of it.

## When to reach for GAS at all
GAS is Epic's framework (free, in-engine, used by Fortnite and Paragon) for
anything with: abilities that cost resources, cooldowns, stacking buffs/debuffs,
and that must work correctly in multiplayer with client prediction. If your game
is single-player or has 2-3 simple abilities with no stat system, GAS's
boilerplate (an AbilitySystemComponent, AttributeSets, GameplayEffects just to
deal 10 damage) is not worth it — a plain interface + replicated RPC is less
code. Adopt it when you have ≥ ~10 abilities, status effects that stack/interact,
or need prediction out of the box.

## The four pieces
1. **AbilitySystemComponent (ASC)** — owns everything else; lives on the Pawn or
   (more robust for respawning characters) the PlayerState, since PlayerState
   survives Pawn destruction and keeps ability cooldowns/state across death.
2. **AttributeSet** — a `UObject` holding `FGameplayAttributeData` (Health,
   Mana...) with `PreAttributeChange`/`PostGameplayEffectExecute` hooks for
   clamping (health never above max) and reacting (health hits 0 → die).
   Attributes are **not** directly set by gameplay code — they're only ever
   changed through GameplayEffects, which is what makes them replicate and
   predict correctly.
3. **GameplayEffect (GE)** — a data asset describing a change: instant
   (-10 health), duration-based (slow for 3s), or infinite (passive aura). Effects
   can stack (`Aggregate` vs `Stack` by caster/target), and use a
   **ModifierMagnitudeCalculation (MMC)** for anything derived (damage scaled by
   the caster's attack stat, not a flat number).
4. **GameplayAbility** — the activatable logic (a cast, a dash), using
   `AbilityTask`s (`WaitTargetData`, `PlayMontageAndWait`) for latent, cancellable
   steps across frames, gated by **GameplayTags** (`Ability.Cooldown.Dash`,
   `State.Stunned`) that block or cancel other abilities declaratively via the
   ability's Tags (BlockAbilitiesWithTag, CancelAbilitiesWithTag) instead of if-
   checks scattered across every ability.

## Prediction and the thing that confuses everyone
Client-predicted abilities run locally immediately (responsive input) and are
corrected if the server disagrees — but **prediction only applies to GAS's own
plumbing** (attribute changes via GameplayEffects, ability activation/cooldown).
Anything you do manually inside an ability that isn't routed through a
GameplayEffect (a raw `Health -= 10` instead of applying a GE, a direct
`SpawnActor` for a projectile) is **not** predicted or reconciled — it either
runs only on the server (feels laggy) or runs unpredicted on the client and
desyncs. The rule: every stat change goes through a GameplayEffect, every spawn
that needs to be predicted goes through `UAbilitySystemBlueprintLibrary`'s
prediction-aware spawn helpers or is purely cosmetic (a particle that doesn't
need to match server state).

## GameplayCues for presentation
Don't put VFX/SFX/camera shake inside the ability or effect logic — fire a
**GameplayCue** tag (`GameplayCue.Weapon.Fire`) instead. Cues run locally on
every client (including simulated proxies) independent of replication timing
for the gameplay effect itself, which is what keeps hit reactions feeling instant
even under latency, and keeps presentation separable from designers tuning the
underlying numbers.

## Verify
- [ ] ASC lives on PlayerState (or justified reason it's on the Pawn) for anything
      that must survive respawn.
- [ ] No gameplay code sets an Attribute directly outside a GameplayEffect.
- [ ] Ability-blocking/cancelling uses GameplayTags, not manual boolean flags
      checked in every ability's `CanActivateAbility`.
- [ ] Tested with artificial latency (`Net PktLag=150`) — predicted abilities
      still feel instant locally and correct themselves without visible snapping.
