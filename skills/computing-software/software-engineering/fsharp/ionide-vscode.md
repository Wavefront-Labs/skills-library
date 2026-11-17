---
id: computing-software.software-engineering.fsharp.ionide-vscode
name: ionide-vscode
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, ionide-vscode, fsharp-ide, ionide, fsautocomplete]
level: intro
status: draft
description: "Set up Ionide in VS Code with FsAutoComplete, project loading, analyzers and FSI integration."
sources:
  - https://ionide.io/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Ionide
**Goal:** a productive F# editor setup.

- Install the "Ionide for F#" extension; it runs FsAutoComplete (the language server) and needs the .NET SDK.
- Open the folder containing the `.sln` or `.fsproj`; Ionide loads projects via MSBuild and shows them in the Solution Explorer.
- Useful features: inline type hints, signature help, rename, find references, code fixes, test explorer (with the .NET test adapter).
- Send selected code to F# Interactive with Alt+Enter; `Alt+/` sends the current line.
- Settings of interest (JSON settings): `FSharp.enableAnalyzers`, `FSharp.inlayHints.enabled`, `FSharp.fsac.netCoreDllPath`; confirm names in extension docs.
- Format on save via Fantomas: set `editor.formatOnSave` and `[fsharp]` default formatter to Ionide.

## Gotchas
- If project load hangs, run `dotnet restore` and check `global.json` SDK availability.
- Stale `obj` folders cause phantom errors; clean.

## Self-check
Hover over a pipeline stage and confirm the inferred type tooltip appears.
