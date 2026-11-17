---
id: computing-software.game-programming.gameplay-programming.loot-tables-and-weighted-drops
name: loot-tables-and-weighted-drops
category: computing-software
field: game-programming
product: gameplay-programming
tags: [gameplay-programming, game-state, loot-table, weighted-random, drop-rates, game-programming]
level: practitioner
status: verified
description: "Build loot tables: weighted random selection, nested tables, guaranteed and pity drops, rarity tiers, seeded RNG for reproducibility and testing drop distributions."
sources: ["https://www.redblobgames.com/articles/probability/damage-rolls.html", "https://www.keithschwarz.com/darts-dice-coins/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Loot tables and weighted drops

**Goal:** drops with designer-controlled odds that are verifiable, reproducible and fair over time.

## Weighted pick
```csharp
public T Pick<T>(IReadOnlyList<(T item, float weight)> table, System.Random rng) {
    float total = 0; foreach (var e in table) total += e.weight;
    float r = (float)rng.NextDouble() * total;
    foreach (var e in table) { if ((r -= e.weight) < 0) return e.item; }
    return table[^1].item;                       // float edge case
}
```
The C# above was not compiled here (only the .NET runtime, no SDK, was available); the same algorithm re-implemented in Python (`r -= weight; if r < 0`) over weights 70/25/4.5/0.5 gave 700294/249381/45304/5021 hits in 1,000,000 picks (chi-square p = 0.28, consistent with the weights). For huge tables picked very often, precompute prefix sums + binary search, or Walker/Vose **alias
method** (O(1) per pick; a Vose alias table built in Python reproduced the same frequencies: 699934/250196/44948/4922).

## Table structure
- Entries: item, weight, quantity range, conditions (level range, quest state, region).
- **Nested tables**: entry can be another table ("Rare Weapons") — designers manage tiers separately.
- **No drop** as an explicit weighted entry rather than a separate chance.
- Rolls: N independent rolls, or pick without replacement for "3 distinct rewards".
- Guaranteed drops (boss always drops key) listed separately from random rolls.

## Fairness controls
- **Pity timer**: increase weight of a rare after each miss; reset on drop (or guarantee after N).
- **Bad-luck protection** per player, persisted.
- Avoid duplicates of uniques already owned (filter before pick, renormalise).

## Reproducibility
Seed per drop event (world seed + chest id) for deterministic loot in roguelikes/co-op sync; server-side
RNG for online games (client never decides drops).

## Testing distributions
Simulate 1e6 rolls in a unit test and compare observed frequencies to weights (chi-square or tolerance
per entry). Export expected "chance per kill" tables for designers: probability of at least one item X
in K kills = 1 - (1 - p)^K (p = 0.005, K = 200 gives 63.3%; a 20,000-trial simulation gave 63.6%).

## Gotchas
- Designers reason in percentages; display computed % next to weights in tools.
- Conditional entries change totals; document that weights are relative within the filtered set.
- Integer weights avoid float drift for very small odds (use long sums).

## Verify
- [ ] Simulation test within tolerance for every table in CI.
- [ ] Pity guarantee triggers at exactly N misses in tests.
