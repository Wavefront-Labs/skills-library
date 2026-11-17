---
id: computing-software.software-engineering.fsharp.fsharplint
name: fsharplint
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, fsharplint, fsharp-analysis, linter, fsharplint-config]
level: practitioner
status: draft
description: "Lint F# for style and correctness with FSharpLint and its config."
sources:
  - https://github.com/ionide/FSharp.Analyzers.SDK
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# FSharpLint
**Goal:** style lint in CI.

```bash
dotnet tool install dotnet-fsharplint
dotnet fsharplint lint MySln.sln
dotnet fsharplint lint src/App/App.fsproj
```
`fsharplint.json` (excerpt):
```json
{
  "ignoreFiles": ["*.fsi"],
  "hints": { "add": ["not (a = b) ===> a <> b"] }
}
```
- Rules cover naming, formatting limits (line length, function length), and hints that rewrite patterns.
- Configure rules in `fsharplint.json` at the repo root; unconfirmed: the exact rule names and `hints` syntax, see the project documentation.
- It complements, not replaces, warnings-as-errors and Fantomas.

## Gotchas
- Rule defaults can be noisy; start with a small enabled set.
- Lint results depend on project builds; run after `dotnet build`.

## Self-check
Run the linter on a file with a deliberately badly named function and confirm a warning.
