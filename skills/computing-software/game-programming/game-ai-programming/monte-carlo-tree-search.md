---
id: computing-software.game-programming.game-ai-programming.monte-carlo-tree-search
name: monte-carlo-tree-search
category: computing-software
field: game-programming
product: game-ai-programming
tags: [game-ai-programming, game-tree-search, mcts, uct, playouts, ismcts, board-game-ai, card-game-ai, game-programming]
level: advanced
status: verified
description: "Use Monte Carlo Tree Search for game AI: selection with UCT, expansion, playouts, backpropagation, time budgets, heavy playouts, and ISMCTS for hidden-information card games."
sources: ["https://www.routledge.com/AI-for-Games-Third-Edition/Millington/p/book/9781138483972", "http://www.incompleteideas.net/609%20dropbox/other%20readings%20and%20resources/MCTS-survey.pdf", "https://en.wikipedia.org/wiki/Monte_Carlo_tree_search"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Monte Carlo Tree Search (MCTS)

**Goal:** decent play in games where writing a good evaluation function is hard (Go-like, many
moves, randomness, card games), using simulations instead of heuristics (Browne et al. MCTS survey;
Millington, AI for Games).

## Four steps per iteration
```
node = root
1. Selection: while node fully expanded and not terminal: node = argmax_child UCT(child)
     UCT = child.wins / child.visits + C * sqrt(ln(node.visits) / child.visits)   # survey: Cp = 1/sqrt(2) in 2*Cp*sqrt(2 ln n / n_j), i.e. C = 2 here, for rewards in [0,1]; tune
2. Expansion: if not terminal, add one untried move as a new child; node = child
3. Simulation (playout): from node's state play random (or lightly guided) moves to the end
4. Backpropagation: walk back to root updating visits and wins (from each node's player's perspective)
repeat until time budget; choose root child with the most visits (robust child)
```

## Practical details
- **Anytime**: stop when the frame/turn budget expires; more iterations = stronger play. Spread across
  frames or a worker thread.
- **Heavy playouts**: use cheap heuristics (prefer captures, avoid obvious blunders) instead of pure
  random moves; big strength gains, at the cost of iterations.
- **Playout cutoff**: stop playouts after N moves and score with a simple evaluation.
- **Tree reuse**: after a move, keep the chosen child's subtree as the new root.
- Memory: node pools; cap node count.
- Exploration constant C tuned per game (and reward scale normalised to [0,1]).

## Randomness and hidden information
- Chance nodes (dice) can be handled by sampling outcomes during simulation.
- **ISMCTS** (Information Set MCTS; the survey describes an early variant as ISUCT) for card games: each iteration samples a **determinization** (a
  plausible assignment of hidden cards consistent with what the AI knows) and searches nodes keyed by
  information sets; avoids the AI "cheating" or strategy-fusion errors of naive determinization.

## Difficulty
Scale iterations/time, playout quality, or pick among top moves weighted by visits with temperature.
Fewer iterations degrade play naturally (more human-like mistakes than depth-limited minimax).

## Verify
- [ ] Win rate vs random and vs a simple heuristic bot increases with iteration count (self-play test).
- [ ] Search respects the time budget on target hardware.
- [ ] For hidden-information games, the AI never uses information it should not know (audit determinization).

## Checked (2026-10-22)
- Implemented the four steps with the formula as written (tic-tac-toe, wins credited to the player who moved into each node, draws 0.5, most-visited root child): score against a random player 0.70 at 5 iterations, 0.91 at 30, 1.00 at 200 (40 games each).
- Browne et al. survey PDF: UCT formula `X_j + 2 Cp sqrt(2 ln n / n_j)` with Cp = 1/sqrt(2) valid for rewards in [0,1], 'robust child = most visited root child', ISUCT mentioned. Removed the unverified Spades/AI Factory claim; the ISMCTS algorithm text itself is not checked against Cowling et al. beyond the survey's mention.
