---
id: creative-arts.game-design.puzzle-design.physics-and-environmental-puzzles
name: physics-and-environmental-puzzles
category: creative-arts
field: game-design
product: puzzle-design
tags: [game-design, puzzle-design, physics-puzzles, environmental-puzzles, systemic-puzzles, emergent-solutions]
level: practitioner
status: draft
description: "Design physics and environmental puzzles: consistent simulation rules, readable affordances, tolerance for alternate solutions, reset handling and preventing soft-locks."
sources:
  - https://www.routledge.com/The-Art-of-Game-Design-A-Book-of-Lenses-Third-Edition/Schell/p/book/9781138632059
  - https://www.gdcvault.com/
  - https://www.routledge.com/An-Architectural-Approach-to-Level-Design-Second-Edition/Totten/p/book/9780815361367
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Physics and environmental puzzles

**Goal:** puzzles solved by manipulating the world's systems (weight, momentum, fire,
water, light), with rules players can predict and creativity the game accepts (Half-Life 2,
Portal, Zelda: Breath of the Wild shrines, Limbo, Inside).

## Principles
1. **Consistent rules:** if wood burns once it always burns; if a crate floats it always
   floats. Players solve by prediction; inconsistency reads as bugs.
2. **Readable affordances:** materials and weights telegraph behaviour visually (metal
   sheen for magnetism, cracked walls for breakable). Teach each property once before testing it.
3. **Accept alternate solutions:** if the physics allows stacking boxes to climb, the
   puzzle allows it, unless it breaks the lesson. Breath of the Wild's shrines are designed
   around multiple valid answers.
4. **Tolerances:** physics outcomes are noisy; give margins (larger pressure plates,
   slightly forgiving trajectories) so correct ideas succeed reliably.
5. **Feedback:** show progress (water level rising, a scale tipping) so players see the
   simulation responding.

## Soft-lock prevention
- Required objects that can be lost (fall off the world, get stuck) must respawn
  at a dispenser or reset point.
- Provide a reset lever, or auto-reset when the puzzle state becomes unsolvable.
- Test with "chaos players" who throw everything everywhere.

## Procedure
1. Prototype in a greybox with physics tuned; build the solution path first.
2. List the intended solution and every alternative found in tests; decide accept or block.
3. Run edge tests: knocking objects off, stacking, using the player as a weight.
4. Tune physics parameters (mass, friction) only in a puzzle-specific way if needed, and
   document it; global changes break other puzzles.

## Gotchas
- Frame-rate-dependent physics changes outcomes on different hardware; use fixed timesteps.
- Physics objects near doors and triggers cause jams; add kill volumes or no-physics zones.
- Puzzles depending on precise physics timing frustrate players who know the answer.

## Verify
- [ ] Intended solution succeeds across 10 repetitions without precise input.
- [ ] Every required object respawns or the puzzle resets.
- [ ] Alternate solutions catalogued and deliberately accepted or blocked.
