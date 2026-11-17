---
id: computing-software.game-programming.game-ai-programming.transposition-tables-and-zobrist-hashing
name: transposition-tables-and-zobrist-hashing
category: computing-software
field: game-programming
product: game-ai-programming
tags: [game-ai-programming, game-tree-search, transposition-table, zobrist-hashing, alpha-beta, bound-types, replacement-scheme, board-game-ai, game-programming]
level: advanced
status: verified
description: "Speed up game-tree search with transposition tables: incremental Zobrist hashing, depth/score/bound/best-move entries, replacement schemes and alpha-beta pitfalls."
sources: ["https://www.chessprogramming.org/Transposition_Table", "https://www.chessprogramming.org/Zobrist_Hashing", "https://www.routledge.com/AI-for-Games-Third-Edition/Millington/p/book/9781138483972"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Transposition tables and Zobrist hashing

**Goal:** avoid re-searching positions reached by different move orders, and reuse previous
iterations' best moves for ordering (Millington, AI for Games; chessprogramming.org).

## Zobrist hashing
Assign a random 64-bit number to each (piece type, square) pair, plus side-to-move and other state
(castling rights, en passant file, etc.). The position hash is the XOR of numbers for everything present:
```
init: for each piece p, square s: Z[p][s] = random64(); Zside = random64()
make move (piece p from a to b, capturing q on b):
    h ^= Z[p][a]; h ^= Z[p][b]; if q: h ^= Z[q][b]; h ^= Zside
```
Incremental update is O(1) per move; unmaking applies the same XORs. Use a fixed seed so hashes are
reproducible for debugging.

## Table entry
```
entry fields: key, score, depth, bound, best move, age
bound: EXACT (score within window), LOWER (fail-high: score >= beta), UPPER (fail-low: score <= alpha)
```
Table size a power of two; index = `key & (size - 1)`; store the full key (or upper bits) to detect
collisions.

## Using it in alpha-beta
```
probe at node start:
    e = tt[index]
    if e.key == key and e.depth >= depth:
        if e.bound == EXACT: return e.score
        if e.bound == LOWER and e.score >= beta: return e.score
        if e.bound == UPPER and e.score <= alpha: return e.score
    ttMove = (e.key == key) ? e.best : none        # search it first even if depth is insufficient
store at node end with bound from the result relative to the ORIGINAL alpha/beta
```

## Replacement schemes
Depth-preferred (keep deeper searches), always-replace (newer info), or two-tier buckets (one of each).
Age entries per search so stale ones get replaced. Typical tables: tens to hundreds of MB in engines;
a few MB suffice for game AI on a time budget.

## Pitfalls
- Mate/win scores adjusted by ply when storing/retrieving (store relative to the node, not root).
- Repetition/draw detection depends on path history, which hashes do not capture: TT cutoffs can hide
  repetitions; handle carefully in games with repetition rules.
- Missing state in the hash (side to move, special rights) causes wrong cutoffs: include everything that
  affects legal moves or evaluation.

## Verify
- [ ] Incremental hash equals full recomputation after random move sequences (test).
- [ ] Search with TT returns the same best score as without at fixed depth (correctness), with fewer nodes.
- [ ] Node count reduction and time saved measured per depth.

## Checked (2026-10-22)
- Python re-implementation (no C++ compiler) on a 5x4 connect-3 game: incremental XOR hash equals full recomputation after every move of 300 random games and returns to 0 after unmaking; alpha-beta with the probe/store rules above returned the same score as without a table at depths 4, 6, 8 and 10 (0, 0, 0, 991) with fewer nodes (93/87, 929/682, 7810/4328, 33195/13891).
- chessprogramming.org: Zobrist = XOR of per-feature random numbers, 64-bit keys standard; transposition table entries carry exact/lower/upper node types and the best move is usable even when depth is insufficient. The C struct with field widths was replaced by a field list (not compiled).
