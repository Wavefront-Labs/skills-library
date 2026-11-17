---
id: computing-software.software-engineering.fsharp.fsdocs-site
name: fsdocs-site
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, fsdocs-site, fsharp-docs, fsdocs, literate-programming]
level: practitioner
status: draft
description: "Generate API reference and tutorial pages from F# code and markdown/.fsx literate files with the fsdocs tool."
sources:
  - https://learn.microsoft.com/en-us/dotnet/fsharp/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# fsdocs
**Goal:** a docs site from your repo.

```bash
dotnet new tool-manifest
dotnet tool install fsdocs-tool
dotnet fsdocs watch          # local preview with live reload
dotnet fsdocs build --clean  # outputs to output/
```
- Content lives in a `docs/` folder as `.md` and `.fsx` (literate scripts with `(** markdown *)` blocks and evaluated code output).
- API reference is generated from the XML doc comments of projects packable as libraries (needs `GenerateDocumentationFile` and a Release build).
- Project metadata (`<RepositoryUrl>`, `<Authors>`, `<Description>`) feeds the site template; `_template.html` customises layout.
- Publish `output/` to GitHub Pages in CI.
- Option names for fsdocs evolve; run `dotnet fsdocs --help` on your installed version.

## Gotchas
- Docs build fails if the library has not been built in Release first.
- Literate script code runs during the docs build, so it can fail the pipeline.

## Self-check
`dotnet fsdocs watch` serves a page listing your public module.
