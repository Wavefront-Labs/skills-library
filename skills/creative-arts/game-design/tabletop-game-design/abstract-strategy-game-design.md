---
id: creative-arts.game-design.tabletop-game-design.abstract-strategy-game-design
name: abstract-strategy-game-design
category: creative-arts
field: game-design
product: tabletop-game-design
tags: [game-design, tabletop-game-design, abstract-strategy, perfect-information, combinatorial-games, pie-rule, board-games]
level: practitioner
status: draft
description: "Design an abstract strategy game: minimal rules with deep play, first-player advantage and the pie rule, draws and game length, and testing depth with AI or solvers."
sources:
  - https://en.wikipedia.org/wiki/Abstract_strategy_game
  - https://en.wikipedia.org/wiki/Pie_rule
  - https://mitpress.mit.edu/9780262017138/characteristics-of-games/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Abstract strategy design

**Goal:** a game with few rules, perfect information and no luck (or nearly none) that
stays deep after hundreds of plays: Go, chess, Hex, Hive, Santorini, Onitama, the GIPF series.

## Design principles
1. **Elegance:** the rules fit on a card; depth comes from interaction, not exceptions.
   Count rules and exceptions; each exception needs to earn its place.
2. **Every move matters:** avoid long sequences of forced or obvious moves.
3. **Clear goal:** connection (Hex), capture (chess), territory (Go), pattern (Gomoku),
   race, or elimination. Goals that can be blocked forever produce draws.
4. **Tension between offence and defence:** one move should often do both.
5. **Board size and game length:** test sizes; small boards may be solved, large ones drag.
   Target 15-45 minutes for modern abstracts.

## First-player advantage
- Perfect-information games almost always favour one side. Measure the first-player win
  rate over many games (or self-play AI).
- Mitigations: **pie rule** (first player moves, second chooses to swap sides; standard in
  Hex), komi (Go's points for the second player), fewer pieces placed on the first turn
  (Connect6 places 1 then 2 per turn), alternating start in a match.

## Draws and stalemates
- Decide whether draws are acceptable; many modern abstracts design them out (Hex cannot draw).
- Add a progress rule (repetition ends the game, move limits) if cycles are possible.

## Testing depth
1. Play against yourself; look for an obviously best opening or a dominant piece.
2. Write a simple AI (minimax or Monte Carlo tree search) to find forced wins and measure
   first-player advantage over thousands of games.
3. Check whether better players beat weaker players consistently; depth shows as a skill gradient.
4. Track average game length and number of meaningful choices per turn (branching factor).

## Theming
Abstracts can carry light theme (Hive's insects, Santorini's buildings) to aid teaching
via piece identity, as long as theme does not add rules.

## Gotchas
- A rule added to fix a broken edge case often reveals a simpler core rule is wrong.
- Symmetric starting positions with a mirror strategy for the second player can make the game trivial.
- Very small games are quickly solved; check game-tree size.

## Verify
- [ ] Rules fit on one page.
- [ ] First-player win rate measured and mitigated.
- [ ] Stronger players win consistently in tests.
