---
id: computing-software.software-engineering.fsharp.fantomas-formatter
name: fantomas-formatter
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, fantomas-formatter, fsharp-format-tools, fantomas, code-formatter]
level: practitioner
status: draft
description: "Install and run Fantomas to format an F# codebase and check formatting in CI."
sources:
  - https://fsprojects.github.io/fantomas/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Fantomas
**Goal:** automatic, consistent formatting.

```bash
dotnet tool install fantomas            # local tool; or -g for global
dotnet fantomas src                      # format files in place
dotnet fantomas --check src              # exits non-zero if changes are needed
dotnet fantomas src/Program.fs
```
- Install as a local tool via `dotnet new tool-manifest` then `dotnet tool install fantomas` so the version is pinned in `.config/dotnet-tools.json`.
- Formatting choices live in `.editorconfig` (see the next skill).
- Format-on-save integrates with Ionide, Rider (Fantomas plugin) and Visual Studio extensions.
- Exclude files with a `.fantomasignore` file (gitignore syntax).
- Fantomas can fail on invalid code; fix compile errors first.

## Gotchas
- Different Fantomas versions format slightly differently; pin the version and format the whole repo on upgrade in one commit.
- `--check` in CI only works if developers format with the same version.

## Self-check
Run `dotnet fantomas --check .` after reformatting and expect exit code 0.
