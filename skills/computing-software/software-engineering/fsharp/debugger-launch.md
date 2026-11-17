---
id: computing-software.software-engineering.fsharp.debugger-launch
name: debugger-launch
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, debugger-launch, fsharp-debug, debugger, breakpoints]
level: practitioner
status: draft
description: "Attach a debugger to F# programs with launch configurations, breakpoints and watch expressions, and know F# debugging quirks."
sources:
  - https://ionide.io/
  - https://learn.microsoft.com/en-us/dotnet/core/tools/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Debugging F#
**Goal:** step through code reliably.

`.vscode/launch.json` (VS Code with a .NET debugger extension):
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": ".NET Launch",
      "type": "coreclr",
      "request": "launch",
      "program": "${workspaceFolder}/src/App/bin/Debug/net8.0/App.dll",
      "args": [],
      "cwd": "${workspaceFolder}/src/App",
      "preLaunchTask": "build"
    }
  ]
}
```
- Debug builds (default) keep locals and disable tailcalls; use them to debug.
- Breakpoints inside pipelines can hit per stage; use "step into" for lambdas.
- Debugging `async`/`task` state machines: locals appear inside generated closures; the debugger may show compiler-generated names.
- Inline functions and optimised builds lose debug info; debug in `-c Debug`.
- Quick trace: `x |> tee (printfn "%A")` where `tee f x = f x; x` is a user-defined helper.
- Rider and Visual Studio have built-in .NET debuggers with F# support; Ionide uses the coreclr adapter you install.

## Gotchas
- `printfn "%A"` on huge structures is slow and may hide the issue.
- Source link mismatches cause breakpoints to show as unbound; rebuild without stale `obj`.

## Self-check
Set a breakpoint on the first line of `main` and confirm it hits.
