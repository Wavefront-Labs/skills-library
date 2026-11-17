---
id: computing-software.game-programming.game-ai-programming.opening-books-and-endgame-tables
name: opening-books-and-endgame-tables
category: computing-software
field: game-programming
product: game-ai-programming
tags: [game-ai-programming, opening-book, endgame-tablebase, board-game-ai, game-programming]
level: practitioner
status: verified
description: "Add opening books and endgame tablebases to board-game AI: book formats and selection, Polyglot books, Syzygy probing and variety without losing strength."
sources: ["https://www.chessprogramming.org/Opening_Book", "https://www.chessprogramming.org/Syzygy_Bases"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Opening books and endgame tables

**Goal:** perfect or expert play at the start and end of the game, where search is weakest or wasteful.

## Opening books
- A map from position hash (Zobrist) to candidate moves with weights (from master games or
  self-play statistics).
- **Polyglot format** (chess): 16-byte entries sorted ascending by key `{key u64, move u16, weight u16, learn u32}`,
  integers stored most significant byte first (`struct.calcsize(">QHHI") == 16`); binary search by position key. A
  weight of 0 means do not play the move. Keys are the XOR of entries of a fixed `Random64[781]` table (768 piece-square,
  4 castling, 8 en passant, 1 turn), so compute Polyglot keys separately from the engine's own Zobrist keys.
- Selection: weighted random by weight for variety; filter moves with poor results; limit book depth
  for lower difficulties.
- Handle transpositions naturally since lookup is by position, not move sequence.
- Leave the book when no entry or when weights fall below a threshold.

## Endgame tablebases
Retrograde analysis: from all mate positions, work backwards computing win/draw/loss and distance.
- **Syzygy** (chess, up to 7 pieces; the 8-piece set is not built): WDL tables (win/draw/loss, probed during search) and DTZ
  tables (distance to zeroing move, used at the root to make progress under the 50-move rule).
  Fathom (MIT licence, C99 or C++) is a stand-alone Syzygy probing tool with `tb_probe_wdl` and `tb_probe_root`.
- Probe WDL in search at nodes with few pieces; treat results as exact scores.
- Other games: the 2007 Science result that checkers is a draw used a database of all positions with 10 or fewer
  pieces (about 3.9 x 10^13 positions) built with the Chinook team's backward computation; for your own game, generate
  tables offline when piece counts are small.

## Practicalities
- File sizes: the full 6-piece Syzygy set is roughly 150 GB (the ChessProgramming page says keeping full DTZ for both
  sides would add 158 GB for 307 GB in total); ship only what fits.
- Memory-map tables; lazy-load files.
- In games for casual players, books and tables can make the AI feel too strong or repetitive;
  scale usage by difficulty.

## Verify
- Book lookups match expected moves for known openings; tablebase positions are converted correctly
  (engine wins KQK every time, draws known draws).

## Checked (2026-10-22)
- Computed the entry size with `struct.calcsize(">QHHI")` = 16 and read H.G. Muller's Polyglot book format page (field sizes, big-endian, weight 0, `Random64[781]` split 768 + 4 + 8 + 1).
- ChessProgramming 'Syzygy Bases': WDL (.rtbw) for search and DTZ (.rtbz) at the root, 7-man tables exist, 6-man size arithmetic (307 GB - 158 GB); Fathom GitHub README (MIT, C99/C++, tb_probe_wdl, tb_probe_root); checkers result via the Science 2007 paper summary (10-piece database, 3.9 x 10^13 positions). Removed the unconfirmed 5-piece '~1 GB' figure and the castling-rights remark. Retrograde analysis is described, not run.
