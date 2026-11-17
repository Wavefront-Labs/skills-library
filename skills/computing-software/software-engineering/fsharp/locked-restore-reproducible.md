---
id: computing-software.software-engineering.fsharp.locked-restore-reproducible
name: locked-restore-reproducible
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, locked-restore-reproducible, fsharp-ci, nuget-lock-file, locked-mode]
level: advanced
status: draft
description: "Make restores reproducible with RestorePackagesWithLockFile, locked mode and package source mapping."
sources:
  - https://learn.microsoft.com/en-us/nuget/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Locked restores
**Goal:** the same package graph every time.

```xml
<PropertyGroup>
  <RestorePackagesWithLockFile>true</RestorePackagesWithLockFile>
</PropertyGroup>
```
```bash
dotnet restore                    # writes packages.lock.json
dotnet restore --locked-mode      # fails if the graph differs
```
`nuget.config` with package source mapping:
```xml
<configuration>
  <packageSources>
    <clear />
    <add key="nuget.org" value="https://api.nuget.org/v3/index.json" />
  </packageSources>
  <packageSourceMapping>
    <packageSource key="nuget.org"><package pattern="*" /></packageSource>
  </packageSourceMapping>
</configuration>
```
- Commit `packages.lock.json`; run `--locked-mode` in CI.
- Pair with `Deterministic` builds and `global.json` for full reproducibility.
- Source mapping reduces dependency confusion risk when you add private feeds.
- Paket's `paket.lock` serves the same purpose for Paket-managed repos.

## Gotchas
- Lock files get noisy with floating versions (`1.*`); pin versions.
- Changing target frameworks changes the lock file.

## Self-check
Edit a package version and see `--locked-mode` fail until the lock file is regenerated.
