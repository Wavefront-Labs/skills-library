---
id: creative-arts.game-design.tabletop-game-design.trick-taking-game-design
name: trick-taking-game-design
category: creative-arts
field: game-design
product: tabletop-game-design
tags: [game-design, tabletop-game-design, trick-taking, card-games, bidding, trumps, follow-suit]
level: practitioner
status: draft
description: "Design a trick-taking card game: deck and suit structure, follow and trump rules, bidding or contract scoring, card passing and making each trick a decision."
sources:
  - https://en.wikipedia.org/wiki/Trick-taking_game
  - https://www.pagat.com/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Trick-taking game design

**Goal:** a game where each card played is a decision, constrained just enough by the
rules to create inference, and scored so that winning tricks is not always good.

## Core rules to decide
| Decision | Common options |
|---|---|
| Deck | 52 standard, 4 suits x 13; custom (The Crew 4 x 9 plus rockets; Tichu adds 4 specials) |
| Follow rule | must follow suit if able (creates information); must-not-follow variants exist |
| Trumps | fixed trump suit, trump chosen by bid winner, no trumps, changing trumps per hand |
| Lead | winner of last trick leads |
| Scoring | per trick (Spades), point cards (Hearts: hearts and the queen of spades), exact bid (Oh Hell), contract (Bridge) |
| Partnership | fixed partners, hidden partners, solo |
| Pre-play | bidding, card passing (Hearts passes 3), drafting |

## Making it interesting
1. **Exact-bid or avoid-trick scoring** makes losing tricks valuable; "win as many as
   possible" alone is often shallow.
2. **Information from the follow rule:** a player who fails to follow reveals a void.
   Inference is the skill of the genre; avoid rules that remove it.
3. **Hand evaluation phase:** a bid or pass forces players to read their hand before play.
4. **Twist mechanisms** used by modern designs: The Crew's cooperative tasks and limited
   communication, Tichu's bombs and combinations, The Fox in the Forest's odd-card powers
   for two players.
5. **Two-player** trick-takers need a reason to care about every trick (Fox in the Forest
   scores by trick count bands, punishing greed).

## Procedure
1. Prototype with a standard deck and paper scoring; most rules are testable this way.
2. Count deck size vs players: deal all cards for fullest information, or hold some out to add uncertainty.
3. Play 20+ hands; log trick winners and scores. Look for hands decided by the deal alone.
4. Tune scoring so a strong hand and a weak hand both have interesting goals.

## Gotchas
- Too many special cards hide the core inference; keep powers rare.
- Long hands with obvious late tricks: allow claiming the remaining tricks when certain.
- Partnership communication rules must be explicit (no table talk vs limited signals).

## Verify
- [ ] Strong and weak hands both have a scoring goal.
- [ ] Follow/void inference matters in tested hands.
- [ ] Deal-decided hands under a small share of logged hands.
