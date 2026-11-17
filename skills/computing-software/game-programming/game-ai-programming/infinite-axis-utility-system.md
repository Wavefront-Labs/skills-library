---
id: computing-software.game-programming.game-ai-programming.infinite-axis-utility-system
name: infinite-axis-utility-system
category: computing-software
field: game-programming
product: game-ai-programming
tags: [game-ai-programming, infinite-axis-utility, utility-ai, response-curves, game-programming]
level: practitioner
status: gated
description: "Build an infinite axis utility system: considerations with normalised inputs and response curves, multiplicative scoring with compensation, and designer tooling."
sources: ["https://www.gdcvault.com/play/1021848/Building-a-Better-Centaur-AI", "https://www.gameaipro.com/GameAIPro/GameAIPro_Chapter09_An_Introduction_to_Utility_Theory.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Infinite axis utility system

**Goal:** decisions scored from any number of considerations, each a designer-tunable curve
(Dave Mark and Mike Lewis, *Building a Better Centaur*, GDC 2015).

## Structure
- **Decision** (action + target) has a list of **considerations**.
- Each consideration reads one input (distance, health %, ammo, time since last used), normalises it
  to 0..1 with min/max bookends, and maps it through a **response curve** (linear, quadratic,
  logistic, logit) with parameters m, k, b, c.
- Decision score = product of consideration scores x decision weight.

```python
def score(d, ctx):
    s = d.weight
    for c in d.considerations:
        x = min(max((c.input(ctx) - c.min) / (c.max - c.min), 0.0), 1.0)
        s *= c.curve(x)
        if s <= 0: return 0.0              # early out
    n = len(d.considerations)
    return s + (1 - s) * (1 - 1 / n) * s   # compensation applied once to the product (gated: unconfirmed, source is paywalled or blocked)
```

## Compensation factor
Multiplying many values below 1 punishes decisions with more considerations. Dave Mark's fix as commonly described (gated: unconfirmed, source is paywalled or blocked; the GDC talk could not be fetched):
```text
modification = 1 - 1/n ;  makeUp = (1 - score) * modification ;  final = score + makeUp * score
```
The formula can be applied to the final product (as in the code above) or to each consideration score; the two give
different numbers (n = 3 considerations of 0.9: raw product 0.729, applied once 0.861, applied per consideration
0.885), so pick one and keep it identical for all decisions.

## Selection
Score all decision-target pairs, pick the highest, or weighted random among the top N for variety;
add a momentum bonus to the current decision to prevent flip-flopping.

## Tooling
- Curve editor with live preview; per-agent debug view listing each decision's consideration scores.
- Reusable consideration and decision libraries shared across archetypes.

## Pitfalls
- Input normalisation mistakes (bookends wrong) silently flatten curves.
- Too many decision-target pairs: prefilter targets cheaply.

## Verify
- Logged decision scores for a scenario match designer expectations; unit test curves at edges.

## Checked (2026-10-22)
- Computed the compensation arithmetic for 1, 2, 3 and 6 considerations of 0.9 (raw 0.9, 0.81, 0.729, 0.531; applied once 0.9, 0.887, 0.861, 0.739; per consideration 0.9, 0.893, 0.885, 0.859). The code block is re-implemented in Python (the original was C++, not compiled here).
- The exact compensation formula and its attribution to the Mark/Lewis GDC 2015 talk are gated: GDC Vault redirects to a maintenance page and a search found no free text of the formula. Game AI Pro ch. 9 PDF confirms the multiply-the-considerations technique and logistic response curves.
