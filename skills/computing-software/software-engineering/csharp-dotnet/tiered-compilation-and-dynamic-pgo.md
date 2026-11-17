---
id: computing-software.software-engineering.csharp-dotnet.tiered-compilation-and-dynamic-pgo
name: tiered-compilation-and-dynamic-pgo
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, dotnet, jit, tiered-compilation, dynamic-pgo, readytorun, quick-jit, performance, runtime-config]
level: practitioner
status: docs-checked
description: "Understand the .NET JIT tiers, Dynamic PGO (on by default since .NET 8), and the runtime settings for tiered compilation, quick JIT, ReadyToRun and PGO."
sources: ["https://learn.microsoft.com/en-us/dotnet/core/runtime-config/compilation", "https://learn.microsoft.com/en-us/dotnet/core/whats-new/dotnet-8/runtime#performance-improvements"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tiered compilation and Dynamic PGO

Tiered compilation moves methods through two tiers. The first tier generates code quickly (quick JIT) or loads pre-compiled ReadyToRun code. The second tier generates optimised code in the background (the optimising JIT). It is enabled by default in .NET Core 3.0 and later.

**Dynamic PGO** (profile-guided optimisation) lets the JIT generate code optimised for the types and code paths used most often. It works hand in hand with tiered compilation, using extra instrumentation placed during tier 0. Since .NET 8 it is enabled by default; you no longer need a runtime option to turn it on.
## Settings
| Setting | runtimeconfig.json | MSBuild property | Environment variable |
|---|---|---|---|
| Tiered compilation | `System.Runtime.TieredCompilation` | `TieredCompilation` | `DOTNET_TieredCompilation` (1 or 0) |
| Quick JIT | `System.Runtime.TieredCompilation.QuickJit` | `TieredCompilationQuickJit` | |
| Quick JIT for loops | `System.Runtime.TieredCompilation.QuickJitForLoops` | `TieredCompilationQuickJitForLoops` | `DOTNET_TC_QuickJitForLoops` (1 or 0) |
| Dynamic PGO | | `TieredPGO` | `DOTNET_TieredPGO` (1 or 0) |
| ReadyToRun use | | | `DOTNET_ReadyToRun` (1 or 0) |

```xml
<PropertyGroup>
  <TieredCompilation>true</TieredCompilation>
  <TieredPGO>true</TieredPGO>
</PropertyGroup>
```
- Quick JIT is enabled by default in .NET Core 3.0 and later. If quick JIT is disabled but tiered compilation is enabled, only pre-compiled code takes part in tiering; a method not pre-compiled with ReadyToRun is JIT-compiled as if tiered compilation were disabled.
- `DOTNET_ReadyToRun=0` forces the runtime to JIT-compile framework code instead of using ReadyToRun data. If the setting is omitted, ReadyToRun data is used when available.

## Gotchas
- Dynamic PGO optimises for the behaviour observed at run time, so a test workload unlike production can tune differently from production.
- Defaults changed between .NET Core 2.1/2.2 (tiered compilation and quick JIT off) and 3.0 (both on); check the page for your version.
- If quick JIT for loops is omitted, methods containing loops do not use quick JIT; long-running loops can stay in less-optimised code when it is enabled.

## Verify
- [ ] Compare the hot path with `DOTNET_TieredPGO=0` and `DOTNET_TieredPGO=1` on your own workload and measure steady state and cold start separately.

## Checked
2026-11-09. Confirmed on the Learn runtime configuration page for compilation (two tiers, defaults since .NET Core 3.0, the settings and their value forms for TieredCompilation, QuickJit, QuickJitForLoops, ReadyToRun and TieredPGO, quick-JIT-disabled behaviour) and the Learn .NET 8 runtime performance page (dynamic PGO enabled by default). The cited devblogs page returned 404 and was dropped from sources. Removed as not on those pages: OSR, the 30-call and 100 ms promotion thresholds, TC_CallCountThreshold and background worker settings, AggressiveOptimization and AggressiveInlining advice, warm-up, LINQ/DI and sealed-class remarks, BenchmarkDotNet and dotnet-counters instructions, performance percentages and container start-up claims.
Method: documentation only; no commands were run.
