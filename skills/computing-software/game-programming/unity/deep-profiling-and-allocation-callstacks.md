---
id: computing-software.game-programming.unity.deep-profiling-and-allocation-callstacks
name: deep-profiling-and-allocation-callstacks
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-profiler, deep-profiling, allocation-callstacks, gc-alloc-tracking, game-programming]
level: practitioner
status: docs-checked
description: "What Unity's Profiler instruments by default, what Deep Profile adds and costs, how to enable it for a build or the Editor, and the GC Alloc and Calls columns."
sources: ["https://docs.unity3d.com/Manual/profiler-deep-profiling.html", "https://docs.unity3d.com/Manual/ProfilerCPU.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deep profiling

**Goal:** know what the Profiler records by default and when Deep Profile is worth its cost.

## Default instrumentation
- The Profiler only profiles code explicitly wrapped in Profiler markers. That includes the first call
  stack depth of Unity native calls into your scripts, such as `MonoBehaviour.Start` and `Update`.
- Child samples of your script code are only calls into instrumented Unity APIs, or your own code with
  explicit Profiler marker instrumentation. Most API calls with a performance overhead are instrumented;
  for example `Camera.main` registers as a `FindMainCamera` sample.

## Deep Profile
- Injects profiler instrumentation into all your script methods to record all function calls, including
  at least the first call stack depth into any Unity API.
- Resource-intensive and uses a lot of memory, so the application runs significantly slower. It works best
  for small games with simple scripting; complex script code may not be usable, and for many larger
  applications Deep Profiling might make Unity run out of memory.
- Built application: File > Build Profiles, select the target platform, enable Development Build, enable
  Deep Profiling.
- Editor: Window > Analysis > Profiler, select Deep Profile on the Profiler toolbar; it instruments all
  calls when you start a profiling session.

## Reading allocations in the CPU module
Hierarchy views have a GC Alloc column (scripting heap memory allocated in the current frame) and a Calls
column. Ordering by scripting memory allocated is available in Hierarchy view. Collapse EditorOnly
samples is on by default; collapsed samples' GC.Alloc does not add to the enclosing sample.

## Checked
Date: 2026-11-07

Read in full: "Instrument all function calls" and the CPU Usage Profiler module reference. The
"Profiler markers introduction" and "Introduction to collecting performance data" pages were not opened.

Removed because neither page confirms it: the Call Stacks toolbar option for GC.Alloc and its low
overhead, "domain reload" when toggling Deep Profile, the 2-10x slowdown figure, the claim that tiny
methods are inflated most, the ProfilerMarker sample and `ProfilerRecorder` note, the list of common
allocation sources (foreach, LINQ, boxing, `GetComponents`, `RaycastAll`, `WaitForSeconds`), both
Gotchas and the Verify list. This skill is now thin: the allocation call stack workflow in the title
could not be confirmed from the cited pages.

Method: documentation only; no commands were run.
