---
id: computing-software.game-programming.multiplayer-networking.headless-client-builds-for-tests
name: headless-client-builds-for-tests
category: computing-software
field: game-programming
product: multiplayer-networking
tags: [multiplayer-networking, network-testing, headless-client, bots, nullrhi, batchmode, ci, game-programming]
level: practitioner
status: draft
description: "Build and run headless game clients for multiplayer tests: no-render flags per engine, scripted bot input, many clients per machine, and what headless can't catch."
sources: ["https://docs.unity3d.com/Manual/EditorCommandLineArguments.html", "https://docs.unity3d.com/Manual/PlayerCommandLineArguments.html", "https://dev.epicgames.com/documentation/en-us/unreal-engine/command-line-arguments-in-unreal-engine", "https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Headless client builds for tests

**Goal:** run tens to hundreds of real game clients without GPUs or windows, to test connection
flows, replication, and server load in CI.

## Launch without rendering
| Engine | Command |
|---|---|
| Unity player | `Game.exe -batchmode -nographics -logFile client1.log -- args`; Linux Dedicated Server build target strips rendering for servers, clients use `-batchmode -nographics` |
| Unreal | `Game.exe -nullrhi -nosound -unattended -log=client1.log 127.0.0.1:7777` (`-nullrhi` disables rendering; `-RenderOffscreen` keeps rendering without a window) |
| Godot | `godot --headless --path . -- --bot --server=127.0.0.1` (Godot 4 `--headless` uses dummy display and audio drivers) |

Pass test parameters after `--` (Unity/Godot) or as `-key=value` (Unreal `FParse::Value(FCommandLine::Get(), ...)`).

## Bot input
- Feed input through the same layer the player uses (action/input system), not by calling gameplay
  functions directly, so prediction and RPC paths run. Behaviours: random walk, follow waypoints,
  fire at nearest target, join/leave loops, chat spam.
- Seed bots deterministically per client index for reproducible failures.
- Exit with a status code: 0 on success criteria met, non-zero on disconnect/timeout/assert, so the
  CI orchestrator can fail the job.

## Many clients per machine
- Cap frame rate (`Application.targetFrameRate`, `t.MaxFPS`, `Engine.max_fps`) to save CPU.
- Disable audio, particle and animation update where possible in a `HEADLESS_CLIENT` define.
- Give each client its own log file and a unique identity/auth token.
- Spread across containers or VMs; one machine's NIC and loopback hide real network behaviour, so
  combine with packet-loss/latency emulation (`tc netem`, Clumsy, engine network emulation).

## What headless misses
GPU-dependent code paths, UI flows, animation-driven gameplay (if animation is skipped), and frame
pacing problems. Keep at least one rendered client in the soak test.

## CI shape
Start server -> wait for "listening" log line -> spawn N clients -> run for T minutes -> collect logs,
server metrics and crash dumps -> fail on any error-level log pattern.

## Verify
- [ ] 50 headless clients connect, play and disconnect cleanly in a nightly job.
- [ ] A forced client crash fails the job and the dump is archived.
