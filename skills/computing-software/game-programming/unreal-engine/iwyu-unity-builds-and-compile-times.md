---
id: computing-software.game-programming.unreal-engine.iwyu-unity-builds-and-compile-times
name: iwyu-unity-builds-and-compile-times
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, iwyu, unity-build, compile-times, includes, cpp, game-programming]
level: practitioner
status: draft
description: "Cut Unreal C++ compile times with Include What You Use, PCH settings, unity build tuning, adaptive non-unity files and forward declarations, and catch missing includes."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/include-what-you-use-iwyu-for-unreal-engine-programming", "https://dev.epicgames.com/documentation/en-us/unreal-engine/module-properties-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/build-configuration-for-unreal-engine"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# IWYU, unity builds and compile times

**Goal:** fast incremental builds and headers that compile on their own.

## IWYU rules
- Each `.cpp` includes its own header **first**, then what it uses. Each header includes what it
  needs (base class headers, types used by value) and forward-declares the rest.
- Do not include `Engine.h` or `EngineMinimal.h`; include `CoreMinimal.h` plus specific headers
  (`GameFramework/Character.h`, `Components/StaticMeshComponent.h`).
- Build.cs: `PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;` (default for new modules),
  `IWYUSupport = IWYUSupport.Full` (UE5.2+, replaces `bEnforceIWYU`).

## Forward declarations
```cpp
class UHealthComponent;                 // header
UPROPERTY() TObjectPtr<UHealthComponent> Health;   // fine with forward decl
```
Pointers, references and TObjectPtr members need only a forward declaration; `TSubclassOf<>`,
by-value members and inline calls need the full include.

## Unity builds
UBT concatenates .cpp files into `Module.N.cpp` blobs. Fast full builds, but:
- Hides missing includes (another file in the blob included it). CI should run a non-unity build:
  `-DisableUnity` or `bUseUnityBuild = false` in a BuildConfiguration.xml / Target for the check job.
- Files you edit are moved out of the unity blob automatically (**adaptive unity**, based on
  source control writable/modified state), so iteration stays fast.
- Static/anonymous namespace name clashes appear only in unity builds; prefix helpers.
Tune `MinFilesUsingPrecompiledHeader`, `NumIncludedBytesPerUnityCPP` in BuildConfiguration.xml.

## Measuring
`-Timing` flag on UBT or `bAllowUBALocalExecutor`/Unreal Build Accelerator logs; MSVC `/d1reportTime`
via `bPrintToolChainTimingInfo`. Unreal Insights with `-trace` for UBA. Find heavy headers included
everywhere and replace with forward declarations.

## Gotchas
- `*.generated.h` must be the last include in a UCLASS header.
- Changing a widely included header rebuilds everything; keep hot headers lean (Pimpl or move
  implementation to .cpp).

## Verify
- [ ] Non-unity CI build passes (proves IWYU correctness).
- [ ] Incremental build after editing one .cpp takes seconds.
