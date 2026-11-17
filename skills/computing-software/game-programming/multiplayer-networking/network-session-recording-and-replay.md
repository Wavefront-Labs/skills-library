---
id: computing-software.game-programming.multiplayer-networking.network-session-recording-and-replay
name: network-session-recording-and-replay
category: computing-software
field: game-programming
product: multiplayer-networking
tags: [multiplayer-networking, network-replay, packet-capture, replay-system, demo-recording, desync-debugging, replication-graph, game-programming, input-replay]
level: advanced
status: draft
description: "Record and replay network sessions for debugging and demos: packet-level vs input-level vs snapshot recording, Unreal DemoNetDriver, Wireshark dissectors and desync diffing."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/using-the-replay-system-in-unreal-engine", "https://www.wireshark.org/docs/wsdg_html_chunked/ChapterDissection.html", "https://developer.valvesoftware.com/wiki/Demo_Recording_Tools"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Network session recording and replay

**Goal:** turn "it desynced once in a 40-minute match" into a file you can replay, step and diff;
the same machinery powers kill-cams and match demos.

## Three levels of recording
| Record | Replays by | Good for | Caveat |
|---|---|---|---|
| **Raw packets** (incoming bytes + receive time per connection) | feeding them back into the client's net layer | client bugs, deserialisation crashes | must replay with the same build |
| **Inputs** (per-tick inputs of all players + initial state + seed) | re-simulating | deterministic lockstep/rollback games; tiny files | requires full determinism |
| **Snapshots/replicated state** (server's view per tick or delta) | playing state back | demos, kill-cams, spectating, server-authoritative games | larger; no re-simulation |
Always store build version, map, settings and seeds in the header; reject mismatched builds.

## Engine support
- **Unreal Replay System:** `DemoNetDriver` records replicated data to a stream (local file or HTTP
  streamer). `demorec MyDemo`, `demostop`, `demoplay MyDemo`; scrub with `demoscrub`/`DemoPause`.
  Actors replay via normal replication (RepNotifies fire). Use for kill-cam with a duplicate level
  collection.
- **Source engine** `record`/`playdemo` are the classic example of snapshot demos.
- Custom engines: tee the receive path (`onPacketReceived(bytes, time)`) into a ring buffer on disk;
  flush the last N minutes when a desync or crash is detected.

## Debugging desyncs with recordings
1. On checksum mismatch, both peers dump their recording plus full state at the mismatch tick.
2. Replay the input log locally in two builds/configs and log per-tick state hashes per subsystem
   (physics, AI, RNG) to find the first diverging tick and subsystem.
3. Diff field-by-field at that tick.

## Packet inspection
Write a Wireshark dissector (Lua plugin) for your protocol header so captures show sequence, acks
and message types; invaluable for loss/ordering bugs and console certification network logs.
Encrypted packets need a debug key-log mode in dev builds.

## Verify
- [ ] A recorded match replays to the same final state hash (input-level) or visually identical
  (snapshot-level).
- [ ] Ring-buffer recording costs under 1% CPU and bounded disk.
- [ ] Replays from an older build fail with a clear version message.
