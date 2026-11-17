---
id: computing-software.software-engineering.fsharp.test-coverage
name: test-coverage
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, test-coverage, fsharp-test-practice, coverlet, code-coverage]
level: practitioner
status: draft
description: "Collect and report test coverage for F# projects using Coverlet and ReportGenerator."
sources:
  - https://learn.microsoft.com/en-us/dotnet/core/tools/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Coverage
**Goal:** measure which code tests exercise.

```bash
dotnet test --collect:"XPlat Code Coverage"
dotnet tool install -g dotnet-reportgenerator-globaltool
reportgenerator -reports:"**/coverage.cobertura.xml" -targetdir:coverage -reporttypes:Html
```
- The `coverlet.collector` package (included in the xUnit template) provides the data collector.
- Output is a Cobertura XML under `TestResults/<guid>/`.
- F# generates compiler artifacts (closures, pattern-match code) that may show as uncovered branches; interpret line coverage with care.
- `[<ExcludeFromCodeCoverage>]` can exclude code, but attribute support on F# constructs is partial (unconfirmed).
- Set thresholds in CI with Coverlet MSBuild options (`/p:Threshold=80`, needs `coverlet.msbuild`).

## Gotchas
- Inline functions are not attributed to the original definition lines.
- Coverage numbers differ between Debug and Release.

## Self-check
Open `coverage/index.html` and confirm the tested module appears.
