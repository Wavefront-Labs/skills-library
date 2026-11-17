---
id: computing-software.game-programming.unreal-engine.module-api-exports-and-unresolved-externals
name: module-api-exports-and-unresolved-externals
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, module-api-export, modules, dllexport, linker-errors, cpp, game-programming]
level: practitioner
status: draft
description: "Fix Unreal LNK2019 unresolved externals across modules: MYMODULE_API exports, MinimalAPI, inline vs exported functions and the Build.cs dependency that must accompany them."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-modules", "https://dev.epicgames.com/documentation/en-us/unreal-engine/class-specifiers", "https://dev.epicgames.com/documentation/en-us/unreal-engine/module-properties-in-unreal-engine"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# MODULE_API exports and unresolved externals

**Goal:** code in module B can call classes and functions defined in module A.

## How exports work
UnrealBuildTool defines `MYGAME_API` per module: `__declspec(dllexport)` when compiling MyGame,
`dllimport` for others (in modular/editor builds; in monolithic builds it is empty, which is why
missing exports often only break the editor build).

```cpp
UCLASS()
class MYGAME_API AWeapon : public AActor { ... };          // whole class exported

class FInventoryUtils { public: static MYGAME_API int32 CountItems(const UInventory& Inv); };  // one function

UCLASS(MinimalAPI)                                           // exports only type info (Cast/StaticClass)
class UMyLightweightThing : public UObject { ... };
```

## Diagnosing LNK2019 / LNK2001
1. Read the mangled symbol: which class/function and which module defines it.
2. Is that module in the caller's `Build.cs` `PublicDependencyModuleNames` or
   `PrivateDependencyModuleNames`? Missing dependency gives unresolved externals or include errors.
3. Is the symbol exported? Engine classes declared without `ENGINE_API` (or MinimalAPI) cannot be
   called from your module except inline functions. Workarounds: use a public exported base/API,
   reflection (UFUNCTION via `ProcessEvent`), or a local engine change.
4. Templates and inline functions defined in headers need no export; non-inline functions defined in a
   .cpp do.
5. Static members and global variables need the API macro too (`extern MYGAME_API int32 GFoo;`).

## Gotchas
- Exporting a class with many members bloats DLL export tables; Epic marks big engine classes
  MinimalAPI and exports chosen functions.
- Virtual functions called through a base pointer do not need export; direct calls do.
- Plugins: macro is the module name uppercased (`MYPLUGINRUNTIME_API`), not the plugin name.
- Hot reload/Live Coding cannot add new exports reliably; restart the editor after changing them.

## Verify
- [ ] Both Development Editor (modular) and a packaged Shipping (monolithic) build link.
