---
id: computing-software.software-engineering.fsharp.msbuild-binlog
name: msbuild-binlog
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, msbuild-binlog, fsharp-compiler, binlog, build-diagnostics]
level: advanced
status: draft
description: "Diagnose slow or failing F# builds with verbosity flags, binary logs and compiler timing."
sources:
  - https://learn.microsoft.com/en-us/dotnet/core/tools/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Build diagnostics
**Goal:** find out why a build misbehaves.

```bash
dotnet build -v:d
dotnet build -bl                      # writes msbuild.binlog
dotnet msbuild -pp:out.xml MyApp.fsproj   # preprocessed project
dotnet build -p:Configuration=Release -clp:ErrorsOnly
```
- Open `msbuild.binlog` with the MSBuild Structured Log Viewer (third party) to see targets, properties and compiler command lines.
- `-pp` prints the project after imports, showing which props files apply.
- Unconfirmed: fsc has a `--times` timing flag; check `dotnet fsc --help` on your SDK.
- Slow F# builds: large files, heavy inline/SRTP, type providers, and complex inference; split projects.

## Gotchas
- Binlogs may contain secrets in properties; scrub before sharing.
- Stale `obj/` folders cause odd errors; `dotnet clean` or delete `bin`/`obj`.

## Self-check
Produce a binlog and locate the `Fsc` task command line in the viewer.
