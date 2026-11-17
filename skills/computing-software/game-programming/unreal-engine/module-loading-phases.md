---
id: computing-software.game-programming.unreal-engine.module-loading-phases
name: module-loading-phases
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, module-loading-phase, modules, uplugin, startupmodule, game-programming]
level: practitioner
status: draft
description: "Pick Unreal module LoadingPhase values (PostConfigInit, PreDefault, Default, PostEngineInit) and module Type in uproject/uplugin, and write safe StartupModule code."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-modules", "https://docs.unrealengine.com/5.3/en-US/API/Runtime/Projects/ELoadingPhase__Type/", "https://dev.epicgames.com/documentation/en-us/unreal-engine/plugins-in-unreal-engine"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Module loading phases

**Goal:** each module loads early enough for what depends on it, and no earlier.

## Where it is set
```json
"Modules": [
  { "Name": "MyGame",        "Type": "Runtime", "LoadingPhase": "Default" },
  { "Name": "MyGameEditor",  "Type": "Editor",  "LoadingPhase": "PostEngineInit" },
  { "Name": "MyShaders",     "Type": "Runtime", "LoadingPhase": "PostConfigInit" }
]
```
in `.uproject` or `.uplugin`.

## Phases (in order)
| Phase | Use for |
|---|---|
| EarliestPossible / PostConfigInit | low-level systems; shader source directory mappings (must exist before shaders compile) |
| PostSplashScreen / PreEarlyLoadingScreen | loading screen modules |
| PreLoadingScreen | movie player/loading screen |
| PreDefault | modules other Default modules depend on at load (e.g. custom asset types used in CDOs) |
| Default | gameplay modules (default) |
| PostDefault | after Default |
| PostEngineInit | needs GEngine, editor subsystems, asset registry; editor tools, menu extensions |

## Types
`Runtime` (everywhere except programs), `RuntimeNoCommandlet`, `Editor` (editor only, stripped from
games), `EditorNoCommandlet`, `UncookedOnly` (editor and uncooked, e.g. Blueprint node modules),
`DeveloperTool`, `ClientOnly`, `ServerOnly`.

## Module class
```cpp
class FMyGameEditorModule : public IModuleInterface {
    void StartupModule() override {
        FCoreDelegates::OnPostEngineInit.AddRaw(this, &FMyGameEditorModule::Register);   // if phase is earlier
        AddShaderSourceDirectoryMapping(TEXT("/Plugin/MyShaders"), FPaths::Combine(Dir, TEXT("Shaders")));  // PostConfigInit modules
    }
    void ShutdownModule() override { /* unregister menus, tickers, delegates */ }
};
IMPLEMENT_MODULE(FMyGameEditorModule, MyGameEditor)
```
The primary game module uses `IMPLEMENT_PRIMARY_GAME_MODULE`.

## Gotchas
- UObject classes in a module are registered when it loads; a Default-phase module class referenced by
  a PreDefault module's CDO fails to resolve.
- Accessing `GEngine` or `UAssetManager` in StartupModule of a Default module can be null; defer to
  `OnPostEngineInit`.
- ShutdownModule runs during exit when other systems may be gone; null-check and avoid UObject work.

## Verify
- [ ] Editor, packaged game and commandlets (cook) all start without module load errors in the log.
