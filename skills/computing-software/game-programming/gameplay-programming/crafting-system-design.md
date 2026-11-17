---
id: computing-software.game-programming.gameplay-programming.crafting-system-design
name: crafting-system-design
category: computing-software
field: game-programming
product: gameplay-programming
tags: [gameplay-programming, crafting-system, recipes, inventory, game-programming]
level: practitioner
status: draft
description: "Build a data-driven crafting system: recipe definitions, ingredient matching with tags, atomic inventory transactions, discovery and crafting queues."
sources: ["https://gameprogrammingpatterns.com/type-object.html", "https://minecraft.wiki/w/Recipe"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Crafting systems

**Goal:** recipes defined by designers in data, with crafting that never duplicates or loses items.

## Recipe data
```yaml
- id: iron_sword
  station: anvil            # optional context requirement
  inputs:  [{item: iron_ingot, count: 3}, {tag: wood_any, count: 1}]
  outputs: [{item: iron_sword, count: 1}]
  time: 4.0
  unlock: recipe_book_iron
```
Tags (any item tagged `wood_any`) keep recipe counts down. Minecraft's data-pack recipe JSON is a
good model: shaped (grid pattern), shapeless, and smelting types.

## Matching
- Shapeless: build a multiset of available items, greedily satisfy specific-item inputs first, then
  tag inputs (otherwise a tag can consume the only item a specific input needed).
- Shaped grids: normalise the pattern (trim empty rows/cols), try mirrored variants if allowed.
- Index recipes by output and by each input for "what can I make" UI; avoid scanning every recipe
  per frame.

## Atomic transaction
```text
validate(all inputs present) -> reserve -> remove inputs -> add outputs -> commit
on failure (inventory full): roll back removal
```
Check output space before removing inputs. In multiplayer, run the transaction on the server only;
the client sends "craft recipe X", never "remove these items".

## Queues and timers
Store queued crafts with start time, not a ticking counter, so offline progress is
`elapsed = now - start`. Cap with max queue length.

## Pitfalls
- Duplicate exploits from crafting while an inventory move is in flight; lock or sequence inventory ops.
- Floating recipe balance: keep a script computing raw-resource cost per item to catch loops
  (A makes B makes more A).

## Verify
- Property test: random inventories and recipes, total item value conserved per recipe definition.
