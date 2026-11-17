---
id: computing-software.game-programming.unreal-engine.memreport-and-llm-memory-tracking
name: memreport-and-llm-memory-tracking
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, ue5, performance, memreport, low-level-memory-tracker, llm, memory-insights, obj-list, game-programming]
level: advanced
status: docs-checked
description: "Find memory usage in Unreal with the Low Level Memory Tracker (-LLM, stat LLM, custom tags) and Memory Insights traces and allocation queries."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/using-the-low-level-memory-tracker-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/memory-insights-in-unreal-engine"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LLM and Memory Insights

**Goal:** know what is using memory and find growth or leaks.

## Low-Level Memory Tracker
LLM is a scoped-tag system that accounts for memory allocated by the engine and OS. Two trackers: the Default Tracker
(allocations through `FMemory` Malloc; feeds `stat LLM` and `stat LLMFULL`) and the lower-level Platform Tracker (all OS
allocations, so Default stats are a subset).
| Command line | Effect |
|---|---|
| `-LLM` | enable LLM |
| `-LLMCSV` | continuously write values to CSV; enables `-LLM` |
| `-llmtagsets=Assets` / `AssetClasses` | experimental: totals per asset / per UObject class |
Console: `stat LLM` (summary, lower engine stats grouped as Engine), `stat LLMFULL` (all), `stat LLMPlatform` (OS
allocations), `stat LLMOverhead` (LLM's own memory). The CSV goes to `saved/profiling/llm/`, one column per tag in
MB, a new line every 5 seconds by default; change with the `LLM.LLMWriteInterval` console variable.
- Tag categories on the page include UObject, EngineMisc, TaskGraphTasksMisc and StaticMesh. Tags are applied with
  scope macros and LLM uses the top of its tag stack for each allocation.
- Custom tags (no engine edits, usable in game modules or plugins): declare `LLM_DECLARE_TAG(MyTestTag);` in a header,
  define `LLM_DEFINE_TAG(MyTestTag);` in a `.cpp`, and wrap code in `LLM_SCOPE_BYTAG(MyTestTag);`. Names must be
  unique across all tags. `LLM_DEFINE_TAG` also takes optional DisplayName, ParentTagName, StatName and SummaryStatName.
  Use them when Memory Insights shows allocations tagged "LLM Untracked".
- Tag Sets are experimental and need `LLM_ALLOW_ASSETS_TAGS` defined in `LowLevelMemTracker.h`; they add memory and
  runtime overhead.
- Builds: LLM is completely compiled out in Shipping; in Test it can run without the stats system (no on-screen
  stats, CSV still written) after changing `ENABLE_LOW_LEVEL_MEM_TRACKER` in `LowLevelMemTracker.h`. The page says
  overhead can be 100 MB or more, so use large memory mode on consoles.

## Memory Insights
Run the game with the memory trace channel from process start (late-connect cannot start allocation tracing), for
example `MyGameSample.exe -trace=default,memory`; add `metadata,assetmetadata` for per-asset and per-class costs. A
packaged project must be Development mode. Open the `.utrace` in Unreal Insights, then Menu > Memory Insights.
- Panels: Timing, Investigation, LLM Tags, Modules. Graphs include Total Allocated Memory, Live Allocation Count and
  Allocation/Free Event Count, plus LLM-tag tracks.
- Investigation queries use a rule and time markers A, B (and C, D): Active Alloc, Before, After, Decline, Growth,
  Growth Vs Decline, Free Events, Alloc Events, Short Living Allocs, Long Living Allocs, Memory Leaks (allocated between
  A and B, not freed until after C; the page's example is a level transition), Limited Lifetime, Decline of Long
  Living Allocs, Specific Lifetime. Press Run Query; queries can take a long time.
- Results can be grouped (for example Tags, Asset, Class Name, Alloc Callstack) and exported with Export Snapshot to
  .csv or .tsv.
- Callstack symbols need the matching .pdb or .elf; Insights searches paths you enter, the executable path,
  `UE_INSIGHTS_SYMBOLPATH` (semicolon-separated), `_NT_SYMBOL_PATH`, then the user config.
- The page notes UE5.4 and later supports memory tracing with callstacks on Android.

## Verify
- [ ] A `-LLMCSV` run writes a CSV under `saved/profiling/llm/` with a column for each tag.
- [ ] A custom tag declared, defined and scoped as above appears in `stat LLMFULL`.

## Checked
Date: 2026-11-07.
Read in full: Low-Level Memory Tracker (all sections including macro parameters and implementation details) and Memory
Insights (all sections including every query rule). dev.epicgames.com; no engine version for LLM, UE5.4 noted for Android above.
Removed as unconfirmed: the whole `memreport -full` / `obj list` / `listtextures` / `rhi.DumpMemory` section (not on
either cited page; the skill's name keeps the old id), `LLM_ENABLED_IN_CONFIG`, "compiled in Development/Test by
default", `r.Streaming.PoolSize` and `stat streaming`, the example platform budgets, CI soak advice, and 30-minute soak
and 10 percent headroom Verify steps.
Method: documentation only; no commands were run.
