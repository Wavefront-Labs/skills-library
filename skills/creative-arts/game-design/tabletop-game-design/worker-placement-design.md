---
id: creative-arts.game-design.tabletop-game-design.worker-placement-design
name: worker-placement-design
category: creative-arts
field: game-design
product: tabletop-game-design
tags: [game-design, tabletop-game-design, worker-placement, board-game-mechanisms, action-selection, blocking, eurogame, building-blocks]
level: practitioner
status: draft
description: "Design a worker placement system: action spaces and exclusivity, worker count growth, blocking and first-player value, scaling by player count, and the space-value tuning sheet."
sources:
  - https://boardgamegeek.com/boardgamemechanic/2082/worker-placement
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Worker placement design

**Goal:** a worker placement game where every placement is a trade-off between what you
need, what others need, and what you deny them.

Worker placement (BoardGameGeek mechanic; covered in Engelstein and Shalev's *Building
Blocks*): players take turns placing a limited number of workers on action spaces;
typically a space taken by one player is blocked for others that round.

## Core levers
| Lever | Effect |
|---|---|
| Space exclusivity | single-occupancy = blocking and tension; multi-occupancy or paid "bumping" softens it |
| Workers per player | more workers = more actions per round, longer turns |
| Gaining workers | "family growth" creates an engine and a tempo decision |
| Feeding / upkeep | workers cost resources (scarcity pressure) |
| Accumulating spaces | unclaimed spaces grow in value each round (self-balancing) |
| First player marker | an action space to take it; value tuned explicitly |
| Round-by-round new spaces | escalating options and arc |

## Tuning procedure
1. **List every action space** with its output in a common value unit (e.g. convert
   resources to "victory point equivalents" or "actions").
2. **Compare space values**; strongest spaces should have a cost, accumulate slowly, or
   be contested.
3. **Scale by player count:** remove/add spaces or block some at lower counts so
   competition for spaces stays similar.
4. **Track first-pick value:** playtest who takes which space first; a space always
   taken first is too strong (or the first-player space is undervalued).
5. **Check the turn length:** with many workers and options, downtime grows; limit
   options per round.

## Gotchas
- Pure blocking can feel mean and create kingmaking; accumulation and alternatives
  reduce frustration.
- A single "must take" space every round makes turn order decisive; fix with
  accumulation or rotating availability.
- Too many action spaces dilute interaction (no one blocks anyone).

## Verify
- [ ] Space value sheet in a common unit.
- [ ] Space counts scaled per player count.
- [ ] First-pick frequency per space logged across playtests.
- [ ] Average turn time within target.
