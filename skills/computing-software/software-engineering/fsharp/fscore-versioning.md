---
id: computing-software.software-engineering.fsharp.fscore-versioning
name: fscore-versioning
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, fscore-versioning, fsharp-nuget, fsharp-core-version, disable-implicit-fsharp-core]
level: advanced
status: draft
description: "Manage FSharp.Core versions: why libraries should target an older FSharp.Core and how consumers resolve it."
sources:
  - https://learn.microsoft.com/en-us/dotnet/fsharp/style-guide/
  - https://learn.microsoft.com/en-us/nuget/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# FSharp.Core versioning
**Goal:** avoid FSharp.Core conflicts.

```xml
<PropertyGroup>
  <TargetFramework>netstandard2.0</TargetFramework>
</PropertyGroup>
<ItemGroup>
  <PackageReference Update="FSharp.Core" Version="6.0.0" />
</ItemGroup>
```
- Every F# project references the `FSharp.Core` NuGet package implicitly (the SDK adds it); the compiler version brings a default version.
- Libraries should reference the lowest FSharp.Core that supplies the APIs they need, so applications can raise it; applications decide the final version.
- `<DisableImplicitFSharpCoreReference>true</DisableImplicitFSharpCoreReference>` turns off the implicit reference.
- FSharp.Core is backwards compatible: newer FSharp.Core works with code compiled against older, not the reverse.
- Version numbers here are illustrative; check the library design guidelines.

## Gotchas
- Binding redirect style conflicts appear as `MissingMethodException` at runtime when an old FSharp.Core wins.
- `dotnet list package --include-transitive` shows which FSharp.Core resolves.

## Self-check
Run `dotnet list package` and confirm the resolved FSharp.Core version.
