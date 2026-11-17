---
id: computing-software.game-programming.multiplayer-networking.snapshot-interpolation
name: snapshot-interpolation
category: computing-software
field: game-programming
product: multiplayer-networking
tags: [multiplayer-networking, snapshot, snapshot-interpolation, interpolation-buffer, jitter-buffer, hermite-interpolation, packet-loss, render-delay, game-programming]
level: practitioner
status: gated
description: "Render networked state smoothly with snapshot interpolation: snapshot buffers, choosing the interpolation delay, linear vs Hermite interpolation, handling loss and buffer underrun."
sources: ["https://gafferongames.com/post/snapshot_interpolation/", "https://developer.valvesoftware.com/wiki/Source_Multiplayer_Networking", "https://www.gabrielgambetta.com/entity-interpolation.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Snapshot interpolation

**Goal:** remote objects move smoothly even though snapshots arrive at 10-30 Hz with jitter and loss
(Gaffer On Games "Snapshot Interpolation"; Source engine `cl_interp`).

## Mechanism
- Server sends periodic snapshots: tick/time + state of relevant entities.
- Client stores them in a buffer ordered by server time.
- Client renders at `renderTime = estimatedServerTime - interpolationDelay`, finding the two snapshots
  surrounding `renderTime` and interpolating:
```
a, b = snapshots with a.time <= renderTime < b.time
t = (renderTime - a.time) / (b.time - a.time)
pos = lerp(a.pos, b.pos, t)
rot = slerp(a.rot, b.rot, t)
```

## Choosing the delay
`interpolationDelay` must cover the send interval plus jitter, and ideally one lost packet:
- At 20 Hz (50 ms interval): 100 ms delay survives one lost snapshot (Source default
  `cl_interp 0.1` = 2 snapshots (gated: unconfirmed, source is paywalled or blocked)).
- Gaffer's example (10 snapshots per second in the article's later demos) recorded its videos with a 350 ms delay to survive bursts of loss: larger delay = more robust, more
  latency for remote entities.
Make it adaptive: measure jitter and loss, keep the buffer at target depth, adjust slowly.

## Better interpolation
Linear interpolation of positions sampled at low rates shows corners on curved motion. If snapshots
include velocity, use **Hermite** interpolation (positions + velocities as tangents scaled by the
interval) for smooth curves. Gaffer notes this matters for physics objects at low send rates. Computed here for a point circling at radius 10 m, 2 rad/s, sampled at 10 Hz: the worst-case rendering error was 0.0500 m with linear interpolation and 0.00004 m with Hermite (tangents = velocity x interval).

## Edge cases
- **Underrun** (no newer snapshot): briefly extrapolate (cap at ~100-250 ms) or hold the last state;
  then catch up by slightly speeding up render time instead of snapping.
- **Teleports/respawns**: a flag in the snapshot to skip interpolation for that entity.
- **Entity creation/destruction**: create when it first appears in a snapshot at render time, destroy
  when render time passes its removal.
- Local player is not interpolated (predicted instead); interpolated remote players are seen in the
  past, so hit detection needs server lag compensation.

## Clock
Render time is derived from server time estimation (see multiplayer-networking
tick-rate-and-clock-synchronization); drive it with a smoothly adjusted clock, never jump per packet.

## Verify
- [ ] Remote entity motion is smooth under 5% loss and 30 ms jitter (network conditioner).
- [ ] Buffer depth graph stays near target; underruns are rare and recover without pops.
- [ ] Teleported entities snap without sliding across the map.
