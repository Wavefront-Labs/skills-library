---
id: computing-software.software-engineering.fsharp.rider-visual-studio
name: rider-visual-studio
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, rider-visual-studio, fsharp-ide, rider, visual-studio]
level: intro
status: draft
description: "Use JetBrains Rider and Visual Studio for F# projects including file ordering, debugging and Fantomas."
sources:
  - https://ionide.io/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Rider and Visual Studio
**Goal:** know IDE alternatives and their F# specifics.

- JetBrains Rider has first-class F# support (refactorings, debugger, test runner, Fantomas plugin for formatting).
- Visual Studio supports F# project templates, IntelliSense, F# Interactive window and debugging; the F# workload ships with the "F# desktop language support" component.
- Both let you reorder files in the project (move up/down) which updates `Compile Include` order.
- Test discovery works with Expecto (via YoloDev.Expecto.TestSdk), xUnit and NUnit adapters.
- Nullable/analyzer/CI behaviour should be driven by the repo (`.editorconfig`, `Directory.Build.props`), not IDE settings.

## Gotchas
- IDE-specific build settings can differ from `dotnet build`; verify in CI.
- Large solutions may need to unload unused projects to stay responsive.

## Self-check
Create a new F# console app in the IDE and confirm it builds identically with `dotnet build`.
