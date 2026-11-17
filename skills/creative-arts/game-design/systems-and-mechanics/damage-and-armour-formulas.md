---
id: creative-arts.game-design.systems-and-mechanics.damage-and-armour-formulas
name: damage-and-armour-formulas
category: creative-arts
field: game-design
product: systems-and-mechanics
tags: [game-design, systems-and-mechanics, damage-formula, combat-design, armour, effective-hp, stat-scaling, spreadsheet-balancing]
level: practitioner
status: draft
description: "Choose and tune a damage/armour formula (subtractive, divisive, percentage) so stats scale sanely, with effective-HP checks and a spreadsheet sweep."
sources:
  - https://leagueoflegends.fandom.com/wiki/Armor
  - https://bulbapedia.bulbagarden.net/wiki/Damage
  - https://www.routledge.com/The-Art-of-Game-Design-A-Book-of-Lenses-Third-Edition/Schell/p/book/9781138632059
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Damage and armour formulas

**Goal:** a mitigation formula whose every stat point stays meaningful across the whole
progression range, with no zero-damage walls and no one-shot cliffs.

## The families
| Family | Formula | Behaviour | Watch for |
|---|---|---|---|
| Subtractive | `dmg = max(floor, atk - def)` | intuitive, big swings | def >= atk gives the floor every hit; small hits become useless |
| Divisive (diminishing) | `dmg = raw * K / (K + armour)` (League of Legends uses K=100) | never reaches zero; each armour point adds the same EHP | players read the falling "% reduction" as falling value and misjudge it |
| Percentage | `dmg = raw * (1 - min(cap, armour%))` | simple tooltips | stacking to the cap = immunity; hard-cap it (e.g. 75%) |
| Ratio | `dmg = raw * atk / def` (Pokemon-style, plus level and random terms) | scales cleanly when atk and def grow together | runaway when one side outgrows the other |

## Effective HP is the tuning lens
For the divisive form, `EHP = HP * (1 + armour / K)`. It is linear in armour: each point
is worth `HP / K` EHP no matter how much you already have. Compare items by EHP-per-gold
and DPS-per-gold, not by the displayed reduction %.

## Procedure
1. Fix the target **time-to-kill (TTK)** per encounter tier (e.g. trash 2-3 hits, elite
   8-12 s, boss 90-180 s).
2. Write expected attacker and defender stats per level in a sheet (level 1..cap).
3. Plug in each candidate formula; plot hits-to-kill per level for equal-level, +5 and -5 pairs.
4. Reject formulas where any curve goes to 1 hit or to the damage floor inside the normal range.
5. Add penetration (flat and %) only after the base curve is right; document the order
   of application (e.g. % pen before flat pen).
6. Put randomness last (`* uniform(0.9, 1.1)`), and crits as a separate multiplier.

## Gotchas
- Subtractive systems need a floor (1, or 10% of raw) or high-armour enemies become unkillable.
- Multiple mitigation layers multiply: 30% then 30% resistance is 51% total, not 60%. Say so in tooltips.
- Damage over time and multi-hit attacks are punished hardest by subtractive armour.
- Integer rounding at low values distorts results: compute in floats, round once at display.

## Verify
- [ ] Hits-to-kill plotted per level for at least three level gaps.
- [ ] No curve hits the floor or a 1-hit kill inside the intended band.
- [ ] Item value compared in EHP/DPS per cost.
- [ ] Order of operations written in the combat spec.
