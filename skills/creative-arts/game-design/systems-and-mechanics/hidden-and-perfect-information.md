---
id: creative-arts.game-design.systems-and-mechanics.hidden-and-perfect-information
name: hidden-and-perfect-information
category: creative-arts
field: game-design
product: systems-and-mechanics
tags: [game-design, hidden-information, perfect-information, imperfect-information, fog-of-war, bluffing, deduction, meaningful-choice, rules-of-play, information-design]
level: practitioner
status: draft
description: "Decide what each player knows: perfect vs imperfect information, private hands, fog of war, hidden scoring, and how information structure shapes bluffing, deduction and analysis paralysis."
sources:
  - https://mitpress.mit.edu/9780262240451/rules-of-play/
  - https://www.routledge.com/The-Art-of-Game-Design-A-Book-of-Lenses-Third-Edition/Schell/p/book/9781138632059
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hidden and perfect information

**Goal:** an information structure (who knows what, when) chosen on purpose, because it
determines whether play is about calculation, deduction, bluffing or memory.

Rules of Play (ch17 Games as Information Systems) distinguishes **perfect information**
(all players know the full game state: chess, Go) from **imperfect information** (some
state hidden: poker hands, fog of war). Schell (2nd ed.) ch12 asks for each attribute: known to
all, to some, to the game only, or to no one (random).

## Effects of each choice
| Structure | Produces | Risks |
|---|---|---|
| Perfect information | deep calculation, skill expression | analysis paralysis, solvable lines, kingmaking |
| Private info (hands, roles) | bluffing, reading opponents | table talk disputes |
| Hidden from all (face-down deck) | surprise, risk management | luck perception |
| Fog of war / scouting | exploration, intelligence as a resource | frustration if unscoutable |
| Hidden scoring | prevents leader-bashing, keeps all players engaged | anticlimactic reveals |
| Memory-based (revealed then hidden) | memory skill | punishing for some players; rules arguments |

## Procedure
1. Make an **information table**: each state element x who can see it.
2. Ask what decision each hidden element creates. Hidden information without a decision
   about it (deduction, scouting, bluffing) is just noise.
3. Provide **ways to gain information** (scouting units, peek abilities, deduction clues)
   so information becomes a resource.
4. For perfect-information games, limit branching (fewer options per turn) to cap
   analysis paralysis.
5. For tabletop, specify **what is open information** in the rulebook (can players count
   the discard pile? can you show your hand?). Ambiguity here causes table disputes.

## Gotchas
- Digital games can hide information that tabletop cannot enforce; tabletop hidden
  info relies on honour and physical design (screens, card backs that are identical).
- "Open information but tedious to track" (counting cards in a discard) rewards
  memorisers; either make it truly open (face-up) or truly hidden.
- Hidden-traitor and deduction games need enough clues to make deduction possible; test
  how often the hidden side is found by luck vs logic.

## Verify
- [ ] Information table complete.
- [ ] Every hidden element linked to a decision it creates.
- [ ] Rulebook (or UI) states unambiguously what is public.
