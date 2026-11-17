---
id: computing-software.software-engineering.csharp-dotnet.diagnosing-builds-with-msbuild-binlogs
name: diagnosing-builds-with-msbuild-binlogs
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, msbuild-binlog, structured-log-viewer, build-performance, slow-builds, build-diagnostics, msbuild]
level: advanced
status: docs-checked
description: "Diagnose broken or slow .NET builds with MSBuild binary logs: capturing -bl in CI, Structured Log Viewer searches, tracing property values, timing analysis."
sources: ["https://learn.microsoft.com/en-us/visualstudio/msbuild/obtaining-build-logs-with-msbuild", "https://msbuildlog.com/", "https://github.com/dotnet/msbuild/blob/main/documentation/wiki/Binary-Log.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Diagnosing builds with MSBuild binlogs

**Goal:** answer "why did this build fail / pick that version / take 6 minutes"
from a single complete record instead of guesswork.

## Capture
```bash
dotnet build -bl                         # msbuild.binlog in the current directory
dotnet build -bl:logs/build.binlog
dotnet test -bl  /  dotnet publish -bl  /  msbuild -bl
```
- Records every property, item, target, task, message and timing - far more than `-v:diag` text
  logs, and smaller.
- CI: always pass `-bl` and upload the file as an artifact on failure.
- Contains environment variables and command lines - check for secrets before sharing publicly.

## Read with MSBuild Structured Log Viewer
Install from msbuildlog.com (Windows app; cross-platform Avalonia version and a web viewer exist).

Use the viewer's search box (query syntax: see msbuildlog.com) to find:
- errors and warnings with their project and target context;
- where a property or item value was set and by which import;
- why a target ran or was skipped;
- the exact compiler command line of the Csc task.

The **Timeline** and **Tracing** tabs show which projects/targets dominate wall time and
whether nodes run in parallel.

## Common findings
- Wrong package version: property/item tracing shows a `Directory.Packages.props` or
  transitive pin overriding yours.
- "Target X skipped because of condition": the evaluated condition is visible on the target node.
- Incremental build broken: a target without Inputs/Outputs or a file touched every build
  (timestamps) makes CoreCompile run each time.
- Slow restore: NuGet restore task time with many feeds; enable lock files / fewer sources.

## Command-line alternatives
The MSBuild command-line reference lists switches for querying evaluation and for the preprocessed project.

## Checked
2026-10-28: Confirmed in the MSBuild build logs page, msbuildlog.com and the binary log wiki: -bl switch, viewer, timeline, sensitive data caution. Removed unverified search-query syntax, the Project System Tools extension, ReportAnalyzer and the -getProperty/-pp switches.
Method: documentation only; no commands were run.

## Verify
- [ ] CI uploads binlogs for failed builds.
- [ ] Build-time regressions investigated with the Timeline before tweaking flags.
