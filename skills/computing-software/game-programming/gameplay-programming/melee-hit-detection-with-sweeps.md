---
id: computing-software.game-programming.gameplay-programming.melee-hit-detection-with-sweeps
name: melee-hit-detection-with-sweeps
category: computing-software
field: game-programming
product: gameplay-programming
tags: [gameplay-programming, hitbox, melee-hit-detection, weapon-trace, hit-registration, game-programming]
level: practitioner
status: draft
description: "Register melee hits reliably: weapon traces between animation frames, active-frame windows from animation events, per-swing hit lists, and server-side validation in multiplayer."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/animation-notifies-in-unreal-engine", "https://docs.unity3d.com/ScriptReference/Physics.CapsuleCast.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Melee hit detection with sweeps

**Goal:** fast swords never pass through enemies between frames, each swing hits a target once, and
hits match what the animation shows.

## Active window
Animation events/notifies mark `HitStart` and `HitEnd` frames (or a notify state spanning them).
Only trace inside the window. Store frame data so designers tune windows without code.

## Sweeping the blade
Overlap checks at each frame miss thin, fast weapons. Instead, each tick during the window:
1. Sample N points along the blade (socket base to tip) at current pose.
2. For each point, sweep/raycast from its previous position to the current one (or capsule-cast the
   blade segment from previous to current pose).
3. Collect hits on hurtbox layers.
```csharp
for (int i = 0; i < samples; i++) {
    Vector3 cur = Vector3.Lerp(baseSocket.position, tipSocket.position, i / (samples - 1f));
    if (Physics.Linecast(prev[i], cur, out var hit, hurtboxMask) && hitThisSwing.Add(hit.collider.attachedRigidbody))
        OnHit(hit);
    prev[i] = cur;
}
```
At low frame rates, sub-step by interpolating poses (or sample bone transforms at sub-frame times if the
engine allows) — a 30 fps swing can move the tip a meter per frame.

## Hit bookkeeping
- `hitThisSwing` set cleared at window start: one hit per target per swing (unless multi-hit by design).
- Hit stop / hit pause applied on first hit; continue tracing after.
- Hit point and normal from the trace for VFX/decals; hit direction from blade velocity for reactions.

## Alternatives
- Simple shapes (box in front of the character active for N frames) — fine for many games, deterministic,
  easier to network. Blade traces when visual fidelity matters.
- Fighting games: per-frame authored hitboxes rather than physics traces.

## Multiplayer
Client traces for responsiveness (predicted hit effects); server validates: replays the swing with
lag compensation (rewind targets to the attacker's view time), checks distance/angle sanity, then
applies damage.

## Gotchas
- Hitting yourself or allies: filter by owner/team before applying.
- Traces starting inside a collider don't report hits in some engines; also overlap at window start.
- Animation root motion/IK changes blade path between client and server — validate generously.

## Verify
- [ ] At 20 fps (forced), swings still hit targets that are hit at 120 fps.
- [ ] Debug draw of trace segments matches the visible blade path.
