---
id: computing-software.game-programming.gameplay-programming.wall-jump-dash-and-ledge-grab
name: wall-jump-dash-and-ledge-grab
category: computing-software
field: game-programming
product: gameplay-programming
tags: [gameplay-programming, character-controller, wall-jump, ledge-grab, dash, wall-slide, platformer, movement-abilities, state-machine, game-programming]
level: practitioner
status: draft
description: "Implement platformer movement abilities: wall detection, wall slide and wall jump with input lockout, dash with fixed duration, and ledge grab/climb detection with shape casts."
sources: ["https://maddymakesgames.com/articles/celeste_and_towerfall_physics/index.html", "https://github.com/NoelFB/Celeste/blob/master/Source/Player/Player.cs", "https://www.gdcvault.com/play/1023559/Math-for-Game-Programmers-Building"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Wall jump, dash and ledge grab

**Goal:** advanced platformer moves that feel fair: they trigger when the player expects, and do not
fight the regular controller. (Celeste's open-sourced Player.cs is a good reference implementation.)

## Structure
Implement as states of the character state machine (Normal, WallSlide, Dash, LedgeHang, Climb) with
explicit entry conditions and exits; each state owns its movement rules for its duration.

## Wall detection
Cast the collider shape (or two short rays at chest and knee height) a few pixels/centimetres left and
right each frame: `onWallLeft`, `onWallRight`, plus wall normal. Require the player to be airborne.
Add **wall coyote time** (~0.1 s) like ground coyote time so a jump just after leaving the wall still
counts.

## Wall slide and wall jump
```
WallSlide: if airborne and onWall and input toward wall and velocity.y < 0:
    velocity.y = max(velocity.y, -wallSlideMaxFall)       # slower fall
WallJump (jump pressed while onWall or within wall coyote):
    velocity = (wallNormal.x * wallJumpHorizontal, wallJumpVertical)
    lock horizontal input toward the wall for ~0.1-0.2 s   # prevents immediately re-sticking
    face away from wall
```
Variants: neutral wall jump (no input: smaller horizontal push, can climb same wall), wall-climb jumps.
The input lockout (or reduced air control briefly) is the key to wall jumps feeling good.

## Dash
```
on dash pressed and dashesLeft > 0:
    dir = input8 (or facing if none); dashesLeft -= 1
    state = Dash; timer = 0.15 s; velocity = dir * dashSpeed; gravity off
during Dash: ignore input movement; optional trail/afterimages
end: velocity *= endMultiplier (keep some momentum); gravity on
refill dashesLeft on landing (and on special pickups)
```
Freeze-frames of 2-3 frames at dash start sell the impact. Optional invulnerability frames.

## Ledge grab
Conditions (airborne, moving down or slow up, facing the wall):
- Upper ray/box cast in front of the head finds **no** wall, lower cast at chest finds a wall ->
  there is a ledge between.
- Downward cast from above the ledge finds the ledge top; check headroom for standing there (shape cast).
Snap the character to a hang position relative to the ledge corner (exact offset so hands align with
animation), zero velocity, state LedgeHang. Climb: play animation (root motion or scripted tween) to
the standing position; Drop: release with input down.

## Verify
- [ ] Wall jump away from a wall never re-sticks immediately; climbing between two walls works.
- [ ] Dash distance is constant regardless of frame rate.
- [ ] Ledge grab only triggers at real ledges with headroom; hands align with geometry.
