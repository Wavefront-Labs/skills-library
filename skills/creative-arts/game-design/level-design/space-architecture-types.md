---
id: creative-arts.game-design.level-design.space-architecture-types
name: space-architecture-types
category: creative-arts
field: game-design
product: level-design
tags: [game-design, level-design, space-architecture, game-space, open-world, level-structure, schell-lenses]
level: practitioner
status: draft
description: "Pick a game-space architecture (linear, grid, web, points in space, divided space) per Schell and use it to organise open worlds and levels."
sources:
  - https://www.routledge.com/The-Art-of-Game-Design-A-Book-of-Lenses-Third-Edition/Schell/p/book/9781138632059
  - https://www.routledge.com/An-Architectural-Approach-to-Level-Design-Second-Edition/Totten/p/book/9780815361367
  - https://www.gamedeveloper.com/design/the-architecture-of-game-spaces
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Space architecture types

**Goal:** choose the skeleton of your game space on purpose, before content.

Schell (Spaces chapter) names organising principles for game spaces:

| Type | Shape | Good for | Examples |
|---|---|---|---|
| Linear | a line, maybe with branches back | authored pacing, story | Candy Land, side-scrollers |
| Grid | regular cells | tactics, easy measurement | chess, Civilization tiles |
| Web | important points connected by paths | hubs, metroidvania maps | Zelda dungeon maps, Mario World map |
| Points in space | locations in a continuous space, the player chooses paths | open worlds, sandboxes | Breath of the Wild landmarks |
| Divided space | a space cut into regions of varying size | territory and area control | Risk, regional maps |

## Steps
1. Choose from your core verbs: precise tactics need a grid; free exploration suits
   points in space; tight story suits linear or web.
2. Combine scales: an open world (points in space) containing linear dungeons and a web
   of roads.
3. Draw the abstract structure first (graph of nodes and edges), then the physical map.
4. Ask the Lens of the Functional Space questions: what is the space really shaped
   like, is it discrete or continuous, how many dimensions, where are the boundaries,
   and does it support the essential experience?
5. Size relationships: use landmarks and distances in travel time, not metres.

## Gotchas
- Points in space without dense, well-spaced points feel empty; plan POI density.
- Grids constrain art; hide them under organic visuals when needed.
- Webs with too many links lose meaning; keep junctions readable.

## Verify
- [ ] Architecture chosen and justified by core verbs.
- [ ] Abstract graph drawn before the physical map.
- [ ] Nested scales defined (world, region, level).
