---
id: computing-software.software-engineering.csharp-dotnet.dotnet-counters-and-dotnet-trace
name: dotnet-counters-and-dotnet-trace
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, dotnet, dotnet-diagnostics, dotnet-counters, dotnet-trace, eventpipe, performance, cpu-profiling]
level: practitioner
status: docs-checked
description: "Diagnose live .NET processes with dotnet-counters (GC, thread pool, exceptions, request rates) and dotnet-trace CPU/event traces, including containers and analysis tools."
sources:
  - https://learn.microsoft.com/en-us/dotnet/core/diagnostics/dotnet-counters
  - https://learn.microsoft.com/en-us/dotnet/core/diagnostics/dotnet-trace
  - https://learn.microsoft.com/en-us/dotnet/core/diagnostics/built-in-metrics
  - https://learn.microsoft.com/en-us/dotnet/core/diagnostics/diagnostics-in-containers
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# dotnet-counters and dotnet-trace

**Goal:** find out why a .NET service is slow, CPU-hot or allocating heavily, in production, without a debugger.

## 1. Install and find the process
```bash
dotnet tool install -g dotnet-counters
dotnet tool install -g dotnet-trace
dotnet-counters ps
```

## 2. dotnet-counters: first look
```bash
dotnet-counters monitor -p <pid> --counters System.Runtime,Microsoft.AspNetCore.Hosting,System.Net.Http
dotnet-counters collect -p <pid> --format csv -o counters.csv --refresh-interval 5
```
Without `--counters`, `System.Runtime` counters are monitored by default. What to look for (counter names vary by runtime version; check the built-in metrics reference):
- CPU usage, working set, GC heap size; a heap that keeps growing after Gen2 GCs is a leak candidate.
- High time in GC or a high Gen0 GC rate: allocation pressure.
- ThreadPool queue length growing and thread count climbing: sync-over-async / thread pool starvation.
- Exception count per second: exceptions used for control flow.
- Lock contention count: hot locks.
- ASP.NET Core hosting counters: request rate and current requests.

## 3. dotnet-trace: CPU and events
```bash
dotnet-trace collect -p <pid> --profile dotnet-sampled-thread-time --duration 00:00:30 -o cpu.nettrace
dotnet-trace collect -p <pid> --profile gc-verbose -o gc.nettrace          # GC collections and sampled allocations
dotnet-trace collect -p <pid> --providers Microsoft-Windows-DotNETRuntime:0x1:5    # custom keywords/level (provider:keywords:level)
dotnet-trace convert cpu.nettrace --format Speedscope
```
With no `--profile`, `--providers` or `--clrevents`, `collect` enables the `dotnet-common` and `dotnet-sampled-thread-time` profiles. Other profiles: `gc-collect` (GC only, very low overhead) and `database` (ADO.NET and EF commands). `convert --format` accepts `Chromium`, `NetTrace` and `Speedscope`. Analyse `.nettrace` files in PerfView or Visual Studio, or convert them.

## 4. Starting a process under tracing
```bash
dotnet-trace collect --profile dotnet-sampled-thread-time -- dotnet MyApp.dll
```

## 5. Containers and Kubernetes
The runtime writes a diagnostic port Unix domain socket to `/tmp`. To run the tools from a sidecar or the host, the containers must share a process namespace and share `/tmp`. If you do not want to share them, many tools support `--diagnostic-port` to name the socket directly. See the diagnostics in containers article for the details.

## Gotchas
- Keep traces short: `gc-verbose` and verbose providers add overhead; `gc-collect` is the low-overhead GC option.
- Counters are for ad-hoc inspection; use exported metrics for dashboards.

## Verify
- During a reproduced incident, counters identify the symptom class (GC, thread pool, CPU) and a 30 s CPU trace shows the hot method that explains it.

## Checked

Checked 2026-10-25 against dotnet/docs (core/diagnostics/dotnet-counters, dotnet-trace, diagnostics-in-containers) on main.
Confirmed: `collect`/`monitor`/`ps` commands, `--counters`, `--refresh-interval`, `--format csv|json` and the `System.Runtime` default; `dotnet-trace collect` profiles `dotnet-common`, `dotnet-sampled-thread-time`, `gc-verbose`, `gc-collect`, `database`; `--duration dd:hh:mm:ss`; `-- <command>` to start a process under tracing; `convert --format Chromium|NetTrace|Speedscope`; sidecar needs a shared process namespace and shared `/tmp`.
Wrong in the draft: the `cpu-sampling` profile name is not in the current profile list (now `dotnet-sampled-thread-time`).
Removed as unconfirmed: specific counter names and thresholds, `DOTNET_DiagnosticPorts` example, `kubectl debug` command, dotnet-monitor rule example, `DOTNET_EnableDiagnostics` and `TMPDIR` notes, overhead percentages.

Method: documentation only; no commands were run.
