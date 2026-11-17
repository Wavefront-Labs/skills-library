---
id: creative-arts.game-design.systems-and-mechanics.designing-game-space
name: designing-game-space
category: creative-arts
field: game-design
product: systems-and-mechanics
tags: [game-design, game-space, schell-mechanics, game-mechanics-basics, discrete-space, continuous-space, nested-space, grid, hex-grid, board-design, abstraction]
level: practitioner
status: draft
description: "Define a game's functional space (discrete vs continuous, dimensions, bounded areas, nested spaces) per Schell's mechanics chapter, before any art or level layout."
sources:
  - https://www.routledge.com/The-Art-of-Game-Design-A-Book-of-Lenses-Third-Edition/Schell/p/book/9781138632059
  - https://www.redblobgames.com/grids/hexagons/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Designing game space

**Goal:** a clear, abstract model of the space the game takes place in, so rules about
movement, adjacency and range are unambiguous and the space's shape creates decisions.

Schell (2nd ed.) ch12 treats space as the first mechanic: strip away the visuals and describe the
*functional space* - a mathematical construct of places and connections.

## Three properties to decide
1. **Discrete or continuous.** Tic-tac-toe has 9 discrete places; billiards is a
   continuous 2D plane. Many games mix: a continuous 3D world with discrete rooms that
   matter to rules.
2. **Number of dimensions.** 0D (a question-and-answer game has no space), 1D (a race
   track as a track position), 2D, 3D.
3. **Bounded areas, connected or not.** Rooms, zones, regions; and how they connect
   (adjacency graph).
Also: **nested spaces** - a world map containing towns containing buildings, each with
its own space rules (Schell's example: overworld vs dungeon interior).

## Procedure
1. Draw the functional space as a graph or grid, no art.
2. For discrete space, choose the topology:
   | Topology | Use when | Watch for |
   |---|---|---|
   | square grid | simple counting, buildings | diagonal distance ambiguity: decide 1, 1.5 or 2 |
   | hex grid | movement and ranges should be uniform | coordinate systems (Red Blob Games' hex guide covers cube/axial coords) |
   | area/zone map | strategic games, theatre-of-mind | adjacency must be marked clearly |
   | point-to-point | routes, rails, pointcrawls | number of connections per node controls choice |
3. Define distance and line of sight rules in that topology.
4. Check that the **shape creates decisions**: chokepoints, central vs edge positions,
   shortcuts, safe zones.
5. For nested spaces, specify what transfers between levels (time, resources, state).

## Gotchas
- Square-grid diagonals are the classic rules hole; D&D 5e's default treats diagonals
  as 5 ft, with an optional variant alternating 5/10 ft. Pick and state it.
- Continuous space in tabletop needs measurement tools and tolerances (wargame rulers,
  "measure from base edge").
- A space with no constrained areas (all positions equivalent) generates no positional
  decisions.

## Verify
- [ ] Functional space drawn without art.
- [ ] Discrete/continuous, dimensions and areas stated.
- [ ] Distance, adjacency and line-of-sight unambiguous.
- [ ] At least three positions with different strategic value identified.
