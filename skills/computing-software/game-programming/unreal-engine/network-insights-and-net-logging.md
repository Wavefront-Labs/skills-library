---
id: computing-software.game-programming.unreal-engine.network-insights-and-net-logging
name: network-insights-and-net-logging
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, network-insights, networking, replication, bandwidth, profiling, network-profiler, game-programming]
level: practitioner
status: docs-checked
description: "Profile Unreal replication with Networking Insights (-trace=net, -NetTrace), read its panels, and use the legacy Network Profiler (netprofile, .nprof) for per-actor bandwidth."
sources:
  - https://dev.epicgames.com/documentation/en-us/unreal-engine/networking-insights-in-unreal-engine
  - https://dev.epicgames.com/documentation/en-us/unreal-engine/using-the-network-profiler-in-unreal-engine
  - https://dev.epicgames.com/documentation/en-us/unreal-engine/testing-and-debugging-networked-games-in-unreal-engine
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Network Insights and the Network Profiler

**Goal:** find which actors, properties and RPCs use bandwidth.

## Networking Insights capture
Networking Insights is part of the Unreal Insights suite; Unreal Insights must be running first. Start the
client game instances with:
```
-trace=net -NetTrace=<VERBOSITY> [-tracehost=localhost]
```
- `-trace=net` traces the networking category; `-NetTrace` sets the recording verbosity and should be
  greater than zero (the page's example is `-NetTrace=1`).
- The editor runs its own trace data store, so to capture while running in the editor also pass
  `-tracehost` (the page's example: `-NetTrace=1 -trace=net -tracehost=localhost`).

## Panels
- **Packet Overview**: a bar graph of the size in bits of every packet sent or received; click a bar to
  select it (Shift-click for more). Dropped packets are red. Hover shows packet index, sequence number,
  content size, total size, timestamp, delivered/undelivered status, connection state and engine frame
  number. Sizes are before compression, so wire data may be smaller.
- **Packet Content**: the selected packet's content as a hierarchical event graph from bit zero. Level 0
  shows bunches (named after the channel, or the debug name if set); level 2 typically shows replicated
  objects (with NetId once assigned); below that, replicated properties and RPCs with the bits they wrote.
  Filter by NetId and by event type.
- **Connection Selection**: dropdowns for Game Instance (one per NetDriver; PIE has separate server and
  client instances), Connection and Connection Mode (incoming or outgoing).
- **Net Stats**: trace events for the selected packet range with columns Type, Level, Instance Count, Total
  Inclusive Size (bits), Max Inclusive Size (bits), Total Exclusive Size and Max Exclusive Size; sort by any
  active column, group by Level, Flat or Name. Levels: 0 channel information, 1 replicated object (actor),
  2 property replication or RPC events, 3 property serialisation, 4 extra property and array events.
- **Net Stats Counters**: frame stats and packet stats, fed by `UE_NET_TRACE_FRAME_STATSCOUNTER` and
  `UE_NET_TRACE_PACKET_STATSCOUNTER` in C++.

## Legacy Network Profiler
Epic describes it as a legacy tool, less detailed than Networking Insights but a high-level view of bandwidth
and per-actor, property and RPC stats.
- Needs an engine build with stat tracking: typically a debug build, or an editor build for non-debug
  configurations (the `STATS` macro defined nonzero).
- Record with the `networkprofiler=true` command-line argument, or at runtime with `netprofile` (toggle),
  `netprofile enable` or `netprofile disable`.
- Output is `<PROJECT_DIRECTORY>/Saved/Profiling/<PROJECT_NAME>-<TIMESTAMP>.nprof`
  (`NetworkProfiling.tmp` is the temporary file during recording).
- Open the file in the standalone `<UNREAL_ENGINE_ROOT>/Engine/Binaries/DotNET/NetworkProfiler.exe`
  with Open File. Tabs: Chart, Filters, Details; All Actors; All Properties; All RPCs; All Objects.
- Record on the server when you want actor and property detail: only servers replicate actors and
  properties, so a client recording shows detailed data only for RPCs sent from that client.

## Debugging multiple instances (from the Debugging Guide)
- Watch `UnrealEditor-Engine!GPlayInEditorContextString` to see which PIE instance you are stepping through;
  the `NetDriver` `ServerConnection` is null on the server and set on clients.
- `GetLocalRole()` returns `ROLE_Authority` (exists on the server), `ROLE_AutonomousProxy` (Character or
  Pawn possessed by a local PlayerController) or `ROLE_SimulatedProxy` (exists on a client).
- PIE has limits for server/client travel; test those as a separate Standalone process.

## Verify
- [ ] A trace from a worst-case play session was opened and the biggest packets inspected down to the
      property or RPC level.

## Checked
Checked 2026-11-08 against the Networking Insights, Network Profiler and Debugging Guide pages.
Confirmed: command-line options, panels and columns, Network Profiler recording, file path, executable path,
server-vs-client note, debugging watch values and roles.
Removed because the pages do not state them: `LogNet`/`LogRep` verbosity commands, `net.RepGraph.PrintGraph`,
`NetEmulation.*`, `Trace.Start`, the NetTrace level range, and the optimisation advice list.
Method: docs-only read of cited pages, 2026-11-08
