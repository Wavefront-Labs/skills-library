---
id: creative-arts.game-design.tabletop-game-design.deck-building-design
name: deck-building-design
category: creative-arts
field: game-design
product: tabletop-game-design
tags: [game-design, tabletop-game-design, deck-building, board-game-mechanisms, market-row, card-trashing, starting-deck, engine-building, deckbuilder]
level: practitioner
status: draft
description: "Design a deck-building game: starting deck, market structure, cost curve, trashing and deck thinning, shuffle timing, and win conditions that stop runaway engines."
sources:
  - https://boardgamegeek.com/boardgamemechanic/2664/deck-bag-and-pool-building
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deck-building design

**Goal:** a deck-builder where each purchase is a decision about the deck's future
draws, with a market that stays interesting and an ending that arrives on time.

In deck-building (popularised by Dominion), each player starts with a small, weak deck
and acquires cards during play; the deck is reshuffled when exhausted, so purchases
change future hands.

## Design levers
| Lever | Notes |
|---|---|
| Starting deck | size (often ~10) and composition (basic currency/attack cards) |
| Market | fixed supply piles (Dominion-style, full information) vs a rotating market row (more variance) |
| Cost curve | cost vs power across the card pool (see cost-curve skills) |
| Trashing | removing weak cards concentrates the deck; strong but slow |
| Draw | +cards effects increase hand size; key engine pieces |
| Victory cards | cards that score but clog the deck (Dominion's elegant tension) |
| Game end | pile depletion, VP threshold, round limit |

## Procedure
1. Use the hypergeometric/shuffle maths to estimate how often a bought card is seen:
   a 12-card deck with a 5-card hand cycles roughly every 2-3 turns; see
   `creative-arts.game-design.systems-and-mechanics.card-draw-odds-hypergeometric`.
2. Price cards on a cost curve; mark the strongest per cost and test in isolation.
3. Test **"big money" baseline** (buy only the best currency and victory cards): the
   game must reward engines and interaction enough to beat it, but not by a mile.
4. Check **game length:** pile-out or VP triggers should end games before engines go
   infinite; tune victory card availability.
5. For market rows, analyse **swinginess** (a strong card appearing for the next player).

## Gotchas
- Infinite combos are fun once; cap or end games before they dominate.
- Shuffle-heavy games add physical time; digital versions or fewer shuffles help.
- Too many card text effects per turn slow play; keep turn complexity in check.

## Verify
- [ ] Starting deck and market structure documented.
- [ ] Big-money baseline beaten by engine strategies at a reasonable but not overwhelming rate.
- [ ] Average game length within target.
- [ ] No infinite combo without an end condition.
