---
id: computing-software.game-programming.multiplayer-networking.client-prediction-and-server-reconciliation
name: client-prediction-and-server-reconciliation
category: computing-software
field: game-programming
product: multiplayer-networking
tags: [multiplayer-networking, netcode, client-side-prediction, server-reconciliation, server-authoritative, entity-interpolation, lag-compensation, rewind, tick-rate, snapshot, delta-compression, input-buffer, udp, reliable-udp, rollback, ggpo, lockstep, jitter-buffer, packet-loss, latency, netcode-for-gameobjects, unreal-replication, game-programming, error-smoothing]
level: advanced
status: draft
description: "Server-authoritative netcode that feels local: fixed ticks, input sequencing, client prediction, reconciliation by replay, interpolating remote entities, and lag-compensated hits."
sources: ["https://www.gabrielgambetta.com/client-server-game-architecture.html", "https://developer.valvesoftware.com/wiki/Source_Multiplayer_Networking", "https://gafferongames.com/categories/networked-physics/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Client prediction and server reconciliation

**Goal:** a server-authoritative action game where your own character responds instantly
despite 50–150 ms round trips, other players move smoothly, and hits are judged fairly —
without trusting the client.

## Architecture baseline
- **Server is authoritative**: clients send *inputs*, never positions or "I hit him".
  This is your main anti-cheat.
- Simulation runs at a **fixed tick** (e.g. 30, 60 or 64 Hz) on both sides with identical
  movement code (shared module). Snapshot send rate can be lower than tick rate
  (e.g. 20–30 Hz) to save bandwidth.
- Transport: UDP with your own reliability layer only where needed (or a library:
  ENet, GameNetworkingSockets, engine netcode). Movement and state snapshots are
  unreliable — a newer packet supersedes a lost one; chat, purchases, match events are
  reliable.

## 1. Inputs with sequence numbers
```
every client tick:
    cmd = { seq: ++seq, tick, buttons, aim, dt: TICK_DT }
    pending.push(cmd)
    apply_input(local_player, cmd)      // prediction: move immediately
    send(cmd)                           // often redundantly: last 3 cmds per packet, survives loss
```
The server applies each input once, in order, to the authoritative player, and includes
`last_processed_seq` for that client in each snapshot.

## 2. Reconciliation
When a snapshot arrives with server state S and `last_processed_seq = n`:
```
local_player.state = S.player                    // accept server truth
pending.remove_where(cmd.seq <= n)
for cmd in pending: apply_input(local_player, cmd)   // replay unacknowledged inputs
```
If prediction was right, the result equals what's on screen and nothing visibly
happens. If it differed (collision with another player, server-side effect), the player
snaps — so **smooth the correction**: keep a visual offset and decay it over ~100 ms
instead of teleporting, unless the error is large (then snap).
Requirement: `apply_input` must be deterministic enough that client and server agree
nearly always — same code, same fixed dt, same collision world.

## 3. Interpolating everyone else
You can't predict other players' inputs, so render them **in the past**:
- Buffer their snapshots with timestamps; render at `now − interp_delay`, where
  `interp_delay` ≈ 2 snapshot intervals (e.g. 100 ms at 20 Hz; Source's default
  `cl_interp` is 0.1 s) so one lost packet still leaves two points to interpolate between.
- Interpolate position linearly, rotations with slerp. Extrapolate briefly (≤ ~250 ms)
  if the buffer runs dry, then freeze.
- Consequence: you see others ~RTT/2 + interp_delay behind where they are on the server.

## 4. Lag compensation for hits
Because the shooter aimed at a past version of the target:
1. Server keeps a history of each player's hitboxes per tick (e.g. last 1 s).
2. Client sends the fire command with the tick/time it was rendering
   (its clock minus interpolation delay).
3. Server **rewinds** other players' hitboxes to that time, does the hit test, restores.
4. Cap the rewind (e.g. 200–250 ms) so very high-ping players can't shoot people who
   have long since reached cover. "Shot behind the wall" complaints are the trade-off
   — you're choosing to favour the shooter.

## 5. Bandwidth
- Delta-compress snapshots against the last state the client **acknowledged**.
- Quantise: positions to cm in a bounded range, angles to 16 bits, booleans as bits.
- Relevancy / interest management: don't send entities the client can't perceive.
- Budget rough numbers: tens of kbit/s per client is typical for shooters; measure yours.

## Alternatives
- **Deterministic lockstep** (RTS): send only inputs, everyone simulates; needs full
  determinism, input delay equals the slowest peer.
- **Rollback** (fighting games, GGPO-style): predict remote inputs, roll back and
  re-simulate when real ones arrive; needs fast, deterministic, serialisable state.
- Engine frameworks (Unreal's CharacterMovementComponent, Unity Netcode for
  GameObjects/Entities, Photon Fusion, Godot's MultiplayerSynchronizer) implement parts of
  this; know which parts before relying on them.

## Verify
- [ ] Test with simulated latency/loss/jitter (e.g. `tc netem` on Linux, clumsy on
      Windows, or the engine's network emulation): 150 ms RTT, 2% loss, 20 ms jitter.
- [ ] Own movement feels instant at 150 ms; corrections are rare and smooth.
- [ ] Remote players move smoothly with 2% loss.
- [ ] A client sending fake positions or hit claims has no effect.
- [ ] Hit registration fair at 100 ms; rewind capped.
