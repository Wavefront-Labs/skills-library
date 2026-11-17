---
id: computing-software.software-engineering.csharp-dotnet.gcdump-stack-and-dotnet-monitor
name: gcdump-stack-and-dotnet-monitor
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, dotnet-diagnostics, dotnet-gcdump, dotnet-stack, dotnet-monitor, dotnet-trace, production-diagnostics]
level: advanced
status: draft
description: "Production .NET diagnostics: dotnet-gcdump for heap shape, dotnet-stack for live stacks, dotnet-trace and dotnet-monitor sidecar for on-demand dumps, traces and metrics in containers."
sources: ["https://learn.microsoft.com/en-us/dotnet/core/diagnostics/dotnet-gcdump", "https://learn.microsoft.com/en-us/dotnet/core/diagnostics/dotnet-stack", "https://learn.microsoft.com/en-us/dotnet/core/diagnostics/dotnet-monitor"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# gcdump, stack and dotnet-monitor

```bash
dotnet tool install -g dotnet-gcdump dotnet-stack dotnet-trace dotnet-counters dotnet-dump
dotnet-counters ps                                   # find process ids
dotnet-gcdump collect -p 1234 -o heap.gcdump         # managed heap graph only; small, fast, no pause of full dump
dotnet-gcdump report heap.gcdump | head -30          # types by size/count; open .gcdump in VS / PerfView for retention paths
dotnet-stack report -p 1234                          # managed stacks of every thread, no attach pause (EventPipe)
dotnet-trace collect -p 1234 --profile cpu-sampling --duration 00:00:30
```
- **gcdump** answers "what types dominate memory and what roots them". Take two dumps minutes apart under steady load and diff: growing types are the leak. It triggers a gen2 GC, so expect a pause. Contains type names and sizes, not object contents: safer than a full dump.
- **dotnet-stack** shows where threads are right now; many threads in the same blocking call means starvation/deadlock. Needs matching diagnostic IPC access to the process.
- **Full dumps** (`dotnet-dump collect --type Full`, or `DOTNET_DbgEnableMiniDump`) include secrets in memory: treat as sensitive.

## dotnet-monitor (sidecar)
Runs next to the app and exposes an authenticated REST API for dumps, traces, logs, metrics (`/dump`, `/trace`, `/gcdump`, `/livemetrics`, `/metrics` Prometheus).
```yaml
# container: share the diagnostic socket via a volume
- name: monitor
  image: mcr.microsoft.com/dotnet/monitor:8
  args: ["collect", "--urls", "http://+:52323"]
  env: [{name: DOTNET_DiagnosticPorts, value: "/diag/port,nosuspend"}]
```
Configure API key auth (`dotnet monitor generatekey`), never expose the port publicly. Collection rules can trigger a dump or trace automatically (CPU > 80% for 1 min, GC heap size), egress to Azure Blob/S3-like storage.

## Gotchas
- Containers: tool and app must share `/tmp` (diagnostic IPC socket) and the same user; read-only roots need a writable temp.
- Server GC heaps may differ in dump size; plan disk for full dumps (equals working set).
- Trace file sizes grow quickly with verbose providers.
- Production changes: dumps freeze the process unless using gcdump/stack/trace.

## Verify
`dotnet-gcdump report` lists the suspect type; after fix a second dump shows stable counts; `dotnet-stack report` shows no long-blocked threads.
