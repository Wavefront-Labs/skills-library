---
id: creative-arts.game-design.systems-and-mechanics.card-draw-odds-hypergeometric
name: card-draw-odds-hypergeometric
category: creative-arts
field: game-design
product: systems-and-mechanics
tags: [game-design, hypergeometric, draw-odds, card-games, deck-building, probability-design, randomness-design, deck-size, mulligan, opening-hand]
level: practitioner
status: docs-checked
description: "Compute card draw odds with the hypergeometric distribution to size decks, set copy limits, and tune opening hands and mulligans."
sources:
  - https://docs.python.org/3/library/math.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Card draw odds (hypergeometric)

**Goal:** know how often a player sees a given card or card type, so deck sizes, copy
limits and hand sizes produce the consistency you intend.

Drawing without replacement follows the **hypergeometric distribution**:
P(exactly k successes) = C(K,k) x C(N-K, n-k) / C(N,n), where N = deck size, K =
copies of the target, n = cards drawn.

## Python
```python
from math import comb
def p_at_least(N, K, n, k=1):
    return sum(comb(K, i) * comb(N - K, n - i) for i in range(k, min(K, n) + 1)) / comb(N, n)
# 4 copies in a 60-card deck, 7-card opening hand:
assert abs(p_at_least(60, 4, 7) - 0.3995) < 0.001
# same card in a 40-card deck:
print(round(p_at_least(40, 4, 7), 3))   # ~0.552
```
`math.comb(n, k)` is the number of ways to choose k items from n without repetition and
without order (Python 3.8 or later).

## Reference points (4 copies, 7-card hand)
| Deck size | P(at least 1) |
|---|---|
| 40 | ~55% |
| 60 | ~40% |
These two numbers explain why smaller decks are more consistent and why copy limits
interact with deck minimums.

## Design uses
1. **Resource consistency:** P(at least 2 resource cards in opening hand) for land/
   energy systems; tune the recommended ratio from it.
2. **Combo reliability:** P(drawing piece A and B by turn T); multiply carefully - they
   are not independent; enumerate or simulate.
3. **Mulligan rules:** compute how much a mulligan rule improves P(playable hand).
4. **Copy limits:** a limit of 4 vs 3 vs 1 (singleton) directly sets how often key
   cards appear.
5. **Event decks in board games:** P(the bad event appears in the first X draws) to
   place it in a sub-deck ("stack the bottom half") if timing matters.

## Gotchas
- Shuffled decks with discard reshuffles change N over time; model the actual cycle.
- Deck-thinning effects in deck-builders (trashing cards) raise P quickly; compute at
  several deck sizes.
- Players' intuitions about "should have drawn it by now" are poor; for core
  resources add smoothing (mulligans, card selection).

## Verify
- [ ] Opening-hand probabilities computed for core card types.
- [ ] Combo/resource odds by turn T computed by enumeration or simulation.
- [ ] Deck size, copy limit and mulligan rule chosen from the numbers.

## Checked
Checked 2026-11-09 against the Python math module documentation: `comb(n, k)` meaning and
the 3.8 version note. The two reference figures (0.3995 and 0.552) were recomputed by hand
from 1 - C(N-K,n)/C(N,n). Removed the spreadsheet formula and the Wikipedia source (neither
readable this batch). The hypergeometric formula itself is standard probability and was
checked only by that arithmetic, not against a cited page.
Method: documentation only; no commands were run.
