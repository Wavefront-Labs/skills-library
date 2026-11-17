---
id: creative-arts.game-design.tabletop-game-design.action-point-allowance-design
name: action-point-allowance-design
category: creative-arts
field: game-design
product: tabletop-game-design
tags: [game-design, tabletop-game-design, action-points, action-point-allowance, turn-structure, board-games, action-economy]
level: practitioner
status: draft
description: "Design action-point allowance turns: AP budget, action menu and costs, carry-over and saving rules, and keeping AP turns from becoming slow optimisation puzzles."
sources:
  - https://boardgamegeek.com/browse/boardgamemechanic
  - https://mitpress.mit.edu/9780262017138/characteristics-of-games/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Action point allowance

**Goal:** a turn where players spend a fixed budget of action points across a menu of
actions, making efficient and interesting trade-offs (Tikal, Pandemic's four actions,
Through the Ages, many skirmish games).

## Design elements
| Element | Options |
|---|---|
| Budget | fixed (4 AP), variable by role or card, growing over the game |
| Menu | each action costs 1+ AP; same action repeatable or once per turn |
| Saving | lose unused AP, bank up to N, convert to a resource |
| Modifiers | cards and powers that make an action cheaper or free |
| Interrupt | reactions on others' turns cost AP from the next turn |

## Procedure
1. **Start with 3-5 AP and 4-6 actions.** More multiplies the search space: 4 AP over 6
   actions with repeats is already 126 combinations of action counts.
2. **Price actions** so the basic move costs 1 and strong effects cost 2-3. Track how
   often each action is chosen in tests; unused actions are overpriced or redundant.
3. **Give a clear default**: players should see a good turn quickly and a great turn with
   thought. Pandemic works because "treat, move, cure" goals are obvious.
4. **Add a reason to vary**: special roles or cards that discount actions break up
   identical turns.
5. **Decide saving rules** early: banking AP adds depth and slows play.

## Downtime control
- AP turns are long; aim for under 2 minutes per turn at the table.
- Let other players plan during the active turn (public information, predictable
  state changes).
- Offer a quick-play variant with fewer AP for new players.

## Gotchas
- Optimal turns that require exact AP arithmetic over many steps cause analysis paralysis.
- Movement per AP on large maps makes the game about pathing; keep distances short or
  provide fast-travel actions.
- A "do anything" free action becomes the only action; cap or cost it.

## Verify
- [ ] Action usage counts show every action used.
- [ ] Average turn time within target at max player count.
- [ ] New players can state a reasonable turn plan within a minute.
