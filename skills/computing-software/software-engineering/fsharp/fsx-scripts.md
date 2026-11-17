---
id: computing-software.software-engineering.fsharp.fsx-scripts
name: fsx-scripts
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, fsx-scripts, fsharp-fsi, fsx, script-nuget]
level: practitioner
status: draft
description: "Write standalone .fsx scripts that reference NuGet packages and accept command-line arguments."
sources:
  - https://learn.microsoft.com/en-us/dotnet/core/tools/
  - https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# .fsx scripts
**Goal:** one-file tools without a project.

```fsharp
#r "nuget: FSharp.Data, 6.4.0"
open FSharp.Data

let args = fsi.CommandLineArgs |> Array.skip 1
printfn "args: %A" args
let doc = Http.RequestString "https://example.com"
printfn "%d bytes" doc.Length
```
```bash
dotnet fsi tool.fsx arg1 arg2
```
- `#r "nuget: Package, Version"` restores at script load; omit the version for the latest.
- `fsi.CommandLineArgs.[0]` is the script name.
- `#load "helpers.fsx"` includes other scripts; `__SOURCE_DIRECTORY__` and `__SOURCE_FILE__` give paths.
- `#!/usr/bin/env -S dotnet fsi` shebang works on Unix (unconfirmed, depends on env flavour).
- Version above is illustrative.

## Gotchas
- NuGet restore in scripts depends on network and the nearest `nuget.config`.
- Top-level `let` duplicates are allowed in scripts but not in compiled files.

## Self-check
Run `dotnet fsi tool.fsx a b` and confirm the printed args.
