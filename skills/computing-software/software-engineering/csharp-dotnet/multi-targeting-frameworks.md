---
id: computing-software.software-engineering.csharp-dotnet.multi-targeting-frameworks
name: multi-targeting-frameworks
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, multi-targeting, targetframeworks, conditional-compilation, netstandard, polyfills, nuget]
level: advanced
status: docs-checked
description: "Ship one .NET library for several runtimes: TargetFrameworks, choosing netstandard2.0 vs net8.0, #if NET8_0_OR_GREATER, per-TFM dependencies, polyfills and testing each target."
sources:
  - https://learn.microsoft.com/en-us/dotnet/standard/library-guidance/cross-platform-targeting
  - https://learn.microsoft.com/en-us/dotnet/standard/frameworks
  - https://learn.microsoft.com/en-us/nuget/create-packages/multiple-target-frameworks-project-file
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multi-targeting frameworks

**Goal:** one NuGet package that works on .NET Framework and modern .NET, using new
APIs where available without forking the code.

## Choosing targets
Microsoft's cross-platform library guidance:
- DO start with a `net8.0` target or later for new libraries: modern .NET gives access to the latest APIs and performance improvements and enables features like AOT and trimming. (.NET 10 is the current LTS release.)
- CONSIDER a `netstandard2.0` target if you need broad compatibility or .NET Framework support; it is supported by .NET Framework 4.6.1+ and all modern .NET implementations.
- AVOID `netstandard1.x`; and do not publish a `netstandard2.0` target if your project or dependencies multi-target in a way that needs a runtime-specific library.
- Do not include a .NET Standard target if the library relies on a platform-specific app model.

```xml
<PropertyGroup>
  <TargetFrameworks>netstandard2.0;net8.0;net10.0</TargetFrameworks>   <!-- plural! -->
</PropertyGroup>
```

## Conditional code
```csharp
#if NET8_0_OR_GREATER
    return string.Create(len, state, static (span, s) => Fill(span, s));
#else
    var chars = new char[len]; Fill(chars, state); return new string(chars);
#endif
```
The SDK defines preprocessor symbols per target framework (for example `NETSTANDARD2_0`, `NET8_0` and `NET8_0_OR_GREATER`; see the preprocessor symbols reference). Keep
`#if` blocks small and isolate differences in a few helper files.

## Per-target dependencies
```xml
<ItemGroup Condition="'$(TargetFramework)' == 'netstandard2.0'">
  <PackageReference Include="Microsoft.Bcl.AsyncInterfaces" Version="x.y.z" />   <!-- pick the version you need -->
</ItemGroup>
```
Use conditional `ItemGroup`s so a package is only referenced for the target frameworks that need it.

## Building and testing
```bash
dotnet build                          # builds every TFM
dotnet build -f net8.0                # one TFM (faster inner loop)
dotnet test                           # test project can multi-target too
```

## Gotchas
- `TargetFramework` (singular) vs `TargetFrameworks` (plural): use the plural form for several targets; a singular property in the project can override it.
- Keep the `#if` guards consistent with the `TargetFrameworks` list so a missing target fails loudly (the NuGet docs use `#error` in an `#else` branch for this).

## Verify
- [ ] `dotnet pack` output contains `lib/netstandard2.0` and `lib/net8.0` folders.
- [ ] Tests run on the oldest and newest targets in CI.

## Checked

Checked 2026-10-25 against dotnet/docs (standard/library-guidance/cross-platform-targeting, standard/frameworks, includes/preprocessor-symbols) and NuGet/docs.microsoft.com-nuget (multiple-target-frameworks-project-file) on main.
Confirmed: library targeting recommendations (net8.0 or later for new libraries; netstandard2.0 when broad or .NET Framework compatibility is needed, supported by .NET Framework 4.6.1+; avoid netstandard1.x); `TargetFrameworks` plural form; per-TFM preprocessor symbols; conditional references per target framework; `#error` guard pattern; .NET 10 is an LTS release (dotnet/core release notes).
Wrong in the draft: the guidance no longer recommends netstandard2.0 first and "net8.0 (current LTS)" is stale.
Removed as unconfirmed: PolySharp and polyfill package claims, `IsTrimmable` condition, `EnablePackageValidation`, the Framework-on-Windows test note, the netstandard2.1 remark, the pinned package versions.

Method: documentation only; no commands were run.
