---
id: computing-software.software-engineering.fsharp.github-actions-ci
name: github-actions-ci
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, github-actions-ci, fsharp-ci, github-actions, setup-dotnet]
level: practitioner
status: draft
description: "Build, test and format-check F# on GitHub Actions with setup-dotnet, NuGet caching and Fantomas."
sources:
  - https://docs.github.com/en/actions
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# GitHub Actions
**Goal:** a reliable CI pipeline.

```yaml
name: ci
on:
  push:
    branches: [main]
  pull_request:
permissions:
  contents: read
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-dotnet@v4
        with:
          global-json-file: global.json
      - run: dotnet tool restore
      - run: dotnet fantomas --check .
      - run: dotnet restore
      - run: dotnet build -c Release --no-restore
      - run: dotnet test -c Release --no-build --logger trx
```
- `setup-dotnet` can read the SDK version from `global.json`.
- Cache NuGet packages with `actions/cache` keyed on `**/*.fsproj` and `Directory.Packages.props` (or enable caching in setup-dotnet when lock files exist).
- Set minimal `permissions` and pin actions to a major version or commit SHA.
- Add a matrix over operating systems when you ship cross-platform.

## Gotchas
- `dotnet test` on Expecto needs the test SDK adapter or run the project via `dotnet run`.
- Action versions above are illustrative; use currently supported majors.

## Self-check
A PR with unformatted code fails the Fantomas step.
