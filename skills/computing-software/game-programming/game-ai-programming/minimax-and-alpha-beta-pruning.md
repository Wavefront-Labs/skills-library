---
id: computing-software.game-programming.game-ai-programming.minimax-and-alpha-beta-pruning
name: minimax-and-alpha-beta-pruning
category: computing-software
field: game-programming
product: game-ai-programming
tags: [game-ai-programming, game-tree-search, minimax, alpha-beta, negamax, iterative-deepening, move-ordering, evaluation-function, board-game-ai, game-programming, evaluation-functions]
level: practitioner
status: verified
description: "Write board/turn-based game AI with negamax and alpha-beta: evaluation functions, move ordering, iterative deepening under a time budget, and quiescence search."
sources: ["https://www.chessprogramming.org/Alpha-Beta", "https://www.chessprogramming.org/Iterative_Deepening", "https://www.routledge.com/AI-for-Games-Third-Edition/Millington/p/book/9781138483972"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Minimax and alpha-beta pruning

**Goal:** a strong opponent for two-player, turn-based, perfect-information games (board games,
tactics duels) within a fixed thinking time (Millington, AI for Games; chessprogramming.org).

## Negamax with alpha-beta
Minimax in negamax form (score always from the side to move's perspective):
```
int negamax(State& s, int depth, int alpha, int beta) {
    if (depth == 0 || s.gameOver()) return evaluate(s);     // from side-to-move perspective
    int best = -INF;
    for (Move m : orderedMoves(s)) {
        s.make(m);
        int score = -negamax(s, depth - 1, -beta, -alpha);
        s.unmake(m);
        if (score > best) best = score;
        if (best > alpha) alpha = best;
        if (alpha >= beta) break;                           // cutoff: opponent will avoid this line
    }
    return best;
}
```
With perfect move ordering, alpha-beta searches about sqrt of the minimax node count, i.e. roughly
twice the depth for the same time. Measured on random uniform trees (branching 6, depth 6): plain negamax 55,987
nodes, alpha-beta with random order 6,866, with best-first order 812 nodes of which 431 are leaves, which is exactly
`b^ceil(d/2) + b^floor(d/2) - 1`.

## Evaluation function
Weighted sum of features: material, mobility, positional tables, threats, king safety / objective
control. Keep it fast (called millions of times) and symmetric. Terminal states return large
win/loss scores adjusted by depth so faster wins score higher.

## Move ordering (biggest practical gain)
1. Best move from the previous iteration / transposition table.
2. Captures ordered by MVV-LVA (most valuable victim, least valuable attacker).
3. Killer moves (quiet moves that caused cutoffs at the same depth).
4. History heuristic for remaining quiet moves.

## Iterative deepening under a time budget
Search depth 1, 2, 3, ... until time runs out; keep the best move from the last completed depth.
Costs little extra because each iteration is dominated by the last, and earlier iterations improve
ordering. Check the clock every N nodes and abort cleanly.

## Quiescence search
At depth 0, keep searching captures (and checks/forced moves) until the position is quiet, to avoid
the horizon effect (stopping just before a recapture). Use stand-pat: `if eval >= beta return beta`.

## Making it a game opponent, not just strong
- Difficulty: limit depth/time, add noise to evaluation, or pick among top-N moves with weighted
  randomness; avoid obvious blunders at low levels by still searching 1-2 ply for tactics.
- Make/unmake moves in place (no state copies) for speed; use Zobrist hashing for repetitions and the
  transposition table.
- For games with chance or hidden information, use expectimax or MCTS instead.

## Verify
- [ ] Perft-style test: move generator counts match known values for test positions.
- [ ] Alpha-beta returns the same best score as plain minimax at small depths (test).
- [ ] Reaches target depth within time budget on target hardware; stronger levels beat weaker in self-play.

## Checked (2026-10-22)
- The C++ negamax is re-implemented in Python (no C++ compiler here) and run: alpha-beta with random and best-first ordering returned the same root value as plain negamax on 5 random trees; node counts above.
- Fetched chessprogramming.org pages: MVV-LVA ('most valuable victim'), Quiescence_Search ('stand-pat'), Transposition_Table (best move kept when depth is insufficient); Killer_Heuristic, History_Heuristic and Iterative_Deepening pages exist (HTTP 200). Millington chapter numbers were removed (book not available).
