---
id: computing-software.game-programming.unreal-engine.unreal-insights-traces-and-cpu-scopes
name: unreal-insights-traces-and-cpu-scopes
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, ue5, performance, insights-trace, unreal-insights, profiling, trace-channels, trace-server, game-programming]
level: advanced
status: docs-checked
description: "Capture Unreal Insights traces: Trace Server and store, trace channels and defaults, trace console commands, Insights widget, late connect, tail tracing and Timing Insights."
sources:
  - https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-insights-in-unreal-engine
  - https://dev.epicgames.com/documentation/en-us/unreal-engine/trace-in-unreal-engine-5
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Unreal Insights traces

**Goal:** record a trace on target hardware, choose channels sensibly, and open it in Unreal Insights.

## Components
- Trace events (instrumentation in the process), the **Unreal Trace Server** (records and saves traces),
  and Unreal Insights (analyses and visualises). Traces are `.utrace` files; companion data goes in
  `.ucache` files in the same directory.
- `UnrealTraceServer.exe` (in `Engine/Binaries/Win64`) starts automatically. Its Trace Recorder listens on
  port 1981 for incoming trace connections; its Trace Store keeps recorded traces in a folder and lists
  them for the Insights UI. One server instance is shared by projects and branches, and Epic notes support
  is for one user per machine.
- Server configuration and logs: `%LOCALAPPDATA%/UnrealEngine/Common/UnrealTrace` on Windows,
  `~/UnrealEngine/UnrealTrace` on macOS and Linux. Stop the server with `UnrealTraceServer kill`.
- Since UE 5.3 the Trace Server is enabled for all desktop platforms.
- Insights is `Engine\Binaries\[Platform]\UnrealInsights[.exe]` in a binary engine install; from source
  build the `UnrealInsights` target (in the IDE Programs folder, or `Engine/Build/BatchFiles/RunUBT.bat
  UnrealInsights Win64 Development`).

## Capture
- Editor: the Trace button in the bottom toolbar (Trace Insights widget). Destination is Trace Store
  (managed folder) or File; Start Trace, Stop Trace, Save Trace Snapshot; options can auto-open Insights.
- Console and command line, as listed on the Trace page: `trace.start [filename]`, `trace.send [ip]`,
  `trace.screenshot`, `trace.bookmark`, `Trace.Status` (connection, memory used, channels), and
  `-trace.start [file] [channelSet] -tracehost=[ip]` or `-tracefile=[filepath]` on the command line.
- `-statnamedevents` (or the Stat Named Events checkbox) adds more named CPU timers.
- **Late connect**: important events are cached client-side and sent to late-connecting machines, so
  one-time events are not missed; Insights can tell a remote instance to connect (Unreal Insights >
  Connect).
- **Tail tracing** keeps the last few seconds of events; default buffer 4MB, change with `-tracetailmb=X`
  (0 turns it off).

## Channels (selection)
Channels control the data rate: events are emitted only if their channel is on. Defaults per the page:
Bookmark, Cpu, Frame, Gpu, Log, Region, Screenshot. Others include Counters, File, LoadTime, AssetLoadTime,
MemAlloc, MemTag, Module, Net, Task, Stats, Callstack, ContextSwitch (on Windows run as administrator),
Cpu timers and Metadata. MemAlloc, MemTag and Module must be enabled from the command line. Define your
own presets in the `[Trace.ChannelPresets]` config category.

## Reading a trace
Timing Insights shows the Frames panel, Timing panel with CPU and GPU tracks, Log panel, Timers and Counters
tabs, and Callers and Callees panels. Bookmarks and screenshots appear in the markers track under the ruler
and bookmarks in the Log view. Live sessions show LIVE in the status column and update while you analyse
them. Memory Insights records every allocation, reallocation and free and reconstructs memory use during
analysis; see its own documentation for setup.

## Not verified here
Custom scope macros (`TRACE_CPUPROFILER_EVENT_SCOPE` and variants), Blueprint scopes, and build
configuration requirements for tracing in Shipping are not covered by the two cited pages; check the Trace
Developer Guide and the Unreal Insights Reference.

## Verify
- [ ] The trace opens in Unreal Insights and the Frames panel shows the captured session.
- [ ] Channels enabled match what you intend to analyse.

## Checked
Checked 2026-11-08 against the Unreal Insights and Trace pages.
Confirmed: components, server behaviour, port, storage locations, kill command, UE 5.3 note, channels and
defaults, capture commands, tail tracing, late connect, panel names.
Removed because the pages do not state them: the `-trace=default,memory,task` channel set examples,
custom scope macros and their cost claims, Blueprint scope notes, Shipping and Test build requirements,
version-matching and Debug-timing advice.
Method: docs-only read of cited pages, 2026-11-08
