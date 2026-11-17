---
id: computing-software.software-engineering.mobile-development.android-studio-profiler-and-xcode-instruments
name: android-studio-profiler-and-xcode-instruments
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, android-profiler, xcode-instruments, perfetto, time-profiler, system-trace, profileable, performance]
level: advanced
status: draft
description: "Profile mobile apps with the Android Studio Profiler, Perfetto system traces and Xcode Instruments (Time Profiler, Allocations, Hitches) on release-like builds."
sources: ["https://developer.android.com/studio/profile", "https://developer.android.com/studio/profile/profileable", "https://perfetto.dev/docs/", "https://developer.apple.com/documentation/xcode/improving-your-app-s-performance", "https://developer.apple.com/tutorials/instruments"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Android Studio Profiler and Xcode Instruments

**Goal:** find the real cause of slowness, jank, memory growth or battery drain with measurements
from a build that behaves like production.

## Profile the right build
- **Android**: debuggable builds disable ART optimisations and run Compose much slower. Profile a
  release build marked profileable:
```xml
<application ...><profileable android:shell="true" /></application>
```
  Then Android Studio "Profile 'app' with low overhead" (or `adb shell am start --start-profiler`).
  Use a physical mid/low-end device, not an emulator, for timing.
- **iOS**: Product > Profile (Cmd-I) builds the Release configuration by default; profile on a
  device (the simulator uses the Mac's CPU and memory).

## Android Studio Profiler tasks
| Task | Finds |
|---|---|
| Find CPU hotspots (callstack sample / Java/Kotlin method trace) | slow code paths; sampling has low overhead, tracing is exact but distorts timing |
| Capture System Activities (system trace, Perfetto) | jank: main thread vs RenderThread, frame timeline, binder calls, lock contention, CPU scheduling |
| Track Memory Consumption (allocations) / Heap Dump | allocation churn, leaks, large bitmaps |
| Analyze Power / Energy | wakelocks, alarms, location, network radio |
- Add trace sections to your code so they show up in system traces:
```kotlin
trace("loadFeed") { repository.loadFeed() }              // androidx.tracing
Trace.beginAsyncSection("sync", cookie)                   // async work
```
  Compose: `androidx.compose.runtime:runtime-tracing` shows composable names in traces.
- Open traces in **ui.perfetto.dev** for SQL queries and richer views; record from the command line
  with `adb shell perfetto` or the on-device System Tracing app.
- Frame timeline track: red frames = missed deadline; check whether the app (main/RenderThread) or
  SurfaceFlinger caused it.

## Xcode Instruments templates
| Template | Finds |
|---|---|
| Time Profiler | CPU hotspots (enable "Hide System Libraries", "Invert Call Tree") |
| Animation Hitches / SwiftUI | hitches with commit/render phases; SwiftUI body evaluation counts and causes (Xcode 16+ SwiftUI instrument) |
| Allocations + Leaks | memory growth (mark generations between repeated actions), retain cycles |
| App Launch | pre-main, static initialisers, first frame |
| Energy Log / Power Profiler | CPU, network, location, display energy |
| Network | requests, sizes, timing (HTTP traffic instrument) |
| System Trace | thread states, blocking, priority inversions |
- Add signposts: `let signposter = OSSignposter(subsystem: "app", category: "feed")`;
  `let state = signposter.beginInterval("load")` ... `signposter.endInterval("load", state)` -
  visible as intervals in Instruments (os_signpost).
- Debug Memory Graph in Xcode for quick retain-cycle checks; MetricKit and Xcode Organizer for field
  data (launch time, hangs, disk writes) from real users.

## Method
1. Reproduce with a scripted scenario (Macrobenchmark / XCTest performance test) so before/after
   are comparable.
2. Start with a system-level view (system trace / Time Profiler) to see which thread is busy or
   blocked, then drill into method-level detail.
3. Fix the biggest contributor; re-measure; keep the trace files with the PR.

## Gotchas
- Method tracing on Android inflates the cost of small methods; prefer sampling for "where", tracing
  for "how many calls".
- First run after install includes JIT/AOT compilation on Android; warm up or use baseline profiles.
- Thermal throttling skews long sessions; let the device cool, keep it unplugged for energy tests.

## Verify
- [ ] Profiling done on a release/profileable build on a physical device.
- [ ] Trace sections/signposts mark the scenario under test.
- [ ] Before/after traces attached to the performance fix.
