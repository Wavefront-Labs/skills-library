---
id: computing-software.game-programming.unity.ngo-networktransform-and-client-authority
name: ngo-networktransform-and-client-authority
category: computing-software
field: game-programming
product: unity
tags: [unity, netcode-for-gameobjects, networktransform, client-network-transform, interpolation-ngo, game-programming]
level: practitioner
status: draft
description: "Sync movement in Netcode for GameObjects with NetworkTransform: server vs owner authority, thresholds, interpolation, half-float and teleporting correctly."
sources: ["https://docs-multiplayer.unity3d.com/netcode/current/components/networktransform/", "https://docs-multiplayer.unity3d.com/netcode/current/learn/clientside-interpolation/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# NGO NetworkTransform and authority

**Goal:** smooth, bandwidth-sane movement replication with the right authority model.

## Authority modes
- **Server authoritative** (default `NetworkTransform`): only the server writes the transform; owners
  send input via RPCs. Cheat-resistant, adds input latency without prediction.
- **Owner authoritative**: NGO 2.x has `AuthorityMode = Owner` on NetworkTransform (1.x: subclass
  `ClientNetworkTransform` overriding `OnIsServerAuthoritative() => false`). Owner moves locally and
  replicates; responsive, trusts clients.
- Distributed authority topology (NGO 2.x + Multiplayer Services): owner authority by design.

## Settings
- Sync Position/Rotation/Scale per axis: disable what you don't need (scale, X/Z rotation for
  characters).
- **Thresholds** (Position/Rotation/Scale): changes below are not sent.
- **Interpolate**: buffered interpolation on non-authority instances (adds ~ tick delay). Keep on for
  remote players.
- **Use Half Float Precision** and **Use Quaternion Compression**: big bandwidth savings; half floats
  lose precision far from origin (NGO uses delta from a base position to mitigate).
- **In Local Space** for parented objects.
- Tick rate (NetworkManager > Tick Rate) caps send frequency.

## Teleporting
Setting `transform.position` on the authority interpolates the jump across clients. Use
`networkTransform.Teleport(pos, rot, scale)` (authority side) to skip interpolation.

## Rigidbodies
Add `NetworkRigidbody`: non-authority instances become kinematic. Physics on the non-authority side
is not simulated — collisions there are visual only.

## Gotchas
- Modifying the transform on a non-authority instance is overwritten next update (and logs warnings).
- Animator: use `NetworkAnimator` (also server/owner authority choice) — not NetworkTransform.
- Parenting NetworkObjects requires both to be NetworkObjects and done on the server (or authority);
  plain `SetParent` desyncs.

## Verify
- [ ] Network Simulator with 150 ms latency: remote players move smoothly.
- [ ] Teleport does not produce a visible slide on clients.
