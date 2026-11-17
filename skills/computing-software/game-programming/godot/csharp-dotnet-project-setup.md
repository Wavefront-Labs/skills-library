---
id: computing-software.game-programming.godot.csharp-dotnet-project-setup
name: csharp-dotnet-project-setup
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, godot-csharp, godot-dotnet, csproj, dotnet-sdk, partial-class, nuget, external-editor, game-programming, godot-nuget]
level: practitioner
status: docs-checked
description: "Set up C# in Godot 4: the .NET editor build, SDK requirement, generated solution and csproj, NuGet packages, external editors, debugging and export limits."
sources: ["https://docs.godotengine.org/en/stable/tutorials/scripting/c_sharp/c_sharp_basics.html", "https://docs.godotengine.org/en/stable/tutorials/scripting/c_sharp/c_sharp_differences.html", "https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_web.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# C# (.NET) project setup in Godot 4

**Goal:** a Godot project with C# scripts that builds, debugs in an IDE and exports to the target
platforms.

## Requirements
- Install the **.NET SDK** and use the **.NET-enabled** build of Godot. Godot bundles only what is needed to
  run compiled games, not MSBuild or the C# compiler. Match 64-bit SDK to 64-bit Godot.
- The docs state Godot 4.5 requires .NET 8 or later (Android export needs .NET 9 or later); check the
  C# basics page for your Godot version.
- The first C# script generates a solution (`.sln`) and project file (`.csproj`) plus utility files and
  `.godot/mono`. Commit everything except `.godot/mono`; deleting `.godot/mono` and letting it regenerate
  can help when troubleshooting.

## Script shape
```csharp
using Godot;

public partial class YourCustomClass : Node
{
    public override void _Ready() { GD.Print("Hello from C# to Godot :)"); }
    public override void _Process(double delta) { }
}
```
- The class must be `partial`, and its name must match the `.cs` file name or the editor reports
  "Cannot find class XXX for script res://XXX.cs".
- The C# API uses PascalCase instead of snake_case; global GDScript functions live in the static `GD` class.
- Rebuild the assemblies (Build button, top right of the editor) to see new exported variables or signals
  in the editor, and to apply changes in tool scripts.
- Methods such as `Get()/Set()`, `Call()/CallDeferred()` and `Connect()` expect the original snake_case
  names (`CallDeferred("add_child")`, not `"AddChild"`); prefer the `PropertyName`, `MethodName` and
  `SignalName` StringNames.
- Struct properties return copies: `Position.X = 100.0f` fails with CS1612; copy the struct, change it and
  assign it back.

## NuGet
Add a `PackageReference` inside an `ItemGroup` of the `.csproj`; Godot downloads and sets up new packages the
next time it builds. If you see "Unable to find package Godot.NET.Sdk", the NuGet configuration may be
wrong; the docs suggest renaming or deleting `NuGet.Config` in the user NuGet folder so it regenerates.

## IDE
Editor > Editor Settings > Dotnet > Editor > External Editor. Supported: Visual Studio 2022, Visual Studio
Code, MonoDevelop, Visual Studio for Mac, JetBrains Rider. Rider needs the Godot plugin only below version
2024.2. VS Code needs the C# extension plus a `tasks.json` (runs `dotnet build`) and a `launch.json`
(type `coreclr`, `program` pointing at the Godot executable, for example via a `GODOT4` environment
variable). Visual Studio uses the `.NET desktop development` workload and an Executable debug profile
pointing at the main (not console) Godot executable with working directory `.`.

## Export limits
- Godot 4 C# projects currently cannot be exported to the web platform.
- Android and iOS support is available from Godot 4.2 but is experimental with limitations; desktop
  (Linux, Windows, macOS) export is supported.

## Gotchas
- Hot reload does not save and restore state, except for exported variables.
- Calls into the engine are native interop calls; cache property values in locals inside loops and avoid
  implicit string to `NodePath`/`StringName` conversions in hot code.

## Verify
- [ ] `dotnet build` succeeds from the project folder.
- [ ] Exports appear in the inspector after a build.

## Checked
2026-11-08. Read in full: C# basics page (prerequisites, editors, project files, partial class and file name
rule, rebuild, snake_case caveat, CS1612, NuGet, export limits, performance notes). Removed unconfirmed
claims: the example csproj contents and version numbers, the signal `EventHandler` suffix rule, platform
version claims beyond the docs, runtime size and Variant marshalling statements, and the no-SDK desktop
run check. The code sample is illustrative and was not run.
Method: documentation only; no commands were run.
