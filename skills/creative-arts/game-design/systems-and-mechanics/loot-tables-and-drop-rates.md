---
id: creative-arts.game-design.systems-and-mechanics.loot-tables-and-drop-rates
name: loot-tables-and-drop-rates
category: creative-arts
field: game-design
product: systems-and-mechanics
tags: [game-design, loot-table, drop-rates, reward-design, weighted-random, rarity-tiers, nested-loot-tables, expected-farm-time, arpg, mmo]
level: practitioner
status: draft
description: "Build weighted and nested loot tables, set drop rates from target farm time, compute expected attempts and worst-case droughts, and keep rarity tiers meaningful."
sources:
  - https://www.routledge.com/Game-Balance/Schreiber-Romero/p/book/9781498799577
  - https://en.wikipedia.org/wiki/Geometric_distribution
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Loot tables and drop rates

**Goal:** drop rates chosen from how long you want players to chase an item, with the
variance understood, implemented as maintainable tables.

## Table structure
- **Weighted table:** each entry has a weight; P(entry) = weight / sum(weights). Easier
  to edit than percentages (adding an entry does not require renormalising by hand).
- **Nested tables:** roll a rarity tier first, then an item within the tier. Lets you
  tune "how often is a drop legendary" separately from "which legendary".
- **Guaranteed + random:** fixed drops (quest item, currency) plus N rolls on a table.
- **Empty entries:** "nothing" with a weight is how you set the overall drop chance.
```
monster_drop: rolls=1
  nothing  weight 70
  common   weight 22  -> table common_items
  rare     weight  7  -> table rare_items
  epic     weight  1  -> table epic_items
```
P(epic tier) = 1/100 per kill.

## Set rates from target time
1. Decide **target time to obtain** for the median player (e.g. epic weapon ~3 hours of
   farming).
2. Measure or estimate **attempts per hour** (kills, chests, runs).
3. Rate p = 1 / (target hours x attempts per hour). The number of attempts until first
   drop is geometric: mean 1/p, median about 0.69/p.
4. Check the **unlucky tail**: P(no drop after n attempts) = (1-p)^n. With p = 1/100,
   after 300 attempts 4.9% of players still have nothing; 1 in 20 players is a lot of
   angry forum posts. Add bad-luck protection (see
   `creative-arts.game-design.systems-and-mechanics.pseudo-random-distribution-and-bad-luck-protection`).

## Python check
```python
p = 1 / 100
assert abs((1 - p) ** 300 - 0.049) < 0.001
```

## Rarity tiers
- Each tier should be **distinguishable in use**, not only in colour: rarer = new
  effects or build-defining properties, not +3% stats.
- Communicate rarity consistently (colour, sound, beam). Use colour plus shape/label for
  colour-blind players.
- Duplicate protection (no repeats until the set is complete) for collection loot.

## Gotchas
- Group play multiplies rolls; decide whether drops are personal or shared and rebalance.
- Loot that is mostly vendor trash creates inventory chores; auto-salvage options help.
- Paid random loot (loot boxes) triggers odds-disclosure and regional legal rules.

## Verify
- [ ] Every rare drop has a target time and computed p.
- [ ] Tail probability at 3x the median attempts calculated and acceptable (or protected).
- [ ] Simulated drops match intended tier frequencies.
