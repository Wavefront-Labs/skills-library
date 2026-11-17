---
id: computing-software.software-engineering.fsharp.modules-namespaces
name: modules-namespaces
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, modules-namespaces, fsharp-modules, module-declaration, open-declaration]
level: intro
status: docs-checked
description: "Organise F# code into namespaces and top-level, local and nested modules."
sources:
  - https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Modules and namespaces
**Goal:** structure a codebase.

```fsharp
namespace MyApp.Domain

type Customer = { Id: int; Name: string }

module CustomerModule =
    let create id name = { Id = id; Name = name }

module Internal =
    let secret = 42
```
- A top-level module declaration can appear only as the first declaration in a file and covers the whole file; a file without one gets an implicit top-level module named after the file.
- Local modules nested in a namespace or module need their contents indented.

## Gotchas
- A top-level module declaration needs no indentation; local modules do.

## Self-check
Put two modules in one file and one nested module in another, and confirm both forms compile.

## Checked
2026-11-03. Confirmed against the Modules and Namespaces language-reference pages (top-level versus local modules, implicit top-level module, namespace contents). Removed: compile-order and Compile Include claims, `open type`, CompilationRepresentation, the Module-suffix merge, RequireQualifiedAccess on modules, rec modules and AutoOpen.
Method: documentation only; no commands were run.
