---
id: computing-software.game-programming.unreal-engine.csv-profiler-automated-captures
name: csv-profiler-automated-captures
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, csvprofile, csv-profiler, performance, automation, game-programming]
level: practitioner
status: draft
description: "Capture Unreal CSV profiler stats from test runs: csvprofile commands and switches, CSV_SCOPED stats and events, PerfReportTool reports and regression tracking."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/csv-profiler-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/perfreporttool-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/stat-commands-in-unreal-engine"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# CSV profiler automated captures

**Goal:** frame-by-frame stat logs from soak tests and flythroughs, turned into comparable reports.

## Capture
- Console: `csvprofile start`, `csvprofile stop`, `csvprofile frames=3000`.
- Command line: `-csvprofile`, `-csvCaptureFrames=3000`, `-csvExecCmds="stat unit"`, plus
  `-ExecCmds="Automation RunTest MyFlythrough"` or a Gauntlet test for repeatable paths.
- Output: `Saved/Profiling/CSV/Profile(<date>).csv` with per-frame columns (FrameTime, GameThreadTime,
  RenderThreadTime, GPUTime, memory, draw calls, plus categories enabled with
  `csvcategory <name>`), and events (`-csvMetadata=build=123`).

## Instrument code
```cpp
CSV_DEFINE_CATEGORY(AI, true);
void UMyAISubsystem::Tick(float Dt) {
    CSV_SCOPED_TIMING_STAT(AI, Tick);
    CSV_CUSTOM_STAT(AI, ActiveAgents, Agents.Num(), ECsvCustomStatOp::Set);
}
CSV_EVENT(AI, TEXT("WaveStart %d"), Wave);
```
CSV stats are cheap enough for Test builds (unlike full stat system); available in Shipping only with
`CSV_PROFILER` enabled in the target.

## Reports
`PerfReportTool` (Engine/Binaries/DotNET/CsvTools) turns CSVs into HTML reports with graphs and summary
tables: `PerfReportTool.exe -csv Profile.csv -o Reports`. Report types (XML in
`Engine/Source/Programs/CsvTools/PerfReportTool/ReportTypes.xml`) define which stats and budgets
appear. `-csvdir` for batches; summary tables compare builds. CsvToSVG draws specific stats.

## Workflow
Nightly: run the flythrough on target hardware, upload CSV and report, track median/95th percentile
frame time and hitches per map. Regressions alert before content lock.

## Gotchas
- VSync and frame rate caps hide headroom; run with `t.MaxFPS 0` and VSync off for perf captures.
- Long captures produce big files; cap frames or use categories.

## Verify
- [ ] Each nightly build produces a report; budgets flag regressions automatically.
