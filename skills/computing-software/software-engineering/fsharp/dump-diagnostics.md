---
id: computing-software.software-engineering.fsharp.dump-diagnostics
name: dump-diagnostics
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, dump-diagnostics, fsharp-debug, dotnet-trace, dotnet-counters]
level: advanced
status: draft
description: "Profile and inspect running .NET processes with dotnet-trace, dotnet-counters and dotnet-dump."
sources:
  - https://learn.microsoft.com/en-us/dotnet/core/tools/
  - https://learn.microsoft.com/en-us/dotnet/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Runtime diagnostics
**Goal:** observe production-like processes without a debugger.

```bash
dotnet tool install -g dotnet-counters
dotnet tool install -g dotnet-trace
dotnet tool install -g dotnet-dump

dotnet-counters ps                          # list .NET processes
dotnet-counters monitor -p <pid>            # live GC, CPU, thread-pool counters
dotnet-trace collect -p <pid>               # writes a .nettrace file
dotnet-dump collect -p <pid>
dotnet-dump analyze <dump>                  # SOS commands, e.g. dumpheap -stat
```
- `.nettrace` files open in PerfView or Visual Studio; convert to speedscope with `dotnet-trace convert --format Speedscope`.
- GC and allocation counters expose pressure from closures, boxing and list churn typical in F#.
- Set `DOTNET_gcServer` and similar via environment variables for experiments.
- Exact subcommands/options evolve; run `--help` on your installed version.

## Gotchas
- Dumps may contain secrets in memory; handle like credentials.
- Attaching needs the same user and a matching runtime.

## Self-check
`dotnet-counters ps` lists your running app, and `monitor` shows the CPU counter changing under load.
