---
id: creative-arts.game-design.level-design.metroidvania-ability-gating
name: metroidvania-ability-gating
category: creative-arts
field: game-design
product: level-design
tags: [game-design, level-design, ability-gating, metroidvania, lock-and-key, backtracking, interconnected-world, sequence-breaking, world-map]
level: advanced
status: draft
description: "Design ability-gated interconnected worlds: map locks to abilities, show locks before keys, plan the unlock order graph, handle sequence breaks, and keep backtracking rewarding."
sources:
  - https://grumpygamer.com/puzzle_dependency_charts
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Metroidvania ability gating

**Goal:** an interconnected world where new abilities open previously seen but
unreachable areas, so the player's growing power is felt as growing access.

Rogers' Level Up! discusses the Metroidvania structure; the logic is the same as a
puzzle dependency chart (Ron Gilbert): every lock depends on a key.

## Procedure
1. **List abilities** (double jump, dash, swim, wall climb, break blocks) and the
   **lock** each opens (high ledge, long gap, water, vertical shaft, cracked wall).
   One clear visual lock type per ability.
2. **Draw the dependency graph:** areas as nodes, edges labelled with required
   abilities. Check it is solvable from the start state and has the intended order.
3. **Show locks before keys:** the player should encounter each lock (and remember it)
   before getting the ability. The "I can reach that now" moment is the payoff.
4. **Place rewards behind old locks** (health upgrades, lore, shortcuts) so
   backtracking pays.
5. **Reduce backtracking cost:** fast travel, shortcuts that open on the return,
   map markers for seen-but-locked spots.
6. **Sequence breaking:** decide policy. Many players love finding skips; ensure skips
   cannot soft-lock the game (no state where progress is impossible).
7. **Map UI:** show explored areas, doors and lock types; it is the player's planning
   tool.

## Gotchas
- Abilities that only open doors (keys with extra steps) feel flat; each should also
  change combat or movement.
- Too many lock types blur together; keep them visually distinct.
- Soft-locks from sequence breaks (one-way drops without the ability to climb back) are
  severe bugs; test with every ability subset.

## Verify
- [ ] Ability-to-lock table with distinct visuals.
- [ ] Dependency graph solvable; no soft-lock states with any reachable ability set.
- [ ] Each lock is seen before its key.
- [ ] Rewards placed behind old locks; fast travel or shortcuts reduce retrace time.
