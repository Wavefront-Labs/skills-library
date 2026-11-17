---
id: computing-software.software-engineering.fsharp.native-aot-trimming
name: native-aot-trimming
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, native-aot-trimming, fsharp-aot, native-aot, trimming]
level: advanced
status: draft
description: "Understand Native AOT and IL trimming for F# apps and their limits around reflection, printf and FSharp.Core."
sources:
  - https://learn.microsoft.com/en-us/dotnet/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Native AOT and trimming
**Goal:** know the constraints before committing.

```xml
<PropertyGroup>
  <PublishAot>true</PublishAot>          <!-- or PublishTrimmed for IL trimming -->
  <InvariantGlobalization>true</InvariantGlobalization>
</PropertyGroup>
```
```bash
dotnet publish -c Release -r linux-x64
```
- Native AOT compiles to a self-contained native binary with fast startup and no JIT; it needs the platform native toolchain installed.
- Reflection-heavy features break: `%A` printf formatting, reflection-based serialisers, quotation evaluation, `FSharpValue`/`FSharpType` helpers, and some computation expression libraries.
- FSharp.Core support for trimming/AOT is partial; expect trim warnings (IL2026 and similar). Confirm current status in release notes (unconfirmed).
- Use source-generated serialisation (System.Text.Json `JsonSerializerContext`) where possible; compatibility with F# unions/options is limited.
- Test the published binary; behaviours differ from JIT runs.

## Gotchas
- A project can build and pass tests but fail at AOT publish or at runtime.
- Cross-compilation of AOT is limited; build on the target OS/arch.

## Self-check
Publish a hello-world with `PublishAot` and run the resulting executable without .NET installed.
