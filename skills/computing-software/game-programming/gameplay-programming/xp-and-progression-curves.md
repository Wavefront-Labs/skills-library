---
id: computing-software.game-programming.gameplay-programming.xp-and-progression-curves
name: xp-and-progression-curves
category: computing-software
field: game-programming
product: gameplay-programming
tags: [gameplay-programming, progression-system, xp-curve, leveling, experience-points, stat-scaling, game-balance, game-programming]
level: practitioner
status: gated
description: "Implement XP and level progression: XP-to-level formulas (linear, polynomial, exponential), cumulative tables, multi-level-up handling, stat scaling and overflow/save pitfalls."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/data-driven-gameplay-elements-in-unreal-engine", "https://bulbapedia.bulbagarden.net/wiki/Experience"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# XP and progression curves

**Goal:** a level curve designers can tune, code that never mis-levels the player, and stats that
scale predictably.

## Pick a curve (XP needed to go from level L to L+1)
| Shape | Formula | Feel |
|---|---|---|
| Linear | `a * L` | each level slightly longer; cumulative is quadratic |
| Polynomial | `a * L^p` (p ~ 1.5-2.5) | most RPGs; Pokemon "medium fast" cumulative is `L^3` (gated: unconfirmed, source is paywalled or blocked) |
| Exponential | `a * r^L` (r ~ 1.1-1.2) | steep late game; use with exponential rewards |
Match the curve to reward growth: if enemy XP grows with level at the same rate, time-per-level stays
flat. Tune the **time per level** target (e.g. 20 min at L10, 2 h at L50), then derive `a`.

## Store cumulative, compute in a table
Precompute `cumXP[L]` (total XP required to reach L) once from the formula or a designer-edited
table, round to "nice" numbers, and store **total XP** in the save, not "XP into current level".
```csharp
public int LevelForXp(long totalXp) {
    int i = Array.BinarySearch(cumXp, totalXp);      // cumXp[0] = -1 sentinel, cumXp[1] = 0, ascending
    return i >= 0 ? i : ~i - 1;
}
public void AddXp(long amount) {
    int before = Level;
    TotalXp = Math.Min(TotalXp + amount, cumXp[MaxLevel]);  // cap: no overflow past max
    for (int l = before + 1; l <= Level; l++) OnLevelUp(l); // grants every skipped level's rewards
}
```
The C# was not compiled here. A Python port of `LevelForXp` using `bisect_left` on `cumXp = [-1, 0, 8, 27, ...]` (cube table) returned level 1 for 0 XP, 2 for 8, 1 for 7, 3 for 27, 2 for 26 and the max level for 10^9 XP, matching the unit tests listed under Verify. The Unreal Curve Table / `FScalableFloat` pointer was not checked against the Unreal docs (gated: unconfirmed, source is paywalled or blocked).
- Handle **multiple level-ups** from one big reward: loop and fire per level (unlocks, skill points).
- Use `long`/64-bit for idle/incremental games; or a mantissa+exponent "big number" type.
- Progress bar: `(TotalXp - cumXp[L]) / (cumXp[L+1] - cumXp[L])`.

## Stat scaling
- Stats from a curve table keyed by level (Unreal Curve Tables / `FScalableFloat`, Unity
  AnimationCurve or ScriptableObject table), not hard-coded formulas, so balance changes are data.
- Separate base-by-level from modifiers (gear, buffs) to keep the formula auditable.
- Watch the ratio between player damage growth and enemy HP growth; plot both curves before shipping.

## Patch safety
Saves store total XP, so changing the table re-derives level on load. Decide policy if a patch would
de-level players (clamp to their saved level, or grant XP to match).

## Verify
- [ ] Unit test: 0 XP -> level 1; exactly `cumXp[L]` -> level L; one XP less -> L-1.
- [ ] A reward spanning 3 levels fires 3 level-up events.
- [ ] Max level caps XP; the bar shows full; no exception at max.
- [ ] Spreadsheet plot of time-to-level matches playtest telemetry within tolerance.
