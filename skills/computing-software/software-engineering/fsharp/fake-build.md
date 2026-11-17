---
id: computing-software.software-engineering.fsharp.fake-build
name: fake-build
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, fake-build, fsharp-paket-fake, fake, build-fsx]
level: advanced
status: draft
description: "Write build targets in F# with FAKE (build.fsx) including Target.create, dependencies and running."
sources:
  - https://fake.build/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# FAKE
**Goal:** script the build in F#.

```fsharp
#r "paket: nuget Fake.Core.Target nuget Fake.DotNet.Cli //"
#load ".fake/build.fsx/intellisense.fsx"

open Fake.Core
open Fake.DotNet
open Fake.Core.TargetOperators

Target.initEnvironment ()

Target.create "Clean" (fun _ -> Shell.cleanDir "out")
Target.create "Build" (fun _ -> DotNet.build id "MySln.sln")
Target.create "Test" (fun _ -> DotNet.test id "MySln.sln")

"Clean" ==> "Build" ==> "Test"

Target.runOrDefault "Test"
```
- Install with `dotnet tool install fake-cli`, run `dotnet fake build -t Test`.
- `==>` declares ordering dependencies, `<=>` soft ordering.
- Module names such as `Fake.IO.Shell` and `Fake.DotNet.DotNet` come from separate NuGet packages declared in `#r "paket:..."`.
- Unconfirmed: the `Shell.cleanDir` namespace and `DotNet.build` signature changed across FAKE 5 to 6; verify against the FAKE docs for your version.

## Gotchas
- First run restores packages and can be slow.
- Plain `dotnet build` plus MSBuild or a Makefile is often enough; FAKE shines for multi-step pipelines.

## Self-check
`dotnet fake build -t Clean` runs only the Clean target.
