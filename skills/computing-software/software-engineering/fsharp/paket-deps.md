---
id: computing-software.software-engineering.fsharp.paket-deps
name: paket-deps
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, paket-deps, fsharp-paket-fake, paket, paket-lock]
level: practitioner
status: draft
description: "Manage NuGet dependencies with Paket using paket.dependencies, paket.references and paket.lock."
sources:
  - https://fsprojects.github.io/Paket/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Paket
**Goal:** repeatable dependency resolution with a lock file.

```bash
dotnet new tool-manifest
dotnet tool install paket
dotnet paket init
dotnet paket add FSharp.Data --project src/App/App.fsproj
dotnet paket install
dotnet paket update
dotnet paket outdated
```
`paket.dependencies`:
```
source https://api.nuget.org/v3/index.json
storage: none
nuget FSharp.Core
nuget Expecto
```
- Per-project `paket.references` lists the packages a project uses; `paket.lock` pins the full graph (commit it).
- Supports git/GitHub file dependencies and per-group dependencies.
- Paket integrates with MSBuild restore, so `dotnet build` works after `paket install`.

## Gotchas
- Mixing PackageReference in .fsproj and Paket for the same package causes duplicates.
- Without `paket.lock` committed, CI resolves a different graph.

## Self-check
Delete `packages/`, run `dotnet restore`, and confirm builds pass from the lock file.
