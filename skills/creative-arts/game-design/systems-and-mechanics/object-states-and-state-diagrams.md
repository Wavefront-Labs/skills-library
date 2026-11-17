---
id: creative-arts.game-design.systems-and-mechanics.object-states-and-state-diagrams
name: object-states-and-state-diagrams
category: creative-arts
field: game-design
product: systems-and-mechanics
tags: [game-design, object-states, state-diagram-design, attributes, state-machine, schell-mechanics, game-mechanics-basics, secrets, public-information, specification]
level: practitioner
status: draft
description: "Specify game objects by attributes and states, draw a state diagram per object with transitions and triggers, and decide who knows each attribute (public, private, hidden)."
sources:
  - https://www.routledge.com/The-Art-of-Game-Design-A-Book-of-Lenses-Third-Edition/Schell/p/book/9781138632059
  - https://gameprogrammingpatterns.com/state.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Object states and state diagrams

**Goal:** every object in the game is specified by its attributes and states, with
explicit transitions, so rules are complete and implementers or players never guess.

Schell (2nd ed.) ch12: objects have **attributes** (categories of information: max speed, colour)
and each attribute has a **state** (current value). Some attributes are static, some
dynamic. State diagrams show the allowed states and the events that move between them.

## Procedure
1. **List objects:** characters, items, tiles, cards, doors, the game itself.
2. **List attributes per object** and mark each static or dynamic.
3. **For important dynamic attributes, draw a state diagram:**
   ```
   GUARD: Patrolling --(sees player)--> Alert --(loses sight 5s)--> Searching
          Searching --(timer 20s)--> Patrolling
          Alert --(player in range)--> Attacking --(player hidden)--> Searching
          any --(hit by takedown from behind)--> Unconscious
   ```
   Check every state has an exit (or is intentionally terminal) and every event in
   every state is handled (what does a sleeping guard do when hit?).
4. **Decide visibility** for each attribute (Schell: who knows what):
   | Attribute | Known to all | Known to owner | Known to game only | Known to none (random) |
   Hidden information is a key design lever (see
   `creative-arts.game-design.systems-and-mechanics.hidden-and-perfect-information`).
5. **Show state to the player** where it matters: a guard's state must be readable
   (icons, posture, audio barks).

## Gotchas
- **Unhandled event-in-state** combinations are the source of most rules disputes
  (tabletop) and design bugs (digital). A state x event table catches them.
- Too many states per object becomes unreadable for players; if a player cannot tell
  the states apart, merge them.
- Persistent states (a door left open stays open) need save-system decisions.

## Verify
- [ ] Attribute list per object, static/dynamic marked.
- [ ] State diagrams for every object with 3+ states.
- [ ] State x event table has no blank cells for core objects.
- [ ] Visibility decided for each attribute; player-relevant states are readable.
