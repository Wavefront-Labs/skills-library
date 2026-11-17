---
id: creative-arts.game-design.tabletop-game-design.set-collection-and-tile-placement
name: set-collection-and-tile-placement
category: creative-arts
field: game-design
product: tabletop-game-design
tags: [game-design, tabletop-game-design, set-collection, tile-placement, scoring-curves, board-games, tile-laying]
level: practitioner
status: draft
description: "Design set-collection and tile-placement mechanisms: scoring curves for sets, tile mix and edge rules, placement constraints and keeping the draw from deciding the game."
sources:
  - https://boardgamegeek.com/browse/boardgamemechanic
  - https://mitpress.mit.edu/9780262017138/characteristics-of-games/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Set collection and tile placement

**Goal:** collection and placement decisions that are clear on the turn, interesting over
the game, and not dominated by luck of the draw.

## Set collection
**Scoring shapes** (Engelstein and Shalev catalogue these):
| Shape | Example | Effect |
|---|---|---|
| Linear per item | 1 VP each | no reason to specialise |
| Escalating (triangular 1,3,6,10,15) | Ticket to Ride route lengths, many set games | rewards committing; punishes splitting |
| Set-of-different | Sushi Go sashimi, 7 Wonders science (n squared plus 7 per full set) | rewards breadth |
| Threshold / majority | most of a colour scores | creates interaction and hate-drafting |
| Negative until committed | Lost Cities expeditions start at -20 | forces decisive commitment |

Design levers: how many of each type exist (supply caps), how visible others' sets are,
and whether a card can count in more than one set. Count the deck: if 14 of each suit
exist and 4 players chase 2 suits, collisions are guaranteed; tune on purpose.

## Tile placement
1. **Placement rule:** edge matching (Carcassonne), adjacency to own tiles
   (Kingdomino's 5x5 grid), or free placement with scoring patterns (Cascadia).
2. **Tile mix:** list every tile with its edges/features in a sheet; count how many tiles
   complete each feature type. Rare closing tiles create the tension (and frustration).
3. **Choice window:** a market of 3-4 tiles beats blind single draw; Kingdomino's
   pick order (better tile now, later pick next round) is a self-balancing draft.
4. **Unplaceable tiles:** define the rule (discard and redraw) explicitly.
5. **Scoring timing:** on completion (immediate feedback) vs end-game (planning, slower teaching).

## Procedure
1. Spreadsheet the component list and expected set completion rates.
2. Simulate random-draw outcomes (or hand-shuffle 20 games) to check how often sets fail.
3. Give a mitigation for bad draws: market, reserve slot, swap action.

## Gotchas
- Escalating set scores plus hidden collections invite a runaway leader nobody can see.
- Tile games with one feature type dominating scoring collapse to one strategy.
- Small tile art loses features at table distance; test edges at arm's length.

## Verify
- [ ] Component sheet with counts per set type or edge type.
- [ ] Set completion rates measured and in the intended band.
- [ ] A bad-draw mitigation exists.
