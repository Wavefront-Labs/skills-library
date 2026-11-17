---
id: computing-software.game-programming.gameplay-programming.ladder-and-climbing-movement
name: ladder-and-climbing-movement
category: computing-software
field: game-programming
product: gameplay-programming
tags: [gameplay-programming, character-controller, ladder-climbing, climbing, movement-modes, traversal, game-programming]
level: practitioner
status: draft
description: "Implement ladder and climbable-surface movement: entry/exit volumes, snapping to the ladder axis, a dedicated climb movement mode, top/bottom dismounts and edge cases."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Runtime/Engine/GameFramework/UCharacterMovementComponent", "https://docs.godotengine.org/en/stable/tutorials/physics/using_character_body_2d.html", "https://gameprogrammingpatterns.com/state.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Ladder and climbing movement

**Goal:** the player grabs ladders reliably, climbs without jitter, and gets off at either end
without falling or popping through geometry.

## Data
A ladder is a trigger volume plus authored data: `bottom` and `top` points (the climb axis), a
facing direction, and a `topExit` point on the platform above.

## Movement mode
Climbing is its own movement state (not "walking with gravity off"):
```
enter Climb:  velocity = 0; gravity off; snap position onto the axis (lerp over ~0.1 s)
              face the ladder; disable ground snapping and step-up
update Climb: t += input.y * climbSpeed * dt / length(top - bottom)
              position = lerp(bottom, top, clamp(t, 0, 1)) + facingOffset
              if t >= 1 and input.y > 0: dismount top (play climb-over, move to topExit)
              if t <= 0 and input.y < 0: dismount bottom (back to Walk)
              jump pressed: leave with velocity = -facing * pushOff + up * small
exit Climb:   gravity on; restore collision/ground snapping
```
Driving position from a parameter `t` along the axis is what prevents drift and jitter; physics
pushing against the ladder collider causes both.

## Entry rules
- Grab when inside the volume **and** moving toward the ladder (dot(input, facing) > 0.5) or pressing
  up; don't auto-grab when walking past sideways.
- From above: walking off the top edge toward the ladder enters at t = 1 with a climb-down animation.
- Add a short re-grab cooldown after jumping off so the player doesn't instantly re-attach.

## Animation
Drive the climb cycle's playback position from `t * rungs` so hands match rungs; pause animation
when input is zero. Top dismount uses root motion or a scripted curve to `topExit`.

## Engines
- Unreal: `CharacterMovementComponent` custom movement mode (`MOVE_Custom` + `PhysCustom`) or
  `MOVE_Flying` with gravity off; set `bOrientRotationToMovement` off while climbing.
- Godot: a `CLIMB` state in the `CharacterBody3D` state machine; set `velocity` from `t` delta and
  still call `move_and_slide()` so collisions with ceilings stop you.
- Unity CharacterController: disable gravity in your mover and move via `Move` toward the target point.

## Edge cases
- Ladder ends under a ceiling: block climbing up when a capsule cast to the next position hits.
- Getting hit or stunned while climbing: either drop off or play a flinch in place; decide per game.
- Networked: replicate the mode and `t`, not world position, for smooth remote display.

## Verify
- [ ] Grab from bottom, top and mid-air (falling past) all behave as designed.
- [ ] Climb at 30 and 144 fps: same speed, no drift off the axis.
