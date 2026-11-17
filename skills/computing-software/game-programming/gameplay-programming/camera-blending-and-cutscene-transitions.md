---
id: computing-software.game-programming.gameplay-programming.camera-blending-and-cutscene-transitions
name: camera-blending-and-cutscene-transitions
category: computing-software
field: game-programming
product: gameplay-programming
tags: [gameplay-programming, camera-blending, camera-rails, cutscene, game-programming]
level: practitioner
status: draft
description: "Blend between gameplay, rail and cutscene cameras with priority stacks, eased interpolation of position, rotation and FOV, and safe hand-back."
sources: ["https://docs.unity3d.com/Packages/com.unity.cinemachine@3.1/manual/concept-camera-control-transitions.html", "https://docs.unity3d.com/Packages/com.unity.cinemachine@3.1/manual/index.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Camera blending, rails and cutscene transitions

**Goal:** move between camera behaviours without pops, the model Cinemachine popularised: many
virtual cameras, one real camera, a brain that blends.

## Virtual cameras + priority
Each behaviour (follow, aim, rail, cutscene shot) produces a *desired pose* every frame:
position, rotation, FOV. The highest-priority active virtual camera wins; on change, blend from the
**live** pose of the old one (keep evaluating it during the blend) to the new one.

```cpp
Pose blend(const Pose& a, const Pose& b, float t) {      // t eased 0..1
    return { lerp(a.pos, b.pos, t), slerp(a.rot, b.rot, t), lerp(a.fov, b.fov, t) };
}
float easeInOut(float x) { return x * x * (3 - 2 * x); }
```
- Blend rotation with slerp of the final orientation; lerping yaw/pitch separately spins the long
  way around at 180 degrees.
- For orbit cameras, blending in spherical coordinates around the target avoids cutting through
  the character.
- A blend interrupted by another change starts from the current blended pose (blend stacks).

## Rails (dolly tracks)
Parameterise a spline by arc length; find the track position closest to the player (project, then
smooth with a critically damped spring) and look at the player. Clamp speed along the rail so it
does not race when the player teleports.

## Cutscene hand-off
- Into a cutscene: cut if the shot is far away (a blend across the level looks wrong), blend if close.
- Out of a cutscene: snap the gameplay camera's internal state (orbit yaw, pitch) to match the last
  shot, then blend; otherwise the follow camera starts from stale angles.
- Disable camera collision probes during blends or the probe pulls the blend toward walls.

## Verify
- Trigger two transitions within a blend; no pop.
- Record camera pose per frame during a transition and plot velocity: no spikes.
