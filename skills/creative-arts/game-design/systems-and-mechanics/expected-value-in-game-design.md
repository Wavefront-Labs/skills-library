---
id: creative-arts.game-design.systems-and-mechanics.expected-value-in-game-design
name: expected-value-in-game-design
category: creative-arts
field: game-design
product: systems-and-mechanics
tags: [game-design, expected-value, probability-design, randomness-design, balance-math, damage-per-turn, risk-reward, variance, schreiber]
level: practitioner
status: draft
description: "Use expected value and variance to compare random options (attacks, gambles, loot, cards), find options that are secretly dominant, and tune risk-reward choices."
sources:
  - https://gamebalanceconcepts.wordpress.com/
  - https://www.routledge.com/Game-Balance/Schreiber-Romero/p/book/9781498799577
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Expected value in game design

**Goal:** compare random options numerically so that "safe vs risky" choices are real
choices and no option is quietly better in every case.

**Expected value (EV)** = sum over outcomes of (probability x value). **Variance** (or
standard deviation) measures spread: the risk.

## Worked example: two attacks
| Attack | Hit chance | Damage | EV per use |
|---|---|---|---|
| Quick jab | 90% | 4 | 3.6 |
| Haymaker | 50% | 9 | 4.5 |
Haymaker has higher EV but higher variance. Against an enemy with 4 HP left, the jab
(90% to kill) beats the haymaker (50% to kill): **EV is not the whole story when
thresholds matter.** Compute probability of reaching the threshold, not just the mean.

## Including costs
Normalise EV by cost: EV per mana, per action, per gold. Options with higher EV per
cost in all realistic situations are dominant (see
`creative-arts.game-design.systems-and-mechanics.finding-dominant-strategies`).

## Procedure
1. List the random options competing for the same decision.
2. Compute EV and standard deviation for each (spreadsheet: one column per outcome).
3. Compute **threshold probabilities** for common situations (kill in one hit, afford
   the item, survive the turn).
4. Ensure each option wins in some situation; tweak numbers if one is better in all.
5. Check perceived value: players overweight vivid low-probability wins (lottery
   effect) and dislike losses more than equivalent gains (loss aversion). A
   mathematically fair gamble may feel bad; tune presentation or the numbers.

## Spreadsheet sketch
```
A: outcome   B: probability   C: value   D: =B*C
E (EV): =SUM(D:D)
F (variance): =SUMPRODUCT(B:B,(C:C-E1)^2)
```

## Gotchas
- EV for multi-step processes (crit then bonus roll) needs the full tree; do not
  multiply averages when outcomes interact.
- Rounding (integer damage, minimum 1) changes EV at low values; model actual rules.
- EV assumes repeated play; one-shot high-stakes choices are judged by players on risk.

## Verify
- [ ] EV and variance listed for each competing option.
- [ ] Threshold probabilities computed for key situations.
- [ ] Every option is best in at least one realistic situation.
