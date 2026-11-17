---
id: computing-software.game-programming.game-engine-architecture.tracy-instrumented-profiling
name: tracy-instrumented-profiling
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, tracy, instrumented-profiling, profiler-zones, frame-markers, gpu-zones, memory-profiling, game-programming]
level: practitioner
status: docs-checked
description: "Instrument a C++ engine with Tracy: build setup, zone, frame, lock, memory and GPU macros, thread names, and capturing with tracy-capture."
sources: ["https://github.com/wolfpld/tracy/releases/latest/download/tracy.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tracy instrumented profiling

**Goal:** a timeline of every thread in the engine, frame by frame, so hitches and thread stalls are visible (Tracy by
Bartosz Taudul).

## Integration
- Add `public/TracyClient.cpp` to the build and define `TRACY_ENABLE` for the whole project. Without it the
  instrumentation is compiled out and the client does nothing. In CMake, `TRACY_ENABLE` defaults to OFF.
- `TRACY_ON_DEMAND`: collect data only while the profiler is connected, instead of from program launch.
- `TRACY_NO_EXIT`: do not let the client exit until all profiling data has been sent; for short-lived applications set the
  `TRACY_NO_EXIT` environment variable to 1.
- Use the same Tracy version on client and server; the network protocol may change between releases and then the
  connection fails.
- Capture without the GUI with `tracy-capture` (for example `./tracy-capture -a 127.0.0.1 -o trace`). Ctrl+C disconnects
  and saves; `-s seconds` disconnects after a fixed time. `tracy-capture-daemon` captures several clients to separate
  files by listening for their UDP broadcasts.

## Macros
- `ZoneScoped` at the start of a scope records function name, file and location. `ZoneScopedC(color)` sets a constant
  colour, `ZoneScopedN(name)` a custom name, `ZoneScopedNC(name, color)` both.
- `ZoneText(text, size)` attaches a string to a zone (several allowed); `ZoneValue(uint64_t)` sends a number without string
  conversion cost; `ZoneColor(uint32_t)` sets a dynamic colour; `ZoneIsActive` tells whether the zone is active.
- `FrameMarkNamed("name")` marks secondary frame sets.
- `TracyPlot` graphs a value over time. `TracyMessageL(text)` posts a string-literal message.
- `TracyLockable(std::mutex, m_lock)` instruments a lock.
- Memory: `TracyAlloc(ptr, size)` and `TracyFree(ptr)` in your allocator. For a separate pool use the named versions
  `TracyAllocN(ptr, size, name)` and `TracyFreeN(ptr, name)`, where name is a unique pointer to a string literal.
- GPU: `TracyVkZone`, `TracyD3D12Zone` and `TracyGpuZone` (OpenGL), with `TracyVkCollect` and `TracyD3D12Collect` called
  to gather results.
- Name threads with `tracy::SetThreadName(name)` from `public/common/TracySystem.hpp`; `SetThreadNameWithHint(name,
  groupHint)` groups threads in the UI (0 is the main thread's group).
- A C API exists, for example `TracyCZone`.
- With `TRACY_ON_DEMAND`, do not skip the zone's active check where the manual calls for it.

## Checked
Date: 2026-11-09. Read via pdftotext: the Tracy manual (tracy.pdf, latest release): sections on setup, build options,
macros, naming threads, memory, GPU and tracy-capture. The GitHub README was not read. Removed as not confirmed: the
"few nanoseconds per zone" cost, the sampling-on-admin note, `ZoneScoped` usage examples with the per-frame `FrameMark`
placement, the timeline reading checklist, the `-o trace.tracy` file name, and the verify steps.
Method: docs-checked 2026-11-09 against the Tracy manual PDF (tracy.pdf).
