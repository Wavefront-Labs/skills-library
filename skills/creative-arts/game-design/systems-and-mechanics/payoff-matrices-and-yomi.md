---
id: creative-arts.game-design.systems-and-mechanics.payoff-matrices-and-yomi
name: payoff-matrices-and-yomi
category: creative-arts
field: game-design
product: systems-and-mechanics
tags: [game-design, payoff-matrix, yomi, game-theory, mixed-strategy, nash-equilibrium, mind-games, rock-paper-scissors, fighting-games, meaningful-choice]
level: advanced
status: draft
description: "Model simultaneous player choices as payoff matrices, find the mixed-strategy equilibrium, and design yomi (reading the opponent) instead of a solved best move."
sources:
  - https://mitpress.mit.edu/9780262240451/rules-of-play/
  - https://gamebalanceconcepts.wordpress.com/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Payoff matrices and yomi

**Goal:** design simultaneous or hidden choices (attack/block/throw, bid high/low,
reveal/hide) so that no single move is correct and the skill lies in predicting the
opponent.

Rules of Play (ch28 Game Theory) introduces payoff matrices for analysing games of
simultaneous decision. David Sirlin's "Yomi" articles describe the design aim: reward
reading the opponent ("knowing the mind of the opponent"), with counters to counters.

## Build the matrix
Rows = my options, columns = opponent options, cells = my payoff.
```
            Opp: Attack  Opp: Block  Opp: Throw
Me: Attack      0          -1          +2
Me: Block      +1           0          -2
Me: Throw      -2          +2           0
```
Check:
1. **No row dominates** another (every row has a cell where it is the best response).
2. **The mixed-strategy equilibrium** (the probability mix where the opponent cannot
   exploit you) is not degenerate. Solve with the indifference method for 2-3 options,
   or use a small linear program for larger matrices.
3. **Equilibrium probabilities** match the play you want. If "Attack" should be the
   common move, its payoffs should support a higher equilibrium weight.

## Designing yomi layers
- Each option needs a counter, and each counter a counter-counter (Sirlin's layers 0-3).
- Unequal payoffs create interesting reads (a risky option that wins big but loses big).
- Give players **information to read**: tells, history, resources that constrain the
  opponent's options (if they have no meter, they cannot use the super).

## Python check of a 2x2 mixed equilibrium
```python
# payoffs for row player: a b / c d ; opponent zero-sum
a, b, c, d = 2, -1, -1, 1
q = (d - b) / (a - b - c + d)   # prob opp plays column 1 that makes row indifferent
assert 0 < q < 1
```

## Gotchas
- Pure rock-paper-scissors with equal payoffs is random at equilibrium; add asymmetric
  payoffs, information or resources so reads matter.
- Real players are not at equilibrium; design should reward exploiting habits while
  allowing the exploited player to adapt.
- In multiplayer (3+), payoff analysis gets messy (kingmaking, alliances); use playtests.

## Verify
- [ ] Matrix drawn for each simultaneous decision point.
- [ ] No dominated or dominant rows.
- [ ] Equilibrium mix computed and compatible with intended play patterns.
