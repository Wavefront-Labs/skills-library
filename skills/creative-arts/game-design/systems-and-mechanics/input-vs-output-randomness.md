---
id: creative-arts.game-design.systems-and-mechanics.input-vs-output-randomness
name: input-vs-output-randomness
category: creative-arts
field: game-design
product: systems-and-mechanics
tags: [game-design, input-randomness, output-randomness, randomness-design, probability-design, luck, skill-vs-chance, mitigation, characteristics-of-games]
level: practitioner
status: draft
description: "Decide where randomness enters a game: input randomness (before decisions) vs output randomness (after), and add mitigation so luck creates decisions instead of erasing them."
sources:
  - https://mitpress.mit.edu/9780262017138/characteristics-of-games/
  - https://www.routledge.com/The-Art-of-Game-Design-A-Book-of-Lenses-Third-Edition/Schell/p/book/9781138632059
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Input vs output randomness

**Goal:** randomness that makes players plan and adapt, not randomness that decides the
game for them.

The distinction (popularised in Elias, Garfield and Gutschera, *Characteristics of
Games*, and widely used in tabletop design):
- **Input randomness:** random state is revealed *before* the player decides (dealt
  hand, map generation, drafting pool, dice rolled before assigning them). Players plan
  around it.
- **Output randomness:** random resolution *after* the decision (attack roll, crit
  chance, loot drop). Players commit and then learn the result.

## Effects
| | Input | Output |
|---|---|---|
| Skill expression | high: adapt to what you got | lower: right choice can still lose |
| Drama | lower per action | high: the tense roll |
| Perceived fairness | usually high | "I got robbed" moments |
| Replayability | high (varied situations) | moderate |

## Mitigation tools for output randomness
- Rerolls or luck tokens (limited resource to manage luck).
- More rolls, smaller stakes (law of large numbers smooths outcomes).
- Bell-curve dice instead of flat (see `creative-arts.game-design.systems-and-mechanics.dice-probability-distributions`).
- Partial success bands instead of pass/fail.
- Pity / bad-luck protection in digital games.
- Show odds before committing (XCOM-style hit %) so risk is a decision.

## Procedure
1. List every random element and tag it input or output.
2. For each output element, ask: is the drama worth the lost control? If the outcome
   decides the game, convert to input or add mitigation.
3. Check **skill vs chance** at the whole-game level (Schell's balance type): how often
   does the stronger player win? Measure in playtests or simulation.
4. Make sure the random elements are **visible and understandable**; hidden output
   randomness feels like the game cheating.

## Gotchas
- Pure input randomness can create a solved "best play" for each deal; add hidden info
  or opponent interaction.
- Children's games and party games legitimately want lots of output randomness so
  anyone can win.
- In competitive digital games, output randomness (random crits) is often removed after
  community pushback; know your audience.

## Verify
- [ ] Every random element tagged input/output.
- [ ] Each high-stakes output element has mitigation or a stated reason.
- [ ] Skilled-player win rate measured and within target.
