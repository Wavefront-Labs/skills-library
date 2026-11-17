---
id: computing-software.game-programming.unreal-engine.ue-log-categories-and-on-screen-debug
name: ue-log-categories-and-on-screen-debug
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, uclass, ue-log, log-categories, add-on-screen-debug-message, game-programming]
level: practitioner
status: draft
description: "Log properly in Unreal: custom UE_LOG categories and verbosity, UE_LOGFMT, runtime log commands, on-screen debug messages, and stripping logs in shipping."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/logging-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Runtime/Engine/Engine/UEngine/AddOnScreenDebugMessage"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# UE_LOG categories and on-screen debug

**Goal:** filterable, cheap logging that can be turned up at runtime and disappears in shipping.

## Declare a category
```cpp
// MyGame.h
DECLARE_LOG_CATEGORY_EXTERN(LogMyAI, Log, All);   // default verbosity, compile-time max
// MyGame.cpp
DEFINE_LOG_CATEGORY(LogMyAI);
// file-local alternative:
DEFINE_LOG_CATEGORY_STATIC(LogDoor, Log, All);
```
## Use
```cpp
UE_LOG(LogMyAI, Verbose, TEXT("%s picked target %s at %.1f"), *GetName(), *GetNameSafe(Target), Dist);
#include "Logging/StructuredLog.h"
UE_LOGFMT(LogMyAI, Warning, "Path failed for {Agent} reason {Reason}", GetName(), Reason);
```
Verbosity: Fatal (crashes), Error, Warning, Display, Log, Verbose, VeryVerbose. Messages above the
category's runtime verbosity are filtered; above the compile-time max are compiled out.

## Runtime control
- Console: `log LogMyAI Verbose`, `log LogMyAI off`, `log list`.
- Command line: `-LogCmds="LogMyAI Verbose, LogNet Warning"`.
- `DefaultEngine.ini`: `[Core.Log] LogMyAI=Verbose`.
- Output: Output Log window, `Saved/Logs/<Project>.log`, `-log` for a console window.

## On-screen messages
```cpp
if (GEngine) GEngine->AddOnScreenDebugMessage(/*Key*/ 1, 2.f, FColor::Yellow,
    FString::Printf(TEXT("Speed %.0f"), Speed));     // same key overwrites the line
```
Plus `DrawDebugString`, `DrawDebugSphere` in world space (`DrawDebugHelpers.h`), all compiled out in
shipping when wrapped in `#if ENABLE_DRAW_DEBUG`.

## Shipping
`UE_LOG` is compiled out in Shipping unless `bUseLoggingInShipping = true` in Target.cs. Don't
compute expensive arguments outside the macro (they would still run).

## Gotchas
- `%s` needs `*FString` (TCHAR*), not FString — crash or garbage otherwise.
- `UE_LOG(..., Fatal, ...)` crashes the process by design.
- Per-frame Log-level spam tanks performance; use Verbose and turn it on when needed.

## Verify
- [ ] `log LogMyAI Verbose` reveals extra lines without recompiling.
- [ ] Shipping build log contains none of the game's debug categories.
