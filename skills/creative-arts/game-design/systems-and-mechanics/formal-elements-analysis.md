---
id: creative-arts.game-design.systems-and-mechanics.formal-elements-analysis
name: formal-elements-analysis
category: creative-arts
field: game-design
product: systems-and-mechanics
tags: [game-design, formal-elements, fullerton, game-design-workshop, players, objectives, procedures, rules, resources, conflict, boundaries, outcome, game-analysis]
level: intro
status: draft
description: "Break any game into Fullerton's formal elements (players, objectives, procedures, rules, resources, conflict, boundaries, outcome) to analyse it or spec a new design."
sources:
  - https://www.routledge.com/Game-Design-Workshop-A-Playcentric-Approach-to-Creating-Innovative-Games/Fullerton/p/book/9781138098770
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Formal elements analysis

**Goal:** a complete structural description of a game, used either to deconstruct an
existing game or to make sure a new design has no missing pieces.

## The elements (Fullerton, Game Design Workshop ch3)
| Element | Questions |
|---|---|
| **Players** | How many? Invitation to play? Interaction pattern: single vs game, multiple individual vs game, player vs player, unilateral, multilateral, cooperative, team? |
| **Objectives** | Capture, chase, race, alignment, rescue/escape, forbidden act, construction, exploration, solution, outwit? |
| **Procedures** | Starting action, progression of action, special actions, resolving actions. Who does what, where, when, how? |
| **Rules** | Defining objects and concepts, restricting actions, determining effects. |
| **Resources** | Lives, units, health, currency, actions, power-ups, inventory, special terrain, time. What is scarce? |
| **Conflict** | Obstacles, opponents, dilemmas. |
| **Boundaries** | Physical and conceptual edges; what separates the game from not-the-game (the magic circle). |
| **Outcome** | How it ends; is it uncertain until the end; zero-sum or not? |

## Procedure: analysis
1. Play the game (at least twice).
2. Fill one row per element in your own words.
3. Note which element carries the most design weight (Tetris: resources = space, procedures = rotate/drop).
4. Describe the interaction pattern; it predicts the social feel.

## Procedure: spec for a new game
1. Fill the table before writing any rules text.
2. Any blank row is a hole in the design (e.g. no outcome definition = "how do we end?" arguments in playtest).
3. Check that **resources are scarce** - a resource that is never scarce creates no decisions.
4. Check **conflict** exists; without it the objective is a chore.

## Gotchas
- Interaction pattern is often chosen by accident; try alternatives (could this
  competitive game be team-based?) as a cheap ideation move.
- Outcome uncertainty matters (Rules of Play: uncertainty is core to meaningful play). If
  the winner is known early, see `creative-arts.game-design.systems-and-mechanics.feedback-loops-and-catch-up`.
- The formal elements describe structure, not experience; pair with MDA or the tetrad.

## Verify
- [ ] All eight rows filled for the game in question.
- [ ] Every resource listed has a scarcity source.
- [ ] Outcome condition stated unambiguously.
