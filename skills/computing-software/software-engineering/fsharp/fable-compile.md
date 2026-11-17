---
id: computing-software.software-engineering.fsharp.fable-compile
name: fable-compile
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, fable-compile, fsharp-fable, fable, fsharp-to-javascript]
level: practitioner
status: draft
description: "Compile F# to JavaScript with the Fable tool, wiring it to a bundler such as Vite for a dev loop."
sources:
  - https://fable.io/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Fable
**Goal:** run F# in the browser or Node.

```bash
dotnet new tool-manifest
dotnet tool install fable
dotnet fable                        # compile the project in the current folder, output .fs.js
dotnet fable watch --run npx vite   # unconfirmed option wiring; see Fable docs
```
```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup><TargetFramework>net8.0</TargetFramework></PropertyGroup>
  <ItemGroup><Compile Include="App.fs" /></ItemGroup>
  <ItemGroup><PackageReference Include="Fable.Core" Version="4.*" /></ItemGroup>
</Project>
```
- Fable compiles an ordinary F# project to ES modules (`App.fs.js`); a bundler (Vite, webpack) packages them.
- `dotnet fable` supports other targets (TypeScript, Python, Rust, Dart) as options; unconfirmed per-target status, see Fable docs.
- Only a subset of the .NET BCL is supported; JS libraries are used through bindings.
- Elmish/Feliz for UI are separate packages.

## Gotchas
- Code using reflection or .NET-only APIs fails at compile or runtime in JS.
- `Fable.Core` version must match the Fable tool major version.

## Self-check
Compile a `printfn "hi"` program and run the generated `.js` with Node.
