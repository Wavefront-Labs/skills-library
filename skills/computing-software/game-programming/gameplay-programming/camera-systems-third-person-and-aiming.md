---
id: computing-software.game-programming.gameplay-programming.camera-systems-third-person-and-aiming
name: camera-systems-third-person-and-aiming
category: computing-software
field: game-programming
product: gameplay-programming
tags: [gameplay-programming, third-person-camera, camera-collision, spring-arm, camera-smoothing, aim-assist, framing, dead-zone, camera-shake, fov, follow-camera, cinemachine, spring-arm-component, game-programming]
level: practitioner
status: draft
description: "Build a third-person follow/aim camera with collision avoidance and smoothing that reads as responsive, not laggy or fighting the player's own input."
sources: ["https://docs.unity3d.com/Packages/com.unity.cinemachine@latest", "https://dev.epicgames.com/documentation/en-us/unreal-engine/spring-arm-component-in-unreal-engine"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Third-person camera systems and aiming

**Goal:** a follow camera that stays behind the character through geometry,
frames the action well, and smooths motion without ever feeling like it's
lagging behind or fighting the player's own camera input — the three things
that make third-person cameras hard are collision, smoothing, and whose input
wins when.

## Collision: the spring arm pattern
A naive fixed offset behind the character clips through walls the moment the
character backs into a corner. The standard fix (Unreal's SpringArmComponent,
Unity Cinemachine's camera collider extension, or a hand-rolled version) is a
**sphere/capsule cast from the pivot (usually near the character's head/chest)
toward the desired camera position** every frame; if the cast hits geometry
before reaching the target distance, pull the camera in to the hit point minus
a small skin margin. Pulling in should happen instantly (no smoothing lag —
clipping through a wall for even a few frames looks broken), while pulling
back out once clear of the obstruction should smooth back over a short window
(snapping straight back out reads as a jarring pop the instant the obstruction
clears).

## Smoothing: damping, not a flat lerp
`Lerp(currentPos, targetPos, t)` every frame with a fixed `t` produces
frame-rate-dependent behavior (different convergence speed at 30 vs 144 fps)
and overshoots/lags inconsistently. Use a frame-rate-independent
exponential/critically-damped approach instead:
`current = Lerp(current, target, 1 - exp(-speed * deltaTime))` or a proper
spring-damper (position + velocity state, as in Unity's
`SmoothDamp`/Cinemachine's damping, or a custom critically-damped spring) —
these converge to the same visual speed regardless of frame rate and don't
overshoot and oscillate the way an underdamped naive lerp can. Separate
damping values for position vs rotation (rotation often wants to feel snappier
— a camera that smooths its look-direction as slowly as its position feels
disconnected from player aim input) and for different axes (vertical follow
often wants more lag than horizontal, so the camera doesn't bob with every
small jump).

## Framing and aim-assist
- **Over-the-shoulder offset** (camera pivot shifted laterally, not centered
  on the character) reads as more cinematic/aim-focused than dead-center, and
  is near-universal in third-person shooters — but the offset must flip or
  adjust near walls on the offset side (standing against a wall on the camera's
  offset side otherwise either clips or forces an awkward angle).
- **Aim-assist framing** (subtly adjusting FOV, offset, or crosshair reticle
  magnetism toward a nearby target while aiming) is a design decision with real
  competitive-fairness weight in PvP — document and playtest it explicitly
  rather than letting it emerge as a side effect of camera-smoothing code; it
  should be tunable/disableable, not baked permanently into the camera rig.
- **Dead zones** on camera-look input (ignore small stick/mouse deltas near
  zero) prevent camera micro-jitter from analog stick noise, same principle as
  the input dead zone in
  `computing-software.game-programming.gameplay-programming.character-controller-and-game-feel`'s
  input handling, applied to look input specifically.

## Whose input wins — player look vs scripted camera
A common bug class: a scripted camera event (a cutscene look-at, an auto-
target-lock) and the player's manual camera input both trying to drive camera
rotation the same frame, producing a fight (the camera visibly stutters
between the two targets). Resolve with an explicit priority/blend system — a
scripted override either fully owns the camera for its duration (player input
ignored, clearly signaled) or blends in as a weighted influence the player can
still override by moving the stick past a threshold — never let both write to
the same transform unconditionally in the same frame.

## Verify
- [ ] Camera never visibly clips through geometry when backing into a corner;
      pull-in is instant, pull-out-after-clear is smoothed.
- [ ] Position/rotation smoothing converges to the same visual speed at both a
      low and a high frame rate (test capped at 30 and uncapped/144).
- [ ] Look-input dead zone eliminates stick-noise jitter at rest without
      noticeably delaying small deliberate look adjustments.
- [ ] No frame exists where both a scripted camera event and player look input
      write to the camera transform without an explicit priority/blend rule.
