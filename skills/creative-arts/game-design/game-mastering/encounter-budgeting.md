---
id: creative-arts.game-design.game-mastering.encounter-budgeting
name: encounter-budgeting
category: creative-arts
field: game-design
product: game-mastering
tags: [game-design, game-mastering, encounter-budget, challenge-rating, running-combat, dnd-5e, xp-thresholds, encounter-multiplier, combat-encounters, ttrpg]
level: practitioner
status: draft
description: "Budget D&D-style combat encounters with XP thresholds and challenge rating, account for action economy, and adjust live when the fight is too easy or too hard."
sources:
  - https://www.dndbeyond.com/srd
  - https://www.dndbeyond.com/sources/dnd/free-rules
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Encounter budgeting

**Goal:** combat encounters whose difficulty you choose on purpose, with a fallback
plan when your estimate is wrong.

## D&D 5e (2014 DMG) method
1. **Party threshold:** sum each character's XP threshold for the target difficulty.
   Per-character thresholds at level 1: Easy 25, Medium 50, Hard 75, Deadly 100; at
   level 5: 250 / 500 / 750 / 1,100 (full table in the DMG, ch3).
2. **Monster XP:** sum XP of all monsters (from their CR).
3. **Multiply by the encounter multiplier** for number of monsters: 1 = x1, 2 = x1.5,
   3-6 = x2, 7-10 = x2.5, 11-14 = x3, 15+ = x4 (adjusted for party size in the DMG).
4. Compare the adjusted total to the thresholds.
The 2024 revision of the rules replaced this with a simpler per-character XP budget by
difficulty (Low / Moderate / High) without the monster-count multiplier; check which
edition's tables you use.

## Beyond the numbers
- **Action economy:** many weak enemies vs one strong enemy changes everything; a solo
  boss gets swarmed by a full party unless it has extra actions (legendary/lair actions).
- **Terrain and objectives:** cover, hazards, and goals other than "kill everyone" shift
  difficulty more than stats.
- **Resource attrition:** difficulty is cumulative across an adventuring day; the 2014
  DMG gives an adventuring-day XP budget.
- **Party composition and magic items** skew CR estimates.

## Live adjustment (without breaking trust)
| Too easy | Too hard |
|---|---|
| reinforcements arrive (foreshadowed) | enemies flee at morale break |
| add an objective/timer | enemies take captives instead of killing |
| boss uses a held-back ability | environmental escape route |
Decide in advance whether you adjust hidden numbers (HP) at all; many GMs prefer
fiction-based adjustments.

## Verify
- [ ] Encounter difficulty computed with the edition's method.
- [ ] Action economy considered (count enemy actions vs party actions per round).
- [ ] Too-easy and too-hard adjustments prepared.
