---
id: computing-software.game-programming.unreal-engine.module-build-cs-dependencies
name: module-build-cs-dependencies
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, ue5, unreal-build-tool, ubt, build-cs, modules, public-dependency-module-names, private-dependency-module-names, module-api, game-programming]
level: practitioner
status: docs-checked
description: "Structure Unreal C++ modules: Build.cs public vs private dependencies, Public/Private folders, IMPLEMENT_MODULE, .uproject module entries and regenerating project files."
sources:
  - https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-modules
  - https://dev.epicgames.com/documentation/en-us/unreal-engine/module-properties-in-unreal-engine
  - https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-build-tool-in-unreal-engine
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Module Build.cs dependencies

**Goal:** game code split into modules that compile separately, expose only what other modules need,
and load when intended.

## Module anatomy
Per Epic's recommended layout, a module lives in the `Source` directory of a project or plugin, in a
folder named after the module:
```
Source/MyModule/
  MyModule.Build.cs
  Public/                 all public headers
  Private/
    MyModuleModule.cpp    IMPLEMENT_MODULE(...)
                          all .cpp files and private headers
```
Subfolders may be nested at any depth under `Source`. For each new folder under `Public`, make a matching
folder under `Private`; the New Class Wizard does this for you.

`MyModuleModule.cpp` implements the module (`FDefaultModuleImpl` is an empty `IModuleInterface`):
```cpp
#include "Modules/ModuleManager.h"
IMPLEMENT_MODULE(FDefaultModuleImpl, MyModule);
```
Write your own `IModuleInterface` class when you need code on module load and unload.

## Build.cs
UBT builds from the `Target.cs` and `Build.cs` files, not from the IDE solution (it ignores the solution).
A `Build.cs` declares a class derived from `ModuleRules`:
```csharp
using UnrealBuildTool;
public class MyModule : ModuleRules
{
    public MyModule(ReadOnlyTargetRules Target) : base(Target)
    {
        PublicDependencyModuleNames.AddRange(new[] { "GameplayTasks" });
        PrivateDependencyModuleNames.AddRange(new[] { /* modules only your .cpp files use */ });
    }
}
```
- **Public** (`PublicDependencyModuleNames`): modules required by your public source files, such as a class
  from that module used in a public `.h`. Other modules that depend on yours can then include your headers.
- **Private** (`PrivateDependencyModuleNames`): modules only your private code needs. Epic prefers private
  wherever possible because it can reduce compile times; forward declarations in headers let many
  dependencies stay private.
- `PublicIncludePathModuleNames` / `PrivateIncludePathModuleNames`: modules whose headers you need but that
  you do not import or link against.
- `CircularlyReferencedDependentModules`: legacy only, "should not be used in new code"; the module must
  already be in the public or private list. Circular dependencies make builds slower
  (`bValidateCircularDependencies`).
- `bEnforceIWYU` enforces "include what you use" when `PCHUsage` is set to explicit or shared PCH: it warns
  on monolithic headers (`Engine.h`, `UnrealEd.h`) and checks that source files include their matching header first.

To use another module (the page's example is `GameplayTasks`), add its name to the Build.cs of the module
that needs it. UBT compiles only modules in the dependency chain of your project.

The `Public`/`Private` folders are unrelated to C++ access specifiers; they control what other modules see.
A module that nothing depends on (typically the primary game module) needs neither folder; code outside
them behaves as Private.

## .uproject / .uplugin entries
A `Modules` list defines the modules and how they load; entries are added when you regenerate project files,
if the module is in the dependency chain:
```json
"Modules": [ { "Name": "ModuleTest", "Type": "Runtime", "LoadingPhase": "Default" } ]
```
- Common types: `Runtime` (in-game classes) and `Editor` (editor-only classes); see the API docs for
  `EHostType::Type` and `ELoadingPhase::Type`.
- Plugins whose classes the editor cannot find may need `PreDefault`.
- Other parameters: `IncludelistPlatforms` / `ExcludelistPlatforms`, `IncludelistTargets` /
  `ExcludelistTargets` (Game, Server, Client, Editor, Program), `IncludelistTargetConfigurations` /
  `ExcludelistTargetConfigurations` (Debug, DebugGame, Development, Shipping, Test), `IncludelistPrograms` /
  `ExcludelistPrograms`.
- Load order inside a phase is not deterministic; use `LoadModule` / `LoadModuleChecked` in C++ when one
  module must load before another.

## Regenerate project files
Regenerate the IDE solution whenever you edit a `Build.cs` or move source files between folders: run
`GenerateProjectFiles.bat`, right-click the `.uproject` and choose Generate Project Files, or in the
editor choose File > Refresh Visual Studio Project.

## Verify
- [ ] Every module used from a public header is a public dependency; everything else is private.
- [ ] The module appears in the `Modules` list with the intended `Type` and `LoadingPhase`.
- [ ] Project files were regenerated after the Build.cs change and the target builds.

## Checked
Checked 2026-11-08 against Unreal Engine Modules and Module Properties.
Confirmed: layout, `IMPLEMENT_MODULE`, public vs private rules, the listed `ModuleRules` properties,
`Modules` list fields, regeneration methods.
Removed because the pages do not state them: `IMPLEMENT_PRIMARY_GAME_MODULE`, the `*_API` export macro and
linker-error table, the editor-module packaging claim, specific engine module names in the sample, and the
`IWYUSupport` default.
Method: docs-only read of cited pages, 2026-11-08
