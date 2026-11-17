---
id: sports-recreation.mind-sports-and-games.poker.ranges-gto-basics-and-tournament-icm
name: ranges-gto-basics-and-tournament-icm
category: sports-recreation
field: mind-sports-and-games
product: poker
tags: [poker, texas-holdem, no-limit-holdem, nlhe, plo, hand-ranges, preflop-ranges, position, pot-odds, equity, implied-odds, expected-value, ev, gto, game-theory-optimal, exploitative-play, solver, c-bet, bet-sizing, bluffing, value-betting, mdf, minimum-defence-frequency, icm, bubble, push-fold, tournament-strategy, cash-games, bankroll-management, variance, tells, hud]
level: practitioner
status: draft
description: "Poker as a skill game: thinking in ranges, position and pot odds, GTO fundamentals vs exploitative adjustments, bet sizing, tournament ICM and push-fold play, and bankroll management."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Poker — ranges, GTO basics and tournament ICM

**Goal:** make better decisions in no-limit hold'em (NLHE) by reasoning
about ranges and expected value rather than single hands, and adapt
between cash games and tournaments. Treat poker money as entertainment
money and play only where it's legal; for wagering as gambling see
`sports-recreation.gambling-and-wagering` skills.

## 1. Think in ranges
- Opponents hold a **range** (all hands they'd play this way), not one
  hand. Narrow it street by street from their actions and position.
- Your own actions should come from a range too — balanced so you're not
  readable.
- **Preflop:** play tighter from early position, wider from the button
  (last to act post-flop is a big advantage). Use a published or
  solver-derived **opening chart** per position as a starting point.

## 2. Odds and EV
- **Pot odds:** call amount ÷ (pot after your call). Calling 50 into a
  pot of 100 (+ their 50 bet = 150 before your call): 50 / 200 = 25% —
  you need at least 25% equity to call profitably (ignoring future bets).
- **Outs → equity:** rule of 2 and 4 — outs × 2 ≈ % to hit on the next
  card; outs × 4 ≈ % by the river with two cards to come (overestimates
  slightly with many outs). A flush draw (9 outs) ≈ 35% by the river.
- **Implied odds:** extra you'll win when you hit; matters for draws and
  small pairs set-mining (needs deep stacks).
- **EV:** sum of (probability × result) across outcomes; decisions, not
  results, are what you evaluate.

## 3. GTO vs exploitative
- **GTO (game-theory optimal):** a strategy that can't be exploited;
  solvers (e.g. PioSOLVER, GTO Wizard — commercial) compute approximations.
  Useful principles: **minimum defence frequency** — facing a pot-sized
  bet, you must continue with about 50% of your range or the bettor
  profits by bluffing any two cards; **bluff-to-value ratio** depends on
  bet size (bigger bets → more bluffs allowed).
- **Exploitative play:** deviate where opponents are imbalanced — value
  bet thinner and bluff less against calling stations; bluff more against
  players who fold too often.
- Most low-stakes profit comes from exploiting, but a GTO baseline stops
  you being exploited.

## 4. Post-flop basics
- **C-bet** (continuation bet) more on boards that favour your range (high
  cards as preflop raiser), less on low connected boards.
- **Sizing:** small bets on dry boards, larger on wet boards; polarised
  (very strong or bluff) ranges use big sizes.
- Have a reason for each bet: value (worse hands call) or bluff (better
  hands fold). "Information bets" usually aren't.

## 5. Tournaments and ICM
- **ICM (Independent Chip Model):** chips ≠ money; losing chips costs more
  than winning chips gains near pay jumps. Near the **bubble** and final
  table, call shoves tighter; big stacks pressure medium stacks.
- **Short stacks (≈10-15 big blinds or less):** switch to **push-fold**
  (all-in or fold) using push/fold charts.
- Antes widen profitable stealing ranges.

## 6. Bankroll and mindset
- Common guidance: 20-50+ buy-ins for cash games, far more for MTTs
  (huge variance). Move down after a set drawdown.
- **Tilt control:** set stop-loss/time limits; quit after a bad beat if
  you feel it.
- Review hands away from the table; a hand-history tracker helps where
  site rules permit (some sites ban HUDs).

## Gotchas
- Judging decisions by results (a good call that loses is still good).
- Calling with draws without pot odds or implied odds.
- Ignoring ICM: busting with a marginal call on the bubble.

## Verify
- [ ] You can state the pot odds and your equity for any call you made.
- [ ] Your preflop opens follow a position chart.
- [ ] At a pay jump you considered ICM before calling an all-in.
- [ ] You have a written bankroll rule and stop-loss.
