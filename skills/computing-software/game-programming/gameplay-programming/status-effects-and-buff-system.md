---
id: computing-software.game-programming.gameplay-programming.status-effects-and-buff-system
name: status-effects-and-buff-system
category: computing-software
field: game-programming
product: gameplay-programming
tags: [gameplay-programming, hitbox, combat-timing, status-effects, buff-system, debuffs, stacking-rules, damage-over-time, stat-modifiers, game-programming]
level: practitioner
status: draft
description: "Build buffs and status effects: effect definitions, durations and ticks, stacking rules (refresh, stack, independent), stat modifier aggregation order, immunity and UI exposure."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/gameplay-effects-for-the-gameplay-ability-system-in-unreal-engine", "https://gameprogrammingpatterns.com/type-object.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Status effects and buff system

**Goal:** poison, burning, slow, haste, shields and stat buffs implemented by data, combining
predictably, with no lingering effects after they expire.

## Definition vs instance
```
EffectDefinition (data asset)
  id, icon, tags (Debuff, Poison, Movement)
  duration (or infinite), tickInterval
  modifiers: [ {stat: MoveSpeed, op: Multiply, value: 0.7} ]
  onTick: damage 5 Poison
  stacking: Refresh | StackIntensity(max 5) | StackDuration | Independent | None
  immunityTags / cancelledByTags
EffectInstance
  def, source, remaining, nextTick, stacks
```

## Stacking rules (decide per effect)
| Rule | Behaviour |
|---|---|
| Refresh | Reapplying resets duration; one instance. |
| Stack intensity | Stacks increase magnitude up to max; duration refresh or per-stack timers. |
| Stack duration | Adds time to remaining duration. |
| Independent | Each application is its own instance (multiple poisons from different sources). |
| Per-source | Unique per (effect, source): two players can each apply their own bleed. |

## Stat aggregation
Recompute derived stats from base + all active modifiers whenever effects change (dirty flag), never
by applying and un-applying deltas (which drifts when effects overlap). Fixed order:
```
value = (base + sum(Add)) * (1 + sum(AddPercent)) * product(Multiply)
then apply Override (highest priority) and clamp
```
Document the order; designers need it to predict results. GAS uses a similar
Add -> Multiply -> Divide -> Override aggregation.

## Ticking
A manager per entity updates remaining durations and ticks (DoT damage routed through the damage
pipeline). Use game time (pauses stop effects). For long durations at scale, store absolute end
times and check lazily instead of per-frame timers.

## Interactions
- Immunity tags: an entity with `Immune.Poison` rejects effects tagged Poison.
- Cleanses remove effects by tag; some effects cancel others (Wet removes Burning).
- Crowd control diminishing returns: track recent CC durations to shorten repeats.

## UI and save
Expose active effects (icon, stacks, remaining time) via events for the HUD. Save instances with
remaining time and stacks; re-resolve definitions by id on load.

## Verify
- [ ] Two overlapping slows produce the documented result and full speed returns exactly after both expire.
- [ ] Stacking rules per effect match the design table (automated tests).
- [ ] No effect remains after its duration (stat values equal base values after all expire).
