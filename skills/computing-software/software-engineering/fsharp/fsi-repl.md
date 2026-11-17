---
id: computing-software.software-engineering.fsharp.fsi-repl
name: fsi-repl
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, fsi-repl, fsharp-fsi, fsi, repl]
level: intro
status: draft
description: "Evaluate F# interactively with dotnet fsi, double-semicolon terminators, directives and timing."
sources:
  - https://learn.microsoft.com/en-us/dotnet/core/tools/
  - https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# F# Interactive
**Goal:** explore code in a REPL.

```bash
dotnet fsi
> let x = 1 + 2;;
val x : int = 3
> #time "on";;
> #help;;
> #quit;;
```
- `;;` terminates an input submission in the console REPL (not needed in scripts or VS Code selection execution).
- Directives: `#r "path.dll"`, `#r "nuget: Pkg"`, `#load "file.fsx"`, `#I "dir"`, `#time "on"`, `#quit`, `#help`.
- `dotnet fsi --use:init.fsx` runs an init script first; `--exec` runs and exits.
- In VS Code with Ionide: select code and press Alt+Enter to send it to FSI.
- `it` holds the last unbound value.

## Gotchas
- State persists in the session; restart to recompile cleanly.
- FSI runs with different defaults from compiled builds (script mode, debug optimisations).

## Self-check
Evaluate `#time "on";; List.sum [1..1000000];;` and read the timing output.
