---
id: computing-software.software-engineering.fsharp.langversion-features
name: langversion-features
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, langversion-features, fsharp-compiler, langversion, preview-features]
level: practitioner
status: draft
description: "Select the F# language version and opt into preview features, checking what each SDK supports."
sources:
  - https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/compiler-options
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Language versions
**Goal:** pin the language for libraries, try previews on purpose.

```xml
<PropertyGroup>
  <LangVersion>8.0</LangVersion>          <!-- or latest, preview -->
</PropertyGroup>
```
```bash
dotnet fsi --langversion:?
dotnet fsc --langversion:preview
```
- `--langversion:?` lists supported versions for the installed compiler.
- Each .NET SDK bundles one F# version (for example SDK 8 bundles F# 8); choose SDKs deliberately.
- Notable additions by version: F# 4.7 implicit yields, F# 5 `open type` and string interpolation, F# 6 `task` and `[<InlineIfLambda>]`, F# 8 shorthand `_.Property` lambdas; check the official what's-new pages to confirm.
- `latest` is the default with the SDK; `preview` enables unreleased features that can break.

## Gotchas
- Library authors pinning an old LangVersion keep consumers on older toolchains happy.
- Preview features need preview SDKs on every machine in CI.

## Self-check
`dotnet fsi --langversion:?` prints the allowed values.
