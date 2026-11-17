---
id: sports-recreation.mind-sports-and-games.chess.openings-calculation-endgames-and-tournament-play
name: openings-calculation-endgames-and-tournament-play
category: sports-recreation
field: mind-sports-and-games
product: chess
tags: [chess, chess-improvement, opening-principles, opening-repertoire, tactics, tactical-puzzles, calculation, candidate-moves, checks-captures-threats, blunder-check, middlegame, pawn-structure, endgames, king-and-pawn, opposition, lucena, philidor, rook-endgames, time-management, increment, tournament-chess, fide, uscf, elo, rating, notation, touch-move, clock, arbiter]
level: practitioner
status: draft
description: "Getting better at chess: opening principles and a small repertoire, the checks-captures-threats calculation routine, essential endgames, and tournament conduct, clocks and time management."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Chess — openings, calculation, endgames and tournament play

**Goal:** stop losing to blunders, reach playable middlegames, convert
won endgames and handle a tournament clock — the things that move a club
player's rating most. Engine work is in
`sports-recreation.mind-sports-and-games.chess-engines`.

## 1. Openings: principles over memorisation
- **Develop** knights and bishops toward the centre; **control/occupy the
  centre** with pawns; **castle** early; connect the rooks.
- Don't move the same piece twice without reason, or bring the queen out
  early where it can be chased with tempo.
- Below roughly 1800 rating, a **small repertoire** is enough: one answer
  to 1.e4 and one to 1.d4 as Black, one main system as White. Learn the
  *ideas* (typical pawn breaks, piece placement) and ~8-10 moves of main
  lines, not 25 moves of theory.
- When the opponent leaves your preparation, fall back on principles.

## 2. Calculation and blunder-checking
Before every move (especially in critical positions):
1. **What does the opponent's last move threaten?** (The most-skipped
   question.)
2. **Checks, captures, threats** — for both sides, in that order.
3. Pick **2-3 candidate moves**; calculate each to a quiet position.
4. **Blunder check** the chosen move: after it, does any piece hang? any
   check, fork or pin for them?
- Tactics training: 20-30 minutes of puzzles daily, focusing on solving
  correctly, not fast. Common motifs: fork, pin, skewer, discovered
  attack, removing the defender, back-rank mate, deflection.
- Count attackers vs defenders on a square before capturing.

## 3. Middlegame strategy (quick checklist)
- Improve your worst-placed piece.
- Rooks on open files; knights on outposts (squares no enemy pawn can
  attack).
- Plan from the **pawn structure**: attack on the side where you have
  more space / where your pawns point.
- Trade pieces when ahead in material; avoid trades when attacking.

## 4. Essential endgames (learn these exactly)
- **King and pawn vs king:** the **opposition** (kings facing with one
  square between, side *not* to move has the opposition); key squares.
- **Rook endgames:** the **Lucena** position (winning — "build a bridge")
  and the **Philidor** position (drawing defence — rook on the third rank
  until the pawn advances, then check from behind).
- Basic mates: K+Q vs K, K+R vs K (box the king toward the edge).
- In the endgame, the **king is an attacking piece** — centralise it.
- "Rook endgames are always drawn" is a joke with a grain of truth: the
  defending side often holds with active rook play.

## 5. Tournament play
- **Clock:** know the time control (e.g. 90 minutes + 30-second
  increment per move). Budget time: don't spend 20 minutes on move 8.
  Spend time in critical moments (transitions, sharp tactics), move
  quickly in known positions.
- **Notation:** most classical events require writing moves (algebraic
  notation); under FIDE rules you may usually stop recording when under 5
  minutes in games *without* increment (check current rules/arbiter).
- **Touch-move:** a deliberately touched piece must be moved (say
  "j'adoube"/"I adjust" before adjusting).
- Press the clock with the same hand that moved.
- Disputes: stop the clock and call the **arbiter**; don't argue with the
  opponent.
- Phone off and away — carrying a phone in the playing area can be an
  automatic loss.

## 6. Improving
- Analyse every tournament game yourself **before** turning on an engine;
  write your thoughts, then compare.
- Play longer games (15+ minutes) to train thinking; bullet trains habits,
  often bad ones.

## Verify
- [ ] Before each move you asked what the opponent's last move threatened.
- [ ] You can win K+R vs K and set up Lucena and Philidor from memory.
- [ ] You have a named repertoire against 1.e4 and 1.d4.
- [ ] You know the event's time control, notation and phone rules.
