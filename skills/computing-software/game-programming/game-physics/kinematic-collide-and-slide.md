---
id: computing-software.game-programming.game-physics.kinematic-collide-and-slide
name: kinematic-collide-and-slide
category: computing-software
field: game-programming
product: game-physics
tags: [game-physics, kinematic, collide-and-slide, character-controller, sweep-test, depenetration, slope-handling, step-up, ground-snapping, game-programming]
level: advanced
status: verified
description: "Implement a kinematic character's collide-and-slide loop: iterative sweeps with skin width, velocity projection on hit planes, crease handling, slopes, step-up and ground snapping."
sources: ["https://www.peroxide.dk/papers/collision/collision.pdf", "https://nvidia-omniverse.github.io/PhysX/physx/5.4.1/docs/CharacterControllers.html", "https://docs.godotengine.org/en/stable/classes/class_characterbody3d.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kinematic collide-and-slide

**Goal:** a capsule that moves exactly as gameplay asks, slides along walls, handles slopes and
stairs, and never ends up inside geometry (Fauerby, "Improved Collision Detection and Response", 2003, is the classic reference;
PhysX's docs describe their character controller's `move()` as a 'collide-and-slide' algorithm; Godot offers `move_and_slide`).

## Core loop
```
remaining = velocity * dt
for i in 0..MAX_ITER (3-5):
    if |remaining| < epsilon: break
    hit = sweep(capsule, position, remaining)          # shape cast
    if not hit:
        position += remaining; break
    move = max(hit.distance - skin, 0)
    position += normalize(remaining) * move
    remaining -= normalize(remaining) * move
    n = hit.normal
    remaining = remaining - n * dot(remaining, n)      # project onto the hit plane (slide)
    velocity  = velocity  - n * min(dot(velocity, n), 0)  # remove into-surface velocity for next frame
    if second hit plane in this frame (crease):
        dir = normalize(cross(n_prev, n))              # slide along the crease line
        remaining = dir * dot(remaining, dir)
```
`skin` keeps the capsule slightly away from surfaces so the next sweep does not start in
contact (Godot's `safe_margin` defaults to 0.001, PhysX uses `contactOffset`; scale it to your units). After the loop, run a **depenetration** pass (overlap query + compute penetration and push out)
to recover from moving platforms or spawned geometry.

## Slopes, steps and ground
- Classify hits by `dot(n, up)`: above `cos(maxSlope)` = walkable floor, else wall. For walls, remove
  the vertical component of the slide so the character cannot climb steep slopes by sliding up them.
- **Step up**: when blocked by a low obstacle, sweep up by stepHeight, forward by the remaining motion,
  then down; accept if landing on walkable ground.
- **Ground snap**: after moving while grounded, sweep down a short distance (e.g. stepHeight) and snap
  if ground is found, so walking down slopes/stairs does not cause tiny falls (bunny hopping); Godot exposes this as `floor_snap_length`.
- Moving platforms: add platform velocity (and rotation delta) before your own movement.

## Gameplay integration
Velocity is owned by gameplay (input, gravity, jumps); the controller resolves collisions and reports
`isGrounded`, ground normal, and hits (for pushing rigid bodies with applied impulses). Kinematic
characters do not get pushed by physics unless you implement it.

## Verify
- [ ] Running diagonally into a wall slides along it at the projected speed; no sticking in corners.
- [ ] Walking down stairs and slopes stays grounded (no air time) with snapping.
- [ ] Spawning inside a box resolves out within one frame (depenetration).

## Checked (2026-10-22)
- Ported the core loop to Python (3D sphere against planes, using the swept-sphere test checked in shape-casts-and-swept-tests), including projection of `remaining` and `velocity` and the crease direction `normalize(cross(n_prev, n))`. 45 degree motion into a wall gives velocity (0, 6, 0) from (6, 6, 0), i.e. the projected speed; sliding into a floor-wall crease for 60 frames never penetrated (asserted) and ended moving along the crease only.
- Fauerby PDF fetched (title, author Kasper Fauerby, 25 July 2003, sliding plane method). PhysX 5.4.1 CharacterControllers page: 'collide-and-slide', sweep tests, skin via contact offset, depenetration with MTD. Godot docs: `move_and_slide`, `floor_snap_length`, `safe_margin` default 0.001.
- Removed the unverified claim that this is 'the algorithm behind' Godot and Unity controllers.
