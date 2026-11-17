---
id: computing-software.game-programming.multiplayer-networking.bot-soak-and-load-testing-game-servers
name: bot-soak-and-load-testing-game-servers
category: computing-software
field: game-programming
product: multiplayer-networking
tags: [multiplayer-networking, load-test-bots, soak-testing, headless-clients, server-performance, capacity-planning, game-programming]
level: advanced
status: draft
description: "Load and soak test game servers with bots: headless and protocol bots, realistic behaviour, ramp/spike/soak profiles, metrics and pass criteria."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/gauntlet-automation-framework-in-unreal-engine", "https://docs.locust.io/en/stable/", "https://docs.unity3d.com/Manual/PlayerCommandLineArguments.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Bot soak and load testing game servers

**Goal:** know how many players a server process and the backend hold, and find leaks and crashes
that appear only after hours or at full capacity, before launch day finds them.

## Two kinds of bots
- **Headless game clients** (real client build with `-nullrhi`/`-batchmode -nographics`, AI driving
  inputs): exercise everything, but cost ~0.2-1 CPU core each; good for 10s-100s per machine.
  Unreal Gauntlet can launch and orchestrate many client/server processes; Unity
  `-batchmode -nographics` builds with a bot input provider.
- **Protocol-level bots** (lightweight program speaking your net protocol, no simulation): 1000s per
  machine; for connection/matchmaking/backend load. Locust/k6 suit HTTP backends (login, inventory,
  matchmaking); a custom bot harness drives the UDP game protocol.

## Behaviour must be realistic
Idle bots underload the server. Script them to move, fight, use abilities, chat, open inventories,
join and leave at measured real-player rates (from playtest telemetry). Include worst cases: all 100
players in one spot (relevancy/bandwidth spike), everyone respawning at once, mass disconnect.

## Test profiles
- **Ramp**: add players steadily until a metric breaks; find capacity per process/core.
- **Spike**: 0 -> peak in a minute (launch, stream drops).
- **Soak**: target load for 8-24 h; finds memory leaks, handle leaks, counter overflows (16-bit
  sequence, int32 timers in ms overflow after ~24.8 days, float time precision after many hours).

## Metrics
Server tick time p50/p99 vs budget (e.g. 33 ms at 30 Hz), tick rate actually achieved, CPU per player,
memory RSS growth over time, bandwidth per client, packets/s, GC pauses (Unity/.NET), reliable
buffer overflows, disconnect/timeouts, backend latency and error rates. Bots report their own RTT
and correction counts.

## Pass criteria (write them before testing)
Example: 100 bots, 60 min, tick p99 < 30 ms, memory growth < 50 MB/h, zero crashes, < 0.5%
disconnects. Run nightly in CI at small scale; full scale before milestones.

## Verify
- [ ] Capacity per server instance is a measured number with the test profile attached.
- [ ] A 12-hour soak shows flat memory after warm-up.
- [ ] Crash dumps from bot runs are collected automatically.
