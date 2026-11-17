---
id: computing-software.game-programming.unity.physics-materials-friction-and-bounce
name: physics-materials-friction-and-bounce
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-physics, physics-material, friction-combine, bounciness, game-programming]
level: practitioner
status: docs-checked
description: "Tune Unity PhysicsMaterial / PhysicsMaterial2D friction and bounciness, combine modes, and fix characters sticking to walls or objects never coming to rest."
sources: ["https://docs.unity3d.com/Manual/class-PhysicsMaterial.html", "https://docs.unity3d.com/Manual/class-PhysicsMaterial2D.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Physics materials: friction, bounciness and combine modes

**Goal:** surfaces behave as designed (ice, rubber, sticky walls) and common artefacts go away.

## Properties (3D Physics Material)
- **Dynamic Friction** (0 to 1, default 0.6): friction while colliders slide against each other.
- **Static Friction** (0 to 1, default 0.6): friction while colliders are not moving.
- **Bounciness** (default 0): 0 = no bounce, 1 = bounce without losing kinetic energy; the engine's bounce
  approximations can still add small amounts of energy.
- **Friction Combine / Bounce Combine**: both default to Average. Unity combines the values of the two
  touching colliders using this mode; see the manual's "How collider surface values combine".
- With no Physics Material set, a collider uses default surface settings, adjustable in Physics Settings.

2D (Physics Material 2D, `Assets > Create > 2D > Physics Material 2D`) has Friction (0 to 1), Bounciness (0 to 1),
Friction Combine and Bounce Combine (options Average, Mean, Multiply, Minimum, Maximum). Assign it to the Material
property of a Collider 2D or Rigidbody 2D. Check the 2D page for the current defaults.

## Recipes
- **Player sticks to walls while jumping into them**: zero-friction material on the player capsule
  with Friction Combine = Minimum (the smaller value wins); implement ground friction in code.
- **Ice**: friction 0.02, combine Minimum, so the player's material doesn't raise it.
- **Ball that should keep bouncing**: bounciness 0.9, Bounce Combine Maximum. Also check the Bounce
  Threshold in Physics Settings: slower impacts do not bounce.
- **Objects jitter instead of resting**: raise friction, raise Sleep Threshold, check mass ratios.

## Assigning
Drag the material onto a collider, or assign it to the Material property of a Collider 2D or Rigidbody 2D.

## Gotchas
- Bounciness 1 with Maximum combine can accumulate energy from solver error; keep it a little below 1.

## Checked
2026-11-01. Confirmed against the Unity manual pages Physics Material asset reference and Physics Material 2D
reference: property list, 0 to 1 ranges, 3D defaults (friction 0.6, bounciness 0, combine Average), 2D combine
options and asset menu path. Removed: combine priority order, Bounce Threshold figure, PhysicMaterial rename note,
CharacterController and WheelCollider claims, sharedMaterial advice (not on these pages).
Method: documentation only; no commands were run.

## Verify
- [ ] Jump into a wall while holding toward it: player slides down.
- [ ] Drop test: ball bounce heights decay as expected over 5 bounces.
