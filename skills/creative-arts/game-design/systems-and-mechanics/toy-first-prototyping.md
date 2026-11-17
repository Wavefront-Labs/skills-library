---
id: creative-arts.game-design.systems-and-mechanics.toy-first-prototyping
name: toy-first-prototyping
category: creative-arts
field: game-design
product: systems-and-mechanics
tags: [game-design, toy-prototype, game-prototyping, prototype-iteration, lens-of-the-toy, schell, find-the-fun, sandbox, game-feel]
level: practitioner
status: draft
description: "Build a toy before a game: prototype the core interaction with no goals or rules until it is fun to fiddle with, then layer goals on top (Schell's Lens of the Toy)."
sources:
  - https://www.routledge.com/The-Art-of-Game-Design-A-Book-of-Lenses-Third-Edition/Schell/p/book/9781138632059
  - https://www.routledge.com/Game-Feel-A-Game-Designers-Guide-to-Virtual-Sensation/Swink/p/book/9780123743282
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Toy-first prototyping

**Goal:** find an interaction that is satisfying on its own before you add objectives,
so the game is built on something players enjoy touching.

Schell (Lens of the Toy): "a toy is an object you play with; a game is a toy with rules
and goals." If the toy is not fun, rules rarely rescue it. Swink's Game Feel makes the
same point for real-time control: the moment-to-moment sensation should be pleasant
without any goal.

## Procedure
1. **Pick the core interaction** (throwing, drawing a line, stacking, swinging, tilting).
2. **Build it with zero goals:** an empty room, a few objects, no score, no fail state.
3. **Fiddle-test:** give it to people and say only "play with this". Time how long they
   keep going and watch what they invent.
   - Under ~30 seconds: the toy is not interesting yet. Tune response, feedback, physics.
   - Players invent goals themselves ("can I get it to land on that?"): strong signal;
     those invented goals are your first game design.
4. **Tune for feel** (responsiveness, juice, sound) before adding content; see
   `creative-arts.game-design.systems-and-mechanics.juice-and-feedback-polish`.
5. **Add one goal at a time** and check the toy is still fun with the goal on. Goals that
   force players away from the fun part of the toy are wrong goals.

## Questions from the Lens of the Toy
- If my game had no goal, would it be fun at all? If not, how could I change that?
- When people see my game, do they want to start interacting before they know what to do?

## Gotchas
- Some genres are goal-first (puzzle, strategy) where the "toy" is the system state
  space; there the toy test is "is it interesting to poke the system?".
- Over-polishing a toy that has not been goal-tested can sink weeks; time-box it.
- Toys tested only by the developer always seem fun. Test on others.

## Verify
- [ ] Toy exists without goals and has been played by others.
- [ ] Median unprompted play time recorded.
- [ ] Player-invented goals logged and used as goal candidates.
