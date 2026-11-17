---
id: creative-arts.animation.blender.particle-boids
name: particle-boids
category: creative-arts
field: animation
product: blender
tags: [blender, particles, particle-boids, boids, flocking, crowds]
level: practitioner
status: docs-checked
description: "Simulate flocks and swarms with Blender boid particles: movement settings, the Boid Brain rules and rule evaluation modes, relations, battle settings and baking."
sources:
  - https://docs.blender.org/manual/en/latest/physics/particles/emitter/physics/boids.html
  - https://docs.blender.org/manual/en/latest/physics/baking.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---
# particle-boids

## Setup

Emitter particle system, Particle System > Physics > Type **Boids**. Boids are controlled by a limited artificial intelligence that follows rules; the manual lists flocks, swarms, herds, schools and predator-versus-prey as typical uses.

## Movement (Physics > Movement)

- **Allow Flight**, **Allow Land**, **Allow Climbing** (climbing toward goal objects).
- Air: Max Air Speed, Min Air Speed, Max Air Acceleration and Max Air Angular Velocity (percentages), Air Personal Space, Landing Smoothness.
- Land: Max Land Speed, Jump Speed, Max Land Acceleration, Max Land Angular Velocity, Land Personal Space, Land Stick Force.
- **Collision Collection** limits which objects boids collide with. Boids avoid objects that have Collision enabled.
- Misc panel: **Banking** (1.0 gives a natural banking effect), **Pitch**, **Height**. Battle panel: Health, Strength, Aggression, Accuracy, Range.

## Boid Brain rules

The rule list is parsed top to bottom (reorder with the arrow buttons), and only a limited number of rules can be evaluated: when the memory is exceeded the remaining rules are ignored, so order matters. Each rule can apply In Air and/or On Land.

**Rule Evaluation**: Average (all rules averaged), Random (a random rule per boid), Fuzzy (uses fuzzy logic with a Rule Fuzziness threshold; only the first rule above the threshold is evaluated).

Rules: **Goal** (seek an object, with Predict), **Avoid** (flee from an object, with Predict and Fear Factor), **Avoid Collision** (Boids, Deflectors, Look Ahead), **Separate**, **Flock**, **Follow Leader** (Distance, Line and Queue Size), **Average Speed** (Speed, Wander, Level), **Fight** (Fight Distance, Flee Distance).

Without an Object set, Goal uses Boid force fields with negative Strength, and Avoid uses Boid force fields with positive Strength (predators).

## Relations

The Relations panel lists other particle systems (Target Object and System index) with a Mode: Enemy (fight), Friend (work together) or Neutral.

## Recipe: fish school (starting point)

Volume emitter, Allow Flight on, rules Separate, Flock and Goal (an empty animated on a path), plus Avoid Collision with tank walls that have Collision enabled. Tune counts and speeds by eye.

## Gotchas

- Walls and obstacles must have Collision (deflection) enabled for boids to avoid them.
- The manual recommends baking physics simulations before rendering so results stay identical (see cache-step).

## Verify

Playback shows a coherent flock following the goal while keeping spacing, and no boid leaves the collision volume.

## Checked

Date 2026-10-27. Blender manual 5.2 (blender-v5.2-release RST).
Confirmed: Movement, Battle, Misc, Relations and Boid Brain panel contents, the rule list and their options, Rule Evaluation modes, Boid force field behaviour, the baking recommendation.
Removed as unconfirmed: "Rotation Dynamic" for facing, 200 particles and gravity-off recipe numbers, "gravity still applies with flight on", and "boids are frame dependent".
Method: documentation only; no commands were run.
