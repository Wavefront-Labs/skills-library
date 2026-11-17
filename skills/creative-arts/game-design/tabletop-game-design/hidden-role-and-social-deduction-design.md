---
id: creative-arts.game-design.tabletop-game-design.hidden-role-and-social-deduction-design
name: hidden-role-and-social-deduction-design
category: creative-arts
field: game-design
product: tabletop-game-design
tags: [game-design, tabletop-game-design, social-deduction, hidden-role, traitor-mechanics, party-games, deduction-games]
level: practitioner
status: draft
description: "Design hidden-role and social deduction games: team ratios by player count, information leaks, accusation and voting structures, player elimination and moderator load."
sources:
  - https://en.wikipedia.org/wiki/Social_deduction_game
  - https://boardgamegeek.com/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hidden role and social deduction

**Goal:** an informed minority hides among an uninformed majority, and the game supplies
just enough evidence for arguments to be grounded (Mafia / Werewolf, The Resistance,
Secret Hitler, Blood on the Clocktower, Coup).

## Core parameters
1. **Team ratio by player count.** The Resistance uses 2 spies at 5 players rising to 4
   spies at 10, about one third. Informed minorities can be smaller because they coordinate.
2. **Who knows what:** spies know each other (Resistance), one team member is blind
   (Secret Hitler's Hitler at higher counts), special roles see some information (Merlin
   in Avalon knows spies but must stay hidden).
3. **Evidence generators:** mission success/fail cards, policy draws, night kills,
   private role abilities. Without evidence, the game is pure guessing; with too much,
   the minority loses quickly.
4. **Decision structure:** team proposals and votes (Resistance), nomination and execution
   (Werewolf), challenges to claimed roles (Coup).
5. **End conditions:** best of 5 missions, policy tracks, elimination of a side.

## Design levers
| Lever | Effect |
|---|---|
| Player elimination | drama but bored dead players; Resistance removed it entirely; Clocktower lets dead players keep talking and one vote |
| Moderator | Werewolf needs one; app or closed-eyes script can replace |
| Role variety | replayability vs teaching load; use a recommended starter set |
| Round time limit | stops endless discussion |

## Procedure
1. Prototype with playing cards; tune minority size and evidence frequency first.
2. Track win rate per side per player count; aim near 50/50 for experienced groups and
   note new groups usually favour the informed side.
3. Add special roles only once the base is balanced; each role must create a new
   argument, not just new information.

## Gotchas
- Kingmaker or "obvious" patterns from fixed mission sizes; randomise or tune per count.
- Players who never get to talk (introverts, new players): structured turns for speaking help.
- Physical tells in closed-eyes phases: add noise rules (tap the table) or use apps.

## Verify
- [ ] Win rate by side near target at each player count.
- [ ] Dead or idle players still have something to do.
- [ ] Each round produces at least one piece of evidence to argue about.
