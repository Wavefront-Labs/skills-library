---
id: computing-software.game-programming.gameplay-programming.hitscan-and-projectile-weapons
name: hitscan-and-projectile-weapons
category: computing-software
field: game-programming
product: gameplay-programming
tags: [gameplay-programming, hitbox, combat-timing, hitscan, projectiles, raycast-weapons, bullet-spread, projectile-pooling, swept-collision, camera-vs-muzzle, game-programming]
level: practitioner
status: draft
description: "Implement weapon firing: hitscan raycasts from camera vs muzzle, spread and recoil patterns, physical projectiles with swept collision and pooling, penetration and hit reporting."
sources: ["https://docs.unity3d.com/ScriptReference/Physics.Raycast.html", "https://dev.epicgames.com/documentation/en-us/unreal-engine/traces-with-raycasts-in-unreal-engine", "https://developer.valvesoftware.com/wiki/Source_Multiplayer_Networking"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Hitscan and projectile weapons

**Goal:** weapons that hit where the crosshair points, feel consistent, and do not tunnel or cost too
much.

## Hitscan
```
aimRay = camera ray through crosshair (screen centre)
aimPoint = first hit of aimRay (or far point at max range)
dir = normalize(aimPoint - muzzle) (+ spread)
hit = raycast(muzzle, dir, range, mask = world | hurtboxes)
```
- Tracing from the **camera** decides what the player aimed at; tracing again from the **muzzle**
  prevents shooting through a wall right in front of the gun (third-person especially). If the muzzle
  trace is blocked close by, the shot hits that obstacle.
- Spread: random direction in a cone (`Random.insideUnitCircle * tan(spreadAngle)` added to the
  perpendicular plane); grow spread while firing, shrink over time; first-shot accuracy bonus.
- Recoil pattern: deterministic per-shot camera kick sequence (learnable) plus small random component.
- Shotgun: N pellets with spread, damage per pellet, falloff by distance.

## Projectiles
Use for slow, visible or ballistic shots (rockets, arrows, grenades).
- Move in `FixedUpdate`/physics tick; check collisions with a **swept test** each step
  (raycast/spherecast from previous to current position) rather than relying on trigger overlap, which
  tunnels at high speed.
- Ballistics: `v += gravity * dt; p += v * dt`; drag optional.
- Pool projectiles (no Instantiate/Destroy per shot); lifetime and max range to return them.
- Spawn at muzzle but aimed at the camera's aim point so they converge on the crosshair.

## Hit processing
On hit: identify the hurtbox (component on collider or physics material for headshots), build a
damage event (amount, type, instigator, hit point, normal, bone) and pass to the target's damage
pipeline; spawn impact effects by surface type (physics material -> decal/sound/particle table).
Penetration: continue the trace with reduced damage after thin surfaces up to a max thickness.

## Multiplayer note
Client plays muzzle flash/tracers immediately; server validates hits with lag compensation (rewind
hurtboxes to the client's view time) before applying damage. Projectiles: server-authoritative
simulation with client-side visual prediction.

## Verify
- [ ] Shots land exactly at the crosshair at all ranges (debug draw rays).
- [ ] Fast projectiles never pass through thin walls at the minimum frame rate.
- [ ] Firing full auto for a minute causes no GC/instantiation spikes (pooling).
