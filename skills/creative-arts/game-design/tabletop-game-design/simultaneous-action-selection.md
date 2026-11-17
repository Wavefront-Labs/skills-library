---
id: creative-arts.game-design.tabletop-game-design.simultaneous-action-selection
name: simultaneous-action-selection
category: creative-arts
field: game-design
product: tabletop-game-design
tags: [game-design, tabletop-game-design, simultaneous-selection, simultaneous-action-selection, programmed-movement, role-selection, board-games]
level: practitioner
status: draft
description: "Design simultaneous action selection: hidden commit, reveal and resolution order, tie-breaking, information you see before choosing and double-think without paralysis."
sources:
  - https://boardgamegeek.com/browse/boardgamemechanic
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Simultaneous action selection

**Goal:** everyone chooses in secret at the same time, then reveals and resolves, giving
low downtime and mind games (Diplomacy orders, Race for the Galaxy phases, RoboRally
programming, 7 Wonders card play, Citadels-style role guessing).

## Procedure
1. **Commit mechanism:** cards face down, dials, written orders, or a hand-closed token.
   Physical commit must be cheat-proof and quick to reveal.
2. **Reveal together**, then **resolve in a stated order**: initiative numbers on cards,
   turn order, or fixed phase order (Race for the Galaxy resolves chosen phases in
   numeric order; every player takes part in each chosen phase, the chooser gets a bonus).
3. **Collision rules:** what if two players pick the same space or role? Options: both
   fail, both succeed reduced, tie-break by initiative, bump. Write examples for each.
4. **Information before choice:** decide what is public (others' resources, previous
   picks). More visible information gives better reads (yomi) and more thinking time.
5. **Payoff structure:** check for a dominant pick with a payoff matrix; good designs have
   counter-picks (rock-paper-scissors at their core, dressed in theme).

## Programmed movement variant
RoboRally-style: players program several steps ahead, then all execute step by step. The
fun is the chaos when plans collide; keep step count low (5) and resolution clear.

## Pace
- A selection phase should end with a timer or a "last player" rule (sand timer) to stop
  one player stalling everyone.
- Resolution must be fast and mostly mechanical, or simultaneous play loses its benefit.

## Gotchas
- Too many options per selection with a hidden payoff matrix leads to random guessing; 3-7
  options is the workable band.
- Resolution order exceptions accumulate; collect them in a reference card.
- Simultaneous reveal games need a clear "I'm done" signal (card placed face down).

## Verify
- [ ] Payoff matrix shows no strictly dominant choice.
- [ ] Every collision case has a rule and an example.
- [ ] Selection phase timed and capped.
