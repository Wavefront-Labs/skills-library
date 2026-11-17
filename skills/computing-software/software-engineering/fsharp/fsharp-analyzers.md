---
id: computing-software.software-engineering.fsharp.fsharp-analyzers
name: fsharp-analyzers
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, fsharp-analyzers, fsharp-analysis, analyzers-sdk, code-analysis]
level: advanced
status: docs-checked
description: "Run F# analyzers built on FSharp.Analyzers.SDK from the command line runner against a project and an analyzers path."
sources:
  - https://github.com/ionide/FSharp.Analyzers.SDK
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# F# analyzers
**Goal:** extra static checks beyond the compiler.

- FSharp.Analyzers.SDK (Ionide) is a library for building custom analyzers for FSAC and F# editors. Analyzers are live, project-based plugins that diagnose source code and surface custom errors, warnings and code fixes in the editor.
- The repository includes a command-line runner project, FSharp.Analyzers.Cli. The README's sample run passes `--project <fsproj>` and `--analyzers-path <folder with built analyzer>` and optionally `--verbosity d`:

```
dotnet run --project src\FSharp.Analyzers.Cli\FSharp.Analyzers.Cli.fsproj -- --project ./samples/OptionAnalyzer/OptionAnalyzer.fsproj --analyzers-path ./artifacts/bin/OptionAnalyzer/release --verbosity d
```
- To build the repo: install the .NET SDK version in `global.json`, run `dotnet tool restore`, then `dotnet build -c Release`.
- The README points to separate Getting Started guides for analyzer users and for analyzer authors; follow those for current attribute and context types.
- The README says the repo ships an agent skill (`upgrade-fsharp-analyzers`) that upgrades the fsharp-analyzers tool and analyzer packages to matching versions and re-runs them.

## Self-check
Run the sample OptionAnalyzer command above and confirm diagnostics are printed.

## Checked

Method: docs-checked 2026-11-09 against the FSharp.Analyzers.SDK GitHub README. Removed unconfirmed: Ionide setting names, G-Research analyzers, `[<CliAnalyzer>]` code sample, version-matching and build-time gotchas, `dotnet fsharp-analyzers` tool name.
