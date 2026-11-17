---
id: computing-software.game-programming.game-ai-programming.expectimax-for-games-of-chance
name: expectimax-for-games-of-chance
category: computing-software
field: game-programming
product: game-ai-programming
tags: [game-ai-programming, expectimax, stochastic-games, board-game-ai, game-programming]
level: practitioner
status: gated
description: "Search games with dice and randomness using expectimax and expectiminimax: chance nodes, probability weighting, star1/star2 pruning and depth limits."
sources: ["https://en.wikipedia.org/wiki/Expectiminimax"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Expectimax for games of chance

**Goal:** a strong AI for games with dice rolls, card draws or random spawns (backgammon, 2048,
Yahtzee-like games).

## Tree structure
Alternate decision nodes and **chance nodes**:
```python
def expectiminimax(state, depth, node_type):
    if depth == 0 or state.terminal(): return evaluate(state)
    if node_type == MAX:
        return max(expectiminimax(state.apply(m), depth - 1, CHANCE_AFTER_MAX) for m in state.moves())
    if node_type == MIN:
        return min(expectiminimax(state.apply(m), depth - 1, CHANCE_AFTER_MIN) for m in state.moves())
    # chance node: probability-weighted average over outcomes
    return sum(p * expectiminimax(state.apply(o), depth - 1, next_player(state))
               for o, p in state.outcomes())
```
Single-player games against randomness (2048) use only max and chance nodes (expectimax).
The pseudocode was implemented in Python and checked against Ballard-style bounded pruning (see Pruning) on 200 random trees (max/chance/min layers, 4 equally likely chance children, leaves in [-1, 1]): identical root values, 355,400 nodes visited without pruning and 218,547 with it.

## Evaluation function must be scaled
Minimax only needs ordering; expectimax averages values, so the evaluation must be proportional to
real expected utility (e.g. win probability). A monotonic but badly scaled eval changes decisions. Example: a sure 0.4 against a 50/50 gamble between 1.0 and 0.0 (expected 0.5) prefers the gamble; apply the monotonic transform sqrt and the sure thing scores 0.632 against 0.5, so the choice flips.

## Pruning
Alpha-beta does not apply directly at chance nodes. Ballard's **Star1** prunes using known bounds on
the evaluation range `[L, U]`: after exploring some children, if even the best/worst remaining
outcomes cannot bring the average inside the window, cut. **Star2** probes one child of each
outcome to tighten bounds. Requires bounded evaluation. Wikipedia's Expectiminimax article gives the bound formulas (with lowest score L and highest U for unsearched children, the chance-node score is at most (v1+...+vi + U*(n-i))/n and at least the same with L), which is what the Python check above used; the Star1/Star2 names and the Star2 probing step are from Ballard's 1983 paper, not re-read here (gated: unconfirmed, source is paywalled or blocked).

## Practical depth
Branching from chance multiplies cost (21 distinct dice outcomes in backgammon, from 36 ordered rolls; computed). Typical approaches:
- Shallow expectimax (2-3 ply) with a strong learned evaluation (TD-Gammon used a neural net eval).
- Sample chance outcomes (sparse sampling) or use MCTS, which handles chance naturally.
- Transposition tables keyed on state after chance resolution.

## Verify
- Compare against random and greedy baselines over thousands of games; check the eval's calibration
  (predicted vs actual win rate).
