---
id: computing-software.game-programming.unreal-engine.writing-an-unreal-plugin
name: writing-an-unreal-plugin
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, ue5, unreal-build-tool, unreal-plugin, uplugin, plugin-modules, loading-phase, game-features, content-plugin, game-programming]
level: practitioner
status: docs-checked
description: "Create an Unreal plugin: folder layout, .uplugin descriptor fields, module types, content plugins, plugin dependencies, icon, and Game Feature plugins with Add Components actions."
sources:
  - https://dev.epicgames.com/documentation/en-us/unreal-engine/plugins-in-unreal-engine
  - https://dev.epicgames.com/documentation/en-us/unreal-engine/game-features-and-modular-gameplay-in-unreal-engine
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Writing an Unreal plugin

**Goal:** a self-contained feature reusable across projects, with code and/or content of its own.

## Create and locate
Use the New Plugin button in the editor's Plugin Browser, pick a plugin type, name it and set basic
parameters; it appears enabled in the current project. Plugins are found only in search paths:

| Type | Path |
|---|---|
| Engine | `[Engine root]/Engine/Plugins/[Plugin Name]/` |
| Game | `[Project root]/Plugins/[Plugin Name]/` |

Subdirectories under `Plugins` are scanned, but the engine never scans beneath a plugin it already found.

## Anatomy
- `.uplugin` descriptor (JSON; the file name before the extension is the plugin name), found automatically by
  the engine, editor and UBT.
- `Source` (module source; one or more module directories, each with a `.Build.cs`), `Binaries` (compiled
  code), `Intermediate` (temporary build files), optional `Content`.
- Icon: a 128x128 `.png` named `Icon128.png` in the plugin's `Resources` directory.
- Config files: engine plugins use `[PluginName]/Config/Base[PluginName].ini`, game plugins
  `[PluginName]/Config/Default[PluginName].ini`. Plugin config files are not packaged with projects
  at present (copy them to the project's Config folder). Plugins do not support their own Derived Data
  Cache distribution.
- A plugin need not contain code. Plugins with a `Source` folder are added to generated IDE project files
  and compiled with the game; plugins without one still load at start-up if binaries exist.

## Descriptor
```json
{
  "FileVersion": 3,
  "VersionName": "1.0",
  "FriendlyName": "My Plugin",
  "CanContainContent": true,
  "Modules": [
    { "Name": "MyPlugin", "Type": "Runtime", "LoadingPhase": "Default" }
  ]
}
```
- `FileVersion` is the only required field; it versions the descriptor format, not your plugin. Epic says to
  use the highest the engine allows (currently 3) and not change it with your releases.
- Other fields come from `FPluginDescriptor`; boolean field names drop the leading `b`
  (`bEnabledByDefault` becomes `EnabledByDefault`). The Engine's own example adds `Version`, `Description`,
  `Category`, `CreatedBy`, `EnabledByDefault`, `IsBetaVersion` and more.
- Each `Modules` entry requires `Name` and `Type`. Valid types: Runtime, RuntimeNoCommandlet, Developer,
  Editor, EditorNoCommandlet, Program. Runtime loads everywhere including shipped games; Developer loads in
  development runtime or Editor builds but never in shipping; Editor loads only when the editor starts up. A
  plugin may mix module types, and a module with a `Source` directory needs a matching `.Build.cs`.
- `CanContainContent` must be `true` for a plugin to hold content.
- Dependencies: plugins enable other plugins in their own `.uplugin`; project modules enable plugins in the
  `.uproject`. Dependencies may only point at the same or a higher level (a project module may depend on an
  engine module, never the reverse).
- Loading-phase values and module loading behaviour are covered in the Modules documentation; for names
  such as `PreDefault` see the `ELoadingPhase` API reference.

## Reflected types
Plugins can declare `UCLASS`, `USTRUCT` and so on in module headers; the build system generates the code.
Follow the normal rules for UObjects in C++ modules (include the generated header and the module's
`generated.inl` in one source file).

## Game Feature plugins
Enable the Game Features and Modular Gameplay plugins (Gameplay category) and restart. Add a plugin with
type Game Feature (Content Only) saved under `/Plugins/GameFeatures/` in the project. Create a Data Asset of
class `GameFeatureData`, named like the plugin; actions go in its Actions array. Restart the editor once if a
newly created GameFeatureData asset does not work (it loads at editor startup).
- Actions: Add Cheats, Add Components, Add Data Registry, Add Data Registry Source, Add World Partition
  Content.
- Add Components pairs Actor and Component classes and adds the component to matching Actors on clients,
  servers or both (default both). Using the base `AActor` class is unsupported and ignored; choose the
  narrowest Actor subclass. Receiving Actors must register in `BeginPlay`:
```cpp
if (UGameFrameworkComponentManager* ComponentManager =
        GetGameInstance()->GetSubsystem<UGameFrameworkComponentManager>())
{
    ComponentManager->AddReceiver(this);
}
```
- Cheat Manager extensions do not instantiate in Shipping builds.

## Distribution
The Plugin Browser has a Package link that packages a plugin into a folder for distribution. If you
precompile for UE 5.2, Epic says to compile with Visual Studio 2019, its minimum supported version.

## Verify
- [ ] The plugin folder dropped into a fresh project compiles and its content loads.
- [ ] Module types match where each module should load.

## Checked
Checked 2026-11-08 against the Plugins and Game Features and Modular Gameplay pages.
Confirmed: search paths, anatomy, descriptor fields and module types, content flag, dependency rule, Game
Feature setup and actions, `AddReceiver` sample, packaging note.
Removed because the pages do not state them: `RunUAT BuildPlugin` flags, `UDeveloperSettings` snippet,
`MYPLUGIN_API`, `UncookedOnly` and the loading-phase table, "Editor never packaged", and the plugin-reference
rule for content.
Method: docs-only read of cited pages, 2026-11-08
