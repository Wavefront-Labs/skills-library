---
id: computing-software.game-programming.unreal-engine.third-party-libraries-in-modules
name: third-party-libraries-in-modules
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, ue-third-party-library, external-module, build-cs, runtimedependencies, cpp, game-programming]
level: practitioner
status: draft
description: "Integrate prebuilt third-party C/C++ libraries into an Unreal module: External module type, include and lib paths, delay-loaded DLLs, RuntimeDependencies and platform binaries."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/integrating-third-party-libraries-into-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/module-properties-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/build-tool-third-party-libraries"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Third-party libraries in a module

**Goal:** link a prebuilt library (static or DLL) and ship it in packaged builds.

## Layout
```
Plugins/MyLib/Source/ThirdParty/MyLibLibrary/
  MyLibLibrary.Build.cs
  include/mylib.h
  lib/Win64/mylib.lib        bin/Win64/mylib.dll
  lib/Linux/libmylib.a
Plugins/MyLib/Source/MyLib/   (normal module wrapping it)
```

## External module Build.cs
```csharp
public class MyLibLibrary : ModuleRules {
    public MyLibLibrary(ReadOnlyTargetRules Target) : base(Target) {
        Type = ModuleType.External;
        PublicSystemIncludePaths.Add(Path.Combine(ModuleDirectory, "include"));
        if (Target.Platform == UnrealTargetPlatform.Win64) {
            PublicAdditionalLibraries.Add(Path.Combine(ModuleDirectory, "lib", "Win64", "mylib.lib"));
            PublicDelayLoadDLLs.Add("mylib.dll");
            RuntimeDependencies.Add("$(BinaryOutputDir)/mylib.dll",
                Path.Combine(ModuleDirectory, "bin", "Win64", "mylib.dll"));
        } else if (Target.Platform == UnrealTargetPlatform.Linux) {
            PublicAdditionalLibraries.Add(Path.Combine(ModuleDirectory, "lib", "Linux", "libmylib.a"));
        }
    }
}
```
The wrapper module lists `"MyLibLibrary"` in its dependencies. `RuntimeDependencies` with
`$(BinaryOutputDir)` copies the DLL next to the executable when staging, so packaged builds find it.

## Including headers
Third-party headers trigger UE warnings (shadowing, unused params). Wrap:
```cpp
THIRD_PARTY_INCLUDES_START
#include "mylib.h"
THIRD_PARTY_INCLUDES_END
```
Windows headers: `#include "Windows/AllowWindowsPlatformTypes.h"` / `HideWindowsPlatformTypes.h`.

## ABI rules
- Build the library with the same MSVC runtime (`/MD`, release CRT) UE uses; debug CRT libs fail.
- C++ STL types must not cross the boundary into UE containers expecting their allocator; prefer C APIs.
- Exceptions and RTTI are off in UE modules by default (`bEnableExceptions = true` per module if needed).

## Gotchas
- Delay-loaded DLLs must be loaded manually (`FPlatformProcess::GetDllHandle`) from the plugin's
  binaries path in `StartupModule`, or rely on staging to place them beside the exe.
- Prefer static libs for consoles/mobile; DLL rules differ per platform.

## Verify
- [ ] Packaged build on a clean machine runs and loads the library (no missing DLL dialog).
