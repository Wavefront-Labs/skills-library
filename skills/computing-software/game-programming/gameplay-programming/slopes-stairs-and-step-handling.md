---
id: computing-software.game-programming.gameplay-programming.slopes-stairs-and-step-handling
name: slopes-stairs-and-step-handling
category: computing-software
field: game-programming
product: gameplay-programming
tags: [gameplay-programming, character-controller, stairs-handling, slope-movement, step-up, game-programming]
level: practitioner
status: draft
description: "Make characters handle slopes and stairs well in any engine: slope projection, max slope angle, step-up and step-down snapping, sliding on steep faces and speed on inclines."
sources: ["https://docs.unity3d.com/Manual/class-CharacterController.html", "https://docs.godotengine.org/en/stable/classes/class_characterbody3d.html", "https://jrouwe.github.io/JoltPhysics/class_character_virtual.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Slopes, stairs and step handling

**Goal:** walking over ramps, stairs and bumpy terrain feels smooth: no launching off crests, no
bouncing down stairs, no climbing walls.

## Slope movement
1. Ground probe (sphere/capsule cast down) gives `groundNormal`.
2. Walkable if `angle(groundNormal, up) <= maxSlope` (typ. 45-50 degrees).
3. Project desired horizontal velocity onto the ground plane so speed stays constant on inclines:
```
v = desired - groundNormal * dot(desired, groundNormal)
v = normalize(v) * |desired|           // keep authored speed, or scale down uphill by design
```
4. On non-walkable slopes: remove the velocity component into the slope and add gravity sliding along
   it (`slideDir = normalize(projectOnPlane(-up, normal))`).

## Step up (stairs)
Engines: Unity CharacterController `stepOffset`, Godot `floor_snap_length` + `floor_max_angle` (no
built-in step-up — implement), Jolt `CharacterVirtual::ExtendedUpdate` with `mWalkStairsStepUp`, Unreal
CMC `MaxStepHeight`.
Manual algorithm when blocked by a low obstacle while grounded:
1. Cast the capsule **up** by stepHeight; if free,
2. cast **forward** by the remaining move; if free,
3. cast **down** by stepHeight (+ small epsilon); if it lands on walkable ground, accept the new position.
4. Only step if the hit surface normal at the riser is near-vertical (avoid stepping onto steep ramps).
Step height ~0.3-0.4 m for humans; must be smaller than capsule radius-ish to avoid odd snags.

## Step down / ground snapping
Moving down stairs or over crests at speed leaves the ground for a frame -> "air" state, falling anim,
lost jump. While previously grounded and not jumping, cast down up to `snapDistance` (step height) and
move the character onto the hit if walkable. Godot: `floor_snap_length`; Unity: manual SphereCast snap.

## Visual smoothing
Stepping produces vertical pops; smooth the **camera and mesh** height (lerp the visual child toward
the capsule over ~0.1 s), not the collision capsule.

## Speed on slopes
Common designs: same speed in all directions (projected), slower uphill (multiply by curve of slope
angle), faster downhill for sliding games. Make it a tunable curve.

## Gotchas
- Capsule bottom roundness makes edges act like ramps: characters slide off ledges slowly — add
  a "ledge" check comparing ray-under-center vs capsule contact normal.
- Ground normal from the capsule contact at an edge is diagonal; use a ray from the center for
  slope decisions.
- Jump must disable snapping for a few frames or it snaps back down.

## Verify
- [ ] Run up and down a staircase at full speed: grounded state never flickers (log it).
- [ ] Walking into a 60-degree wall doesn't climb; 40-degree ramp walks at constant speed.
