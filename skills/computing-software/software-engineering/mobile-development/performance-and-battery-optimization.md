---
id: computing-software.software-engineering.mobile-development.performance-and-battery-optimization
name: performance-and-battery-optimization
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, performance, battery, jank, main-thread, cold-start, wakelock, android, ios, background-jobs, frame-drops, systrace, instruments, battery-historian]
level: advanced
status: draft
description: "Diagnose mobile jank (dropped frames), slow cold-start, and battery drain from wakelocks and background jobs, with the platform profilers that find each."
sources: ["Android developer docs - Perfetto/systrace, Doze and App Standby, WorkManager", "Apple docs - Instruments Time Profiler, Energy Log", "personal mobile app profiling experience"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Mobile performance and battery — jank, cold start, and what drains the battery

**Goal:** diagnose dropped frames, slow app launch, and battery complaints with the
platform's own profiler instead of guessing which code path is "probably slow."

## 1. Jank: anything on the main/UI thread over one frame budget
A 60fps display needs each frame rendered in ~16.6ms (90/120Hz displays: tighter).
Any main-thread work exceeding that — JSON parsing, a synchronous DB query, bitmap
decoding, even an unexpectedly large layout pass — drops a frame, visible as a stutter.
- **Android**: Perfetto/systrace (`adb shell perfetto` or Android Studio's Profiler)
  shows frame timing and exactly which main-thread call exceeded budget; `Choreographer`
  logs ("Skipped N frames!") in logcat are a cheap first signal.
- **iOS**: Instruments' Time Profiler + the "Hangs" detector surfaces main-thread
  work over a threshold directly, with a symbolized stack.
Fix: move the offending work off the main thread (`Dispatch.global()`/`Task` on iOS,
coroutines/`WorkManager` or a background thread on Android) or make it genuinely
cheaper (cache the decode, paginate the list, avoid synchronous I/O entirely on the
UI thread).

## 2. Cold start time
Time from tap-to-launch to first interactive frame, split into phases:
- **Process creation + framework init** — mostly fixed cost, limited developer
  control beyond keeping the app's own static initializers light.
- **Application/App class init** — eagerly initializing every SDK, DI graph, and
  singleton at startup is the most common self-inflicted cold-start cost; defer
  anything not needed for the first screen (lazy-init analytics SDKs, defer non-critical
  network calls until after first paint).
- **First screen render** — avoid blocking the first screen on a network call;
  render from cache/placeholder data first, fetch in the background.
Android's `androidx.tracing`/`Macrobenchmark` library and iOS's "App Launch"
Instruments template both give a phase breakdown instead of just a single number —
use them to find which phase is actually the long pole before optimizing blindly.

## 3. Battery drain: wakelocks, background work, and radios
- **Wakelocks (Android)**: holding a `PARTIAL_WAKE_LOCK` keeps the CPU awake even
  with the screen off — any wakelock held longer than the task that needs it (a
  forgotten `release()`, an exception path that skips it) drains battery with the
  screen off, which is the single most common root cause of a "drains battery
  overnight" complaint. Always `release()` in a `finally`, and prefer `WorkManager`
  with the "idle" constraint over a manual wakelock for deferrable work — the
  system can batch and schedule it instead of your app forcing wakefulness.
- **Background jobs run too often**: a periodic sync/location poll scheduled more
  frequently than the use case needs is the second most common drain. Respect
  Android's Doze/App Standby batching windows rather than requesting exemptions by
  default; on iOS, `BGTaskScheduler` similarly batches to OS-chosen windows — fighting
  the system scheduler (frequent wake requests, `requestAlwaysOnLocation` when
  "when in use" suffices) is the actual drain, not the work itself.
- **Radios**: GPS/cellular/Bluetooth kept active longer than needed cost
  disproportionately more than CPU — batch network calls instead of many small
  requests waking the radio repeatedly ("radio tail" — the radio stays active for
  seconds after a request completes, so 10 small staggered requests cost far more
  than 1 batched one).
- **Diagnosis tools**: Android's Battery Historian (or `adb shell dumpsys batterystats`)
  attributes wakelock/radio time to specific apps and components; iOS's Instruments
  Energy Log shows per-component energy impact directly.

## Gotchas
- A background job scheduled with the tightest "run ASAP, exact time" constraint
  defeats the OS's batching optimizations (which exist specifically to coalesce many
  apps' wake requests into one radio/CPU wake window) — use the loosest constraint
  the feature can tolerate.
- Image decoding at full resolution for a thumbnail-sized view wastes both CPU (jank)
  and memory — decode at the target display size (`BitmapFactory.Options.inSampleSize`
  on Android, `UIGraphicsImageRenderer` sized appropriately on iOS), not full size
  then scale down in a view.
- Profiling in a debug build understates real performance (debug builds disable many
  compiler optimizations) — always profile a release/profile-configuration build for
  numbers you'll act on.

## Verify
- [ ] Jank was diagnosed with Perfetto/systrace or Instruments showing the specific
      main-thread call over budget, not guessed from a general "feels slow" report.
- [ ] Cold-start time is measured by phase (framework/app-init/first-render), with the
      actual long pole identified before optimizing.
- [ ] Every wakelock has a `release()` reachable from every exit path, including
      exceptions.
- [ ] A battery-drain report was attributed to a specific component via Battery
      Historian or Energy Log before any fix was applied.

Related: computing-software.software-engineering.mobile-development.app-lifecycle-and-offline-sync,
computing-software.software-engineering.concurrency.profiling-before-optimising
