---
id: mathematics.operations-research.game-theory.finding-nash-equilibria
name: finding-nash-equilibria
category: mathematics
field: operations-research
product: game-theory
tags: [operations-research, game-theory, nash-equilibrium, normal-form-game, payoff-matrix, dominant-strategy, iterated-dominance, best-response, mixed-strategy, indifference-principle, zero-sum, minimax, prisoners-dilemma, coordination-game, extensive-form, backward-induction, subgame-perfect-equilibrium, repeated-games, folk-theorem, auctions, mechanism-design, nashpy, gambit]
level: practitioner
status: verified
description: "Find and interpret equilibria: write the payoff matrix, eliminate dominated strategies, mark best responses, solve mixed equilibria by indifference, and use backward induction for sequential games."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Finding Nash equilibria

**Goal:** given a strategic situation, compute its equilibria by hand or code, and say
what they do and don't predict.

## 1. Write the game
- **Players**, each player's **strategies**, and **payoffs** for every combination.
- Normal form: a matrix, row player's payoff first: (row, column).
- Payoffs must reflect what players actually care about (including fairness, reputation),
  or the analysis is about a different game.

## 2. Eliminate dominated strategies
A strategy is **strictly dominated** if another strategy is better against *every*
opponent choice. Rational players never play it — delete it and repeat (**iterated
elimination**). Strict dominance elimination never removes a Nash equilibrium; with
weak dominance, the order can matter and equilibria can be lost — be careful.

## 3. Pure equilibria: mark best responses
For each column, underline the row player's best payoff; for each row, underline the
column player's best. A cell with **both underlined** is a pure Nash equilibrium —
no one gains by deviating alone.
Prisoner's dilemma (C = cooperate, D = defect):
|  | C | D |
|---|---|---|
| **C** | (3, 3) | (0, 5) |
| **D** | (5, 0) | (1, 1) |
D strictly dominates C for both; unique equilibrium (D, D) = (1, 1), although (C, C) is
better for both. Equilibrium ≠ efficient.

## 4. Mixed equilibria: the indifference principle
In a mixed equilibrium, each player mixes so that the **opponent is indifferent**
between the strategies the opponent uses.
Example — matching-pennies-style game, row chooses U/D with prob p/(1−p), column L/R:
|  | L | R |
|---|---|---|
| **U** | (2, −2) | (−1, 1) |
| **D** | (−1, 1) | (1, −1) |
Column indifferent: −2p + 1(1−p) = 1p − 1(1−p) → 1 − 3p = 2p − 1 → p = 2/5.
Row indifferent with column's q = P(L): 2q − (1−q) = −q + (1−q) → 3q − 1 = 1 − 2q → q = 2/5.
Equilibrium: row plays U 40%, column plays L 40%. Note: **each player's mix is set by the
other's payoffs**, a frequent surprise.
Checked with nashpy 0.0.43 `support_enumeration()`: the prisoner's dilemma gives only (D, D); this matching game gives p = q = 0.4, i.e. U 40% and L 40%; the zero-sum LP below on the same matrix returned row mix (0.4, 0.6) and value 0.2; a 2x2 coordination game gave 3 equilibria (odd). Every finite game has at least one equilibrium (possibly mixed). Non-degenerate games
have an odd number of them.

## 5. Zero-sum games: minimax
In two-player zero-sum games, Nash = minimax: each maximises their guaranteed payoff.
Solve the row player's mix with an LP: maximise v s.t. Σᵢ pᵢ aᵢⱼ ≥ v for every column j,
Σ pᵢ = 1, p ≥ 0.

## 6. Sequential games: backward induction
Draw the tree; at the last decisions choose each mover's best action, replace that node
with its payoff, and work back to the root. The result is a **subgame-perfect equilibrium**:
it rules out non-credible threats ("I'll start a price war if you enter" is ignored if a
price war would hurt the threatener at that point).

## 7. Repeated games
A one-shot prisoner's dilemma ends in (D, D), but with indefinite repetition and players
patient enough, cooperation can be sustained by strategies like **grim trigger** or
**tit-for-tat** (folk theorem). Cooperation needs: future interaction likely enough,
deviations observable, punishment credible. Finite, known-end repetition unravels
by backward induction in theory (though people often cooperate in experiments).

## 8. Software
- Python `nashpy`: `nash.Game(A, B).support_enumeration()` lists equilibria of a bimatrix game.
- Gambit (GUI and `pygambit`) for larger and extensive-form games.
- For zero-sum, any LP solver (section 5).

## Applications glimpse
- **Auctions:** in a second-price sealed-bid auction, bidding your true value is a
  weakly dominant strategy (checked by brute force over integer bids 0-10 for value 5); in first-price, bidders shade below value.
- **Mechanism design:** design rules so that the equilibrium outcome is the one you want
  (e.g. truthful reporting).

## Gotchas
- Multiple equilibria (coordination games) — theory alone may not tell you which is
  played; look at focal points, history, communication.
- Nash assumes common knowledge of rationality; real players learn, err and care about fairness.
- A mixed equilibrium doesn't require players to literally randomise — it can describe
  population frequencies.
- The "odd number of equilibria" result applies to non-degenerate games: for an all-ones 2x2 game nashpy returned 4 equilibria with a degeneracy warning (the true set is a continuum).

## Verify
- [ ] Payoff matrix checked with whoever knows the situation.
- [ ] Dominated strategies removed (strict only, unless weak elimination is justified).
- [ ] Every candidate equilibrium checked: no player gains by a unilateral deviation.
- [ ] Mixed probabilities verified by plugging back — opponent's expected payoffs equal.
- [ ] Sequential games solved by backward induction; threats checked for credibility.
