---
id: creative-arts.game-design.tabletop-game-design.board-layout-design
name: board-layout-design
category: creative-arts
field: game-design
product: tabletop-game-design
tags: [game-design, tabletop-game-design, board-layout, board-design, graphic-design, grid-types, component-design]
level: practitioner
status: draft
description: "Lay out a game board: space type (grid, hex, area, point-to-point), track placement, space sizing for components, orientation for all seats and information hierarchy."
sources:
  - https://www.redblobgames.com/grids/hexagons/
  - https://koboldpress.com/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Board layout

**Goal:** a board that makes legal moves obvious, fits components, reads from every seat
and puts needed information where hands and eyes already are.

## Space types
| Type | Movement | Fits |
|---|---|---|
| Square grid | 4 or 8 neighbours (diagonal distance issue) | tactics, abstracts |
| Hex grid | 6 equal neighbours | wargames, terrain, no diagonal ambiguity |
| Areas (regions) | adjacency by borders | area control (Risk, Small World) |
| Point-to-point | nodes and links | routes, travel (Ticket to Ride, Pandemic) |
| Track | linear path | race and score tracks |

## Layout procedure
1. **List what lives on the board**: map, score track, turn track, market slots, discard,
   reference text. Move anything not needed by everyone to player boards.
2. **Size spaces to the largest component plus finger room**: a standard meeple is about
   16 mm wide; spaces holding several pieces need room for all. Prototype with real pieces.
3. **Score track around the edge**, 0-99 or 0-49 with a "+50" token; check the typical
   final score fits without wrap confusion.
4. **Orientation:** text that every seat reads goes on the player boards; board text
   should be minimal or repeated in multiple orientations.
5. **Visual hierarchy:** high contrast for playable spaces and borders; background art
   lower contrast. Run a greyscale and colour-blind simulation check.
6. **Adjacency clarity:** borders between areas must be unambiguous; add connection lines
   for sea zones or bridges.
7. **Board size:** quad-fold boards are commonly about 18-20 inches (around 45-50 cm) square;
   bigger means a six-fold board and more cost. Check table reach from every seat.

## Modular and variable boards
Modular tiles add replayability but need rules for legal configurations and balance
checks for start positions.

## Gotchas
- Area maps with tiny regions next to big ones mislead about value.
- Art hiding grid lines causes rules disputes.
- Print bleed and fold lines: keep important art and text out of the fold gutter.

## Verify
- [ ] Real components fit every space at maximum stacking.
- [ ] Every seat can read and reach what it needs.
- [ ] Adjacency of every region confirmed by a blind tester.
