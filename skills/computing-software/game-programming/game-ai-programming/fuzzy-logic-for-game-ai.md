---
id: computing-software.game-programming.game-ai-programming.fuzzy-logic-for-game-ai
name: fuzzy-logic-for-game-ai
category: computing-software
field: game-programming
product: game-ai-programming
tags: [game-ai-programming, fuzzy-logic, membership-functions, fuzzy-rules, defuzzification, combs-method, decision-making, behavior-tree, game-ai, game-programming]
level: practitioner
status: verified
description: "Apply fuzzy logic to NPC decisions: membership functions, AND/OR operators, rule evaluation, defuzzification, and avoiding combinatorial rule explosion with the Combs method."
sources: ["https://www.routledge.com/AI-for-Games-Third-Edition/Millington/p/book/9781138483972", "https://www.jblearning.com/catalog/productdetails/9781556220784"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fuzzy logic for game AI

**Goal:** smooth decisions from continuous inputs (distance, health, ammo) without hard thresholds
that make NPCs flip-flop (Millington, AI for Games; Buckland, Programming Game AI by Example).

## 1. Fuzzify inputs with membership functions
Each linguistic set maps a crisp value to a degree 0..1. Triangles, trapezoids and shoulders:
```
Distance: Close  = left shoulder (0 m ->1, 10 m ->0)
          Medium = triangle (5, 15, 25)
          Far    = right shoulder (20 m ->0, 30 m ->1)
Ammo:     Low = shoulder(0..5), Okay = triangle(3, 10, 20), Loads = shoulder(15..30)
```
Overlapping sets are the point: at 8 m the target is 0.2 Close and 0.3 Medium.

## 2. Rules
```
IF Close  AND Low   THEN Desirability(RocketLauncher) = Undesirable
IF Medium AND Okay  THEN Desirability = Desirable
IF Far    AND Loads THEN Desirability = VeryDesirable
```
Operators: AND = min, OR = max, NOT = 1 - x. A rule's output degree = the combined antecedent
degree; each output set's degree = max over rules firing it.

## 3. Defuzzify
- **Centroid**: centre of mass of the clipped output sets; smooth, more CPU.
- **Weighted average of representative values**: weight each output set's representative value by its degree:
  `sum(deg_i * rep_i) / sum(deg_i)`. Cheap and fine for games. It is not the mean-of-maxima method (which looks only
  at the output set(s) with the highest degree; Wikipedia lists MeOM and WFM as separate methods). With degrees
  0.2/0.6/0.3 and representatives 10/50/90 it gives 53.6, whereas picking only the top set gives 50.
The crisp result is used directly (score a weapon) or compared across options.

## Rule explosion
With N variables of M sets each, a full rule base has M^N rules. Mitigations:
- **Combs method** (Combs and Andrews, IEEE Trans. Fuzzy Systems 6(1), 1998): a different rule configuration
  whose rule count grows linearly with the number of inputs instead of multiplying.
- Keep variables per decision to 2-3; split into separate fuzzy modules per decision.

## When to use (and not)
- Good: weapon choice, aggression level, driving (steering by angle/distance), blending behaviours.
- Overlaps heavily with **utility AI** response curves, which many teams find easier to author and
  debug. Fuzzy logic shines when designers want rule-like "IF far AND healthy THEN aggressive" text.
- Not a probability system; degrees are not likelihoods.

## Verify
- [ ] Plot output over the input range: continuous, no sudden jumps at set boundaries.
- [ ] Every input value is covered by at least one set (no zero-degree gaps).
- [ ] Debug view lists firing rules with degrees for a selected NPC.

## Checked (2026-10-22)
- Computed the membership functions in the skill: at 8 m Close = 0.2, Medium = 0.3, Far = 0 as stated; both the distance and ammo sets cover their whole range (no zero-degree gaps) when evaluated every 0.1 units.
- Defuzzification: Wikipedia's page lists centre of gravity (centroid) and names MeOM and WFM among 20 methods; the weighted-average arithmetic above is computed. Rule explosion M^N (3^4 = 81 versus 4*3 = 12 for 4 variables of 3 sets) is arithmetic; Combs method citation and 'linear growth' confirmed from the IEEE abstract page (search result). Book chapter numbers removed.
