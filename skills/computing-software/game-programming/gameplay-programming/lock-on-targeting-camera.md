---
id: computing-software.game-programming.gameplay-programming.lock-on-targeting-camera
name: lock-on-targeting-camera
category: computing-software
field: game-programming
product: gameplay-programming
tags: [gameplay-programming, third-person-camera, lock-on, target-switching, soulslike-camera, game-programming, target-selection]
level: practitioner
status: draft
description: "Build lock-on targeting: target scoring, stick-flick switching, camera framing of player and target, breaking lock on distance or occlusion, and strafing."
sources: ["https://www.gdcvault.com/play/1022227/50-Game-Camera-Mistakes", "https://docs.unity3d.com/Packages/com.unity.cinemachine@3.1/manual/CinemachineTargetGroup.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lock-on targeting cameras

**Goal:** soulslike/action lock-on that picks the intended enemy, frames both characters and stays
readable in crowds.

## Target selection on press
Candidates within radius R (e.g. 20 m), on screen, with line of sight. Score:
```
score = w_angle * (1 - angleFromCameraForward / maxAngle)
      + w_dist  * (1 - dist / R)
      + w_threat * isAttackingPlayer
```
Pick highest; no candidate -> recenter camera behind player instead (common fallback).

## Switching
- Stick flick (magnitude crosses threshold then returns) left/right selects the nearest candidate in
  that screen direction: sort by signed screen-space x relative to current target, ignore ones behind.
- Debounce flicks (~0.25 s) and require stick return to neutral.
- On target death: auto-switch to next best within a smaller radius, or release.

## Camera framing
- Place camera behind the player along the player->target direction, raised, looking at a point
  between them (biased toward the target, e.g. 60%).
- Increase distance/FOV as they separate; clamp pitch so a tall boss is still framed.
- Smooth yaw with damping but faster than free camera; avoid flipping when the target passes over
  or very close to the player (lock yaw changes when horizontal distance < ~1.5 m).
- Engines: Cinemachine Target Group + composer; Unreal spring arm with control rotation driven toward
  target; Godot custom.

## Breaking lock
- Distance > R * 1.2 (hysteresis), LOS blocked for > 1 s, target invisible/despawned, player input to
  cancel. Never break silently mid-attack.

## Movement while locked
- Character faces the target; input becomes strafe relative to target (circle-strafe), animation uses
  strafe blend space.
- Dodge directions relative to the target.

## UI
Lock-on reticle on the target's lock point (chest socket), not its pivot; for big enemies multiple lock
points selectable.

## Gotchas
- Switching picks targets behind walls: include LOS in switch candidates.
- Camera collision while locked needs stronger pull-in rules (walls behind player).

## Verify
- [ ] In a group of 5, press lock: chosen target is the one nearest screen center most of the time.
- [ ] Target runs behind a pillar: lock persists briefly then breaks.
