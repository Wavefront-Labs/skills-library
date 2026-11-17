---
id: computing-software.game-programming.multiplayer-networking.dead-reckoning-and-extrapolation
name: dead-reckoning-and-extrapolation
category: computing-software
field: game-programming
product: multiplayer-networking
tags: [multiplayer-networking, dead-reckoning, extrapolation, projective-velocity-blending, entity-interpolation, vehicles, error-correction, snap-threshold, game-programming]
level: practitioner
status: gated
description: "Hide latency for remote entities with dead reckoning: extrapolating position/velocity, projective velocity blending, snap thresholds, and when to interpolate instead."
sources: ["https://www.gamedeveloper.com/programming/dead-reckoning-latency-hiding-for-networked-games", "https://gafferongames.com/post/snapshot_interpolation/", "https://developer.valvesoftware.com/wiki/Source_Multiplayer_Networking"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dead reckoning and extrapolation

**Goal:** show remote entities where they probably are *now*, instead of where they were 100+ ms
ago, and correct smoothly when the next update disagrees.

## Interpolate or extrapolate?
- **Interpolation** (render 100 ms in the past between two known snapshots) is always correct but
  shows the past. Default for player characters in shooters, with lag compensation on the server.
- **Extrapolation / dead reckoning** predicts forward from the last known state. Good for things with
  inertia and predictable motion: vehicles, aircraft, ships, projectiles. Bad for humans that change
  direction instantly (extrapolated characters overshoot corners and jitter back).

## Basic extrapolation
From the last update (position `p0`, velocity `v0`, acceleration `a0`, timestamp `t0`):
```
dt = now - t0                        # server time of update, after clock sync
p_pred = p0 + v0*dt + 0.5*a0*dt*dt
```
Example: p0 = 0, v0 = 10, a0 = 2, dt = 0.3 s gives 3.09. Cap `dt` (e.g. 250-500 ms); beyond that freeze or fade out instead of flying off.
Orientation: integrate angular velocity similarly (quaternion).

## Smoothing corrections: projective velocity blending
When a new update arrives, the current displayed position `p_disp` and velocity `v_disp` differ from
the new prediction. Blend over `T` (often the expected update interval):
```
t  = clamp((now - t_update) / T, 0, 1)
v_b = v_disp + (v_new - v_disp) * t                       # blended velocity
p_proj_old = p_disp_at_update + v_b * elapsed + 0.5*a_new*elapsed^2
p_proj_new = p_new + v_new * elapsed + 0.5*a_new*elapsed^2
p_show = p_proj_old + (p_proj_new - p_proj_old) * t
```
(Murphy, "Believable Dead Reckoning for Networked Games", Game Engine Gems 2 (gated: unconfirmed, source is paywalled or blocked).) Avoids the visible
"pop" and the velocity discontinuity of simple lerping.

## Thresholds
- If error > snap distance (teleport, respawn, big desync), snap immediately.
- Send updates when the sender's own dead-reckoned model diverges beyond a threshold
  (DIS standard style), not only at fixed rate: saves bandwidth for predictable movers.

## Collision with the world
Extrapolated positions can go through walls. Clamp with a cheap sweep against static geometry or
accept brief penetration for cosmetics only; never use extrapolated remote positions for
authoritative hit decisions.

## Verify
- [ ] With 150 ms latency and 10% loss, vehicles move smoothly and corners overshoot less than ~1 m.
- [ ] No visible pops on correction except when beyond snap threshold.
- [ ] Network silence of 1 s: entity stops/fades, does not fly away.
