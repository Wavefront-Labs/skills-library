---
id: sports-recreation.mind-sports-and-games.chess-engines.stockfish-lc0-analysis-and-opening-prep
name: stockfish-lc0-analysis-and-opening-prep
category: sports-recreation
field: mind-sports-and-games
product: chess-engines
tags: [chess-engines, stockfish, leela-chess-zero, lc0, nnue, uci, chessbase, scid, scid-vs-pc, en-croissant, lichess, chess-com, game-review, engine-analysis, evaluation, centipawns, depth, multipv, opening-database, opening-explorer, repertoire-file, pgn, preparation, opponent-prep, blunder-check, hash, threads, fair-play]
level: practitioner
status: draft
description: "Using chess engines for improvement: Stockfish vs Lc0, reading evaluations, depth and MultiPV, analysing your games without outsourcing thinking, opening databases and preparing for an opponent."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Chess engines — Stockfish/Lc0 analysis and opening prep

**Goal:** use engines and databases to learn from your games and prepare
openings, without letting the engine do the thinking. For over-the-board
skills see `sports-recreation.mind-sports-and-games.chess`.

## 1. The tools
- **Stockfish** — free, open-source, the strongest classical-search
  engine (with NNUE neural evaluation since version 12). Runs in most
  GUIs and in the browser on Lichess.
- **Leela Chess Zero (Lc0)** — neural-network engine; strong, more
  "human-strategic" style; runs best on a GPU.
- **GUIs:** Lichess analysis board (free, browser), Chess.com analysis/Game
  Review, ChessBase (commercial, Windows), Scid vs. PC and En Croissant
  (free desktop). Engines speak the **UCI** protocol, so any UCI engine
  plugs into any of these GUIs.
- **Databases:** Lichess opening explorer (masters and online games),
  ChessBase Mega Database (commercial), PGN files from TWIC (The Week in
  Chess) for recent games.

## 2. Reading engine output
- **Evaluation** in pawns/centipawns from White's view: +1.00 ≈ a pawn
  ahead for White. Rough reading: within ±0.5 roughly equal; ±1 to ±2
  clear advantage; beyond ±2 usually winning. "#5" = mate in 5.
- **Depth** — how many plies the search reached; let it run to a stable
  evaluation (depth 25+ in middlegames on modern hardware is usually
  plenty for analysis).
- **MultiPV** (number of lines) — set to 3-5 to see alternatives; if the
  top moves are close, the position is flexible; if only one move holds,
  it's critical.
- Settings: give the engine more **threads** (CPU cores minus one) and a
  bigger **hash** (memory) for deeper analysis.
- Evaluations of blocked/fortress positions can be misleading; a large
  eval with no progress possible may still be a draw.

## 3. Analysing your own games (the right order)
1. **Annotate without an engine** first: your thoughts during the game,
   critical moments, what you feared.
2. Check the opening against a **database** — where did you leave theory?
3. Turn the engine on and find the **biggest evaluation swings** (game
   review tools flag blunders/mistakes).
4. For each, ask *why* you missed it (didn't see the threat? miscounted?
   time pressure?) — and write the lesson.
5. Don't memorise engine lines you don't understand; play out the
   suggested move against the engine to see the idea.

## 4. Opening preparation
- Build a **repertoire file** (PGN or a study on Lichess / ChessBase
  repertoire database) with your main lines and short notes on the ideas.
- Use the database for **what people actually play** (move frequency,
  scores at your level) and the engine to **check** your lines for tactical
  holes.
- **Opponent prep:** download their games (online accounts or tournament
  PGNs), filter by colour and first moves, find their most likely lines,
  and prepare one solid plan against each — not a 30-move novelty.
- Review prep the evening before, not the morning of the game.

## 5. Fair play
Using an engine during a game (online or OTB) is cheating and results in
bans; sites run statistical detection. Disable engine/eval displays in
any app while playing rated games, and don't analyse ongoing
correspondence games where rules forbid engines (rules vary by event).

## Gotchas
- Trusting a low-depth eval during the first second of analysis.
- Prepping engine novelties you can't explain — opponents deviate on move 7.
- Calling a 0.3 eval drop a "mistake": that's noise at club level.

## Verify
- [ ] You annotated the game yourself before opening the engine.
- [ ] Engine ran with MultiPV ≥ 3 and reached a stable evaluation.
- [ ] Each big mistake has a written "why I missed it".
- [ ] Your repertoire file has ideas noted, not just moves.
