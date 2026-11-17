---
id: creative-arts.game-design.systems-and-mechanics.crafting-system-design
name: crafting-system-design
category: creative-arts
field: game-design
product: systems-and-mechanics
tags: [game-design, crafting-system, recipes, game-economy, resource-economy, survival-games, recipe-discovery, material-sinks, progression]
level: practitioner
status: draft
description: "Design a crafting system: recipe structure, discovery, material sources and sinks, value of crafted vs found items, and UI that keeps crafting a decision, not a chore."
sources:
  - https://www.routledge.com/Game-Balance/Schreiber-Romero/p/book/9781498799577
  - https://www.gdcvault.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Crafting system design

**Goal:** crafting that gives players meaningful choices (what to make, what to spend
materials on) and acts as a controllable economic sink.

## Decide crafting's job first
| Job | Implication |
|---|---|
| Material sink for the economy | recipes consume more than they create; crafted items degrade or are consumed |
| Player expression / customisation | many recipe options, few dominant results |
| Progression path alternative to drops | crafted gear competes with found gear at equal effort |
| Survival pressure | basic needs crafted from scarce materials |
| Discovery | recipes hidden and found through experimentation |

## Recipe structure
- **Tiers:** raw -> refined -> component -> item. Each tier adds a decision only if a
  material has more than one use.
- **Material overlap:** each material should feed 2-4 recipes so allocating it is a
  choice. A material with one use is just a key.
- **Recipe count:** keep the active recipe list small enough to scan; hide or collapse
  obsolete ones.

## Value balancing
1. Price every material in time-to-gather.
2. Crafted item value should equal (materials time + crafting time) x a premium for the
   certainty of crafting vs random drops.
3. Compare with an equivalent found item; if crafted is always better or always worse,
   one system is dead.

## Discovery models
- Known recipes (list) - clear, low friction.
- Unlockable blueprints - progression lever.
- Experimentation (combine to discover) - discovery fun, but provide hints or a
  recipe journal; unguided combinatorics frustrate.

## UI rules
- Show missing materials and where to get them.
- "Craft max" and queueing for bulk crafting.
- Inventory pressure from materials is the top crafting complaint: give materials their
  own storage or stack sizes.

## Gotchas
- Crafting systems are often bolted on and ignored; if playtesters skip it, it has no
  job.
- Durability/repair as a sink annoys players unless repair is cheap and convenient.
- Randomised crafting results (quality rolls) compound with random drops; watch variance.

## Verify
- [ ] Crafting's job stated in one sentence.
- [ ] Each material used by 2+ recipes (or justified).
- [ ] Crafted vs found item value compared; both paths viable.
- [ ] Playtesters engage with crafting without prompting.
