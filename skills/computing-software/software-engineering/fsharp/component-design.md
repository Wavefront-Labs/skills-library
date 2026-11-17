---
id: computing-software.software-engineering.fsharp.component-design
name: component-design
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, component-design, fsharp-style, library-guidelines, api-design]
level: advanced
status: draft
description: "Design public F# library APIs following the component design guidelines: modules versus classes, naming, errors and compatibility."
sources:
  - https://learn.microsoft.com/en-us/dotnet/fsharp/style-guide/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Component design guidelines
**Goal:** a library others can consume.

- Namespaces and types at the top level; modules for related functions; keep module names singular or plural consistently.
- Provide a `[<RequireQualifiedAccess>]` module for functions over a type (`Customer.create`).
- Use `Result`/`option` for expected failure; throw exceptions for programmer errors (argument validation).
- Prefer interfaces or records of functions over deep inheritance; make types sealed by default where inheritance is not intended.
- Public tupled method arguments for C# callers; keep curried functions for F#-first APIs.
- Do not expose `list` or F# unions in APIs consumed from C#.
- Add `[<CompiledName>]` for .NET naming of module functions.
- Mark unstable APIs `internal` or document them; version with SemVer; keep FSharp.Core low.
- Minimise generic type annotation noise but annotate public functions fully.
- Write XML doc comments (`///`) on public API.

## Gotchas
- A breaking record change (field order or addition) affects binary compatibility.
- Annotate public functions: inference changes can silently alter public signatures.

## Self-check
Review a public module against this list and a `.fsi` signature file.
