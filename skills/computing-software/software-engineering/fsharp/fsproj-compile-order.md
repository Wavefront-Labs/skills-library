---
id: computing-software.software-engineering.fsharp.fsproj-compile-order
name: fsproj-compile-order
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, fsproj-compile-order, fsharp-project, fsproj, compile-order]
level: intro
status: draft
description: "Structure an F# project file where Compile Include order defines dependencies, and set common properties."
sources:
  - https://learn.microsoft.com/en-us/dotnet/fsharp/
  - https://learn.microsoft.com/en-us/dotnet/core/tools/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# .fsproj and compile order
**Goal:** lay out an F# project correctly.

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>net8.0</TargetFramework>
    <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
    <GenerateDocumentationFile>true</GenerateDocumentationFile>
  </PropertyGroup>
  <ItemGroup>
    <Compile Include="Domain.fs" />
    <Compile Include="Logic.fs" />
    <Compile Include="Program.fs" />
  </ItemGroup>
  <ItemGroup>
    <PackageReference Include="FSharp.Data" Version="6.4.0" />
    <ProjectReference Include="..\Lib\Lib.fsproj" />
  </ItemGroup>
</Project>
```
- F# has no wildcard globbing for source: every file is listed in `<Compile Include>` and order is the dependency order (a file sees only files above it).
- The last file holds `[<EntryPoint>]` for an exe.
- Version numbers above are illustrative; pick current ones with `dotnet add package`.
- `dotnet new console -lang "F#"` / `classlib` / `xunit` scaffold projects.
- `<Compile Include="x.fs" />` order edits can be done with IDE move up/down commands (Ionide, Rider, VS).

## Gotchas
- Forgetting to add a new file to the project produces "not defined" errors although the file exists.
- Circular dependencies are impossible across files; move shared types earlier.

## Self-check
Move `Domain.fs` below `Logic.fs` and observe the compile error.
