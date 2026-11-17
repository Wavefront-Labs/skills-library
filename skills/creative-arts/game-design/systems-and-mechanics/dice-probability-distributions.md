---
id: creative-arts.game-design.systems-and-mechanics.dice-probability-distributions
name: dice-probability-distributions
category: creative-arts
field: game-design
product: systems-and-mechanics
tags: [game-design, dice-probability, anydice, probability-design, randomness-design, 2d6, 3d6, d20, advantage, bell-curve, dice-pool, tabletop]
level: practitioner
status: draft
description: "Choose and compute dice mechanics: flat d20 vs bell-curve 2d6/3d6, advantage, dice pools and exploding dice, with AnyDice and a Python check of the odds."
sources:
  - https://anydice.com/
  - https://www.routledge.com/Game-Balance/Schreiber-Romero/p/book/9781498799577
  - https://gamebalanceconcepts.wordpress.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dice probability distributions

**Goal:** pick the dice mechanic whose odds produce the feel you want, and know the
exact probabilities before playtesting.

## Shapes and what they feel like
| Roll | Range | Shape | Key numbers |
|---|---|---|---|
| 1d20 | 1-20 | flat, 5% each | +1 modifier = +5% success; swingy |
| 2d6 | 2-12 | triangle | 7 = 6/36 = 16.7%; 2 or 12 = 2.8% |
| 3d6 | 3-18 | near bell | 10 and 11 = 12.5% each; 3 or 18 = 0.46% |
| d20 advantage (best of 2) | 1-20 | skewed high | P(>= t) = 1 - ((t-1)/20)^2; mean ~13.8 |
| d20 disadvantage | 1-20 | skewed low | P(>= t) = (21-t)^2/400; mean ~7.2 |
| dice pool (count 5+ on Nd6) | 0-N | binomial | P(success per die) = 1/3 |
Bell curves make modifiers matter less at the extremes and more in the middle, and
make outcomes predictable; flat dice make every +1 equally valuable and outcomes swingy.

## Compute with AnyDice
```
output 3d6
output [highest 1 of 2d20] named "advantage"
output 5d6 >= 5 named "pool successes"   \ count of dice showing 5+ \
output [explode d6]                        \ exploding d6 \
```
Read the "at least" view for target-number mechanics.

## Or check in Python (exact, by enumeration)
```python
from itertools import product
from collections import Counter
def dist(dice, f=sum):
    c = Counter(f(r) for r in product(*[range(1, d + 1) for d in dice]))
    n = sum(c.values()); return {k: v / n for k, v in sorted(c.items())}
p = dist([6, 6]); assert abs(p[7] - 6/36) < 1e-12
adv = dist([20, 20], max); print(sum(v for k, v in adv.items() if k >= 15))  # ~0.51
```

## Procedure
1. Decide the feel: swingy heroics (flat) or reliable competence (bell).
2. Choose target numbers so the **baseline success rate** matches intent (a common
   design target for a competent character on a routine task is well above 50%).
3. Compute how each +1 modifier shifts success at the target; check the extremes.
4. Check critical/fumble frequencies (natural 20 = 5% per roll; over a 4-hour session
   with 100 rolls, players will see ~5).

## Gotchas
- Players misjudge probability; 90% chances failing twice in a row "feels" broken. See
  `creative-arts.game-design.systems-and-mechanics.pseudo-random-distribution-and-bad-luck-protection`.
- Rolling many dice and summing is slow at the table; count-successes pools read faster.
- Exploding dice have unbounded ranges; cap them if numbers break other systems.

## Verify
- [ ] Distribution computed (AnyDice or enumeration) for every core roll.
- [ ] Success chance at each typical target written in the design doc.
- [ ] Extreme outcome frequency per session estimated.
