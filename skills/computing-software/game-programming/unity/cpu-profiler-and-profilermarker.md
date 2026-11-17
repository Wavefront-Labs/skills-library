---
id: computing-software.game-programming.unity.cpu-profiler-and-profilermarker
name: cpu-profiler-and-profilermarker
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-profiler, profiler, cpu-profiler, profilermarker, timeline-view, profile-analyzer, game-programming]
level: practitioner
status: docs-checked
description: "Read Unity's CPU Usage Profiler module (chart categories, Timeline and Hierarchy views, columns), add ProfilerMarker instrumentation, and know what Profile Analyzer compares."
sources: ["https://docs.unity3d.com/Manual/ProfilerCPU.html", "https://docs.unity3d.com/ScriptReference/Unity.Profiling.ProfilerMarker.html", "https://docs.unity3d.com/Packages/com.unity.performance.profile-analyzer@1.2/manual/index.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CPU Profiler and ProfilerMarker

**Goal:** read the CPU Usage Profiler module and instrument your own code with `ProfilerMarker`.

## CPU Usage module
- Chart tracks main thread time in categories: Rendering, Scripts, Physics, Animation, GarbageCollector,
  VSync (waiting for `targetFrameRate` or the next VBlank), Global Illumination, UI, Others (includes the
  EditorLoop and profiling overhead in Play mode).
- Details pane view dropdown (default Timeline):
  - **Timeline**: breakdown of one frame on a time axis; the only view showing all threads at once so you
    can correlate timings across threads (for example job workers starting after the main thread
    schedules them).
  - **Hierarchy**: groups timing data hierarchically, ordered by time by default, or by scripting
    memory allocated, or number of calls.
  - **Raw Hierarchy**: separate call stacks, not merged. **Inverted Hierarchy**: groups by marker with
    inverted stacks; helps reveal many small impacts.
- Live setting is off by default and increases `EditorLoop` overhead when the Profiler window repaints.
  Thread selector and Details dropdown (No Details, Related data, Calls) appear in Hierarchy views.
- Hierarchy columns: Total and Self (percent of frame time), Calls (always 1 in Raw Hierarchy), GC Alloc
  (scripting heap allocated this frame), Time ms, Self ms (excludes sub functions), Warning. Time ms may
  mislead with the job system or multithreaded rendering since it covers only the selected thread.
- Show Flow events (Timeline only) connects samples that schedule and wait on jobs.
  Collapse EditorOnly samples is on by default in Hierarchy views.

## ProfilerMarker (`Unity.Profiling`, struct)
- Marks script code blocks for the Profiler; shows in the CPU Profiler and can be captured with a
  Recorder, during development in the Editor and Development Players. The page calls it the most
  efficient way of profiling code and says it can be used in jobified code.
- `Begin` and `End` have `ConditionalAttribute`, so they compile away with zero overhead in
  non-Development builds. `Auto()` returns a helper struct for `using` blocks.
- `Profiler.BeginSample` transfers the full string; `ProfilerMarker.Begin` and `CustomSampler.Begin`
  transfer only an integer identifier.
- Page example:
  ```csharp
  static readonly ProfilerMarker s_Prepare = new ProfilerMarker("MySystem.Prepare");
  static readonly ProfilerMarker s_Simulate = new ProfilerMarker(ProfilerCategory.Ai, "MySystem.Simulate");
  s_Prepare.Begin(); /* ... */ s_Prepare.End();
  using (s_Simulate.Auto()) { /* ... */ }
  ```

## Profile Analyzer package (1.2)
Aggregates and visualizes frame and marker data from a set of Profiler frames, and compares two sets of
data side-by-side. Compatible with Editor 2020.3 and later. Known limitations: the `.pdata` file does not
contain the original profile data, so keep the Profiler `.data` (or the `.raw` from a standalone player)
alongside it.

## Checked
Date: 2026-11-07

Read in full: the CPU Usage module reference, the `ProfilerMarker` page and the Profile Analyzer package
index. The Profiler window and Profile Analyzer window sub-pages were not opened.

Removed because none of the pages confirm it: Development Build and Autoconnect Profiler steps, the
menu path, the Deep Profile overhead note, wait markers such as `Gfx.WaitForPresent`, the GPU-bound
reading, the "Self ms to find hot functions" workflow, `ProfilerRecorder` overlays, comparing medians
over hundreds of frames, the whole "Common culprits" marker table and the Verify list.

Method: documentation only; no commands were run.
