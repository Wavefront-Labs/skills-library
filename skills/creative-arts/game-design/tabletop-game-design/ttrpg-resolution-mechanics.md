---
id: creative-arts.game-design.tabletop-game-design.ttrpg-resolution-mechanics
name: ttrpg-resolution-mechanics
category: creative-arts
field: game-design
product: tabletop-game-design
tags: [game-design, tabletop-game-design, ttrpg-design, resolution-mechanic, dice-pool, d20-system, pbta, roll-under, success-with-cost, partial-success]
level: advanced
status: draft
description: "Choose and tune a tabletop RPG resolution mechanic: d20 vs target, roll-under, dice pools, 2d6 partial successes; success odds, modifier scale and how failure moves the story."
sources:
  - https://www.dndbeyond.com/srd
  - http://apocalypse-world.com/
  - https://anydice.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# TTRPG resolution mechanics

**Goal:** a core roll that produces the right success rates, makes character
competence matter, and gives the GM interesting outcomes on both success and failure.

## Common families
| Family | Example | Character |
|---|---|---|
| d20 + modifier vs DC | D&D 5e (SRD 5.1/5.2) | flat odds; each +1 = 5%; binary pass/fail |
| Roll-under skill | percentile systems (d100 <= skill) | intuitive "skill % = chance" |
| Dice pool, count successes | many World of Darkness / Shadowrun-style systems | bell-ish; more dice = more reliable |
| 2d6 + stat with bands | Powered by the Apocalypse (Apocalypse World): 10+ full success, 7-9 success with cost, 6- GM makes a move | built-in partial success |
| Fortune-in-the-middle | roll first, narrate after | improv-friendly |

## Procedure
1. **Decide what a roll means:** task success, or story outcome ("do you get what you
   want?").
2. **Compute odds** at typical modifiers (AnyDice or enumeration; see
   `creative-arts.game-design.systems-and-mechanics.dice-probability-distributions`).
   Example 2d6 bands: 10+ = 16.7%, 7-9 = 41.7%, 6- = 41.7% with +0.
3. **Set the modifier scale** so competence shows: how much better is an expert than a
   novice in success %? Bounded accuracy (small modifiers) keeps low-level threats
   relevant; large modifiers make experts near-certain.
4. **Design failure** so it moves play: complications, costs, partial success, "fail
   forward" - never "nothing happens".
5. **Count rolls per session:** frequent rolls need quick resolution; rare rolls can be
   more elaborate.
6. **Playtest pacing:** time per roll including adding modifiers.

## Gotchas
- Flat d20 makes experts fail often (5% natural 1 rules); decide if that's desirable.
- Large dice pools slow the table (counting); cap pool size.
- Partial success bands require GM guidance and examples; write them in the GM section.

## Verify
- [ ] Odds table for typical stats and difficulties.
- [ ] Failure and partial-success outcomes defined with examples.
- [ ] Average time per roll measured at the table.
