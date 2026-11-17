---
id: computing-software.game-programming.unreal-engine.blueprint-function-libraries-in-cpp
name: blueprint-function-libraries-in-cpp
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, ue5, cpp, blueprints, blueprint-function-library, static-functions, worldcontext, game-programming]
level: practitioner
status: docs-checked
description: "Write UBlueprintFunctionLibrary classes in C++: static UFUNCTIONs, BlueprintCallable vs BlueprintPure, and wrapping non-UObject code, per Epic's Function Libraries page."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/blueprint-function-libraries-in-unreal-engine"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Blueprint function libraries in C++

**Goal:** stateless utility nodes written once in C++ and available to Blueprints.

## What the page says
- Blueprint Function Libraries are collections of static functions providing utility functionality not tied to a
  particular gameplay object; typically stateless and reused across gameplay code. Examples named: AI Blueprint
  Library, System Blueprint Library.
- All derive from `UBlueprintFunctionLibrary` and should contain only static methods. They are indirectly UObject derived,
  so use `UCLASS()` and, in the page's snippet, `GENERATED_UCLASS_BODY()`. Functions to expose carry `UFUNCTION()` and can
  be `BlueprintCallable` or `BlueprintPure` "depending on whether the calls have side effects or not".
- Page snippet (Analytics library):
```cpp
UCLASS()
class UAnalyticsBlueprintLibrary : public UBlueprintFunctionLibrary
{
    GENERATED_UCLASS_BODY()
    /** Starts an analytics session without any custom attributes specified */
    UFUNCTION(BlueprintCallable, Category="Analytics")
    static bool StartSession();
```
- A library function can wrap a non-UObject singleton, which the page calls a good way to expose third-party library
  functions or C++ classes without UObject support.
- Rolling several Blueprint nodes into one library function (page example: `UAIBlueprintHelperLibrary::GetAIController`,
  which casts the actor to `APawn` then the controller to `AAIController`) gives better performance than a Blueprint
  function if called often.
- Full source named on the page: `Engine/Plugins/Runtime/Analytics/AnalyticsBlueprintLibrary`.

## Checked
Date: 2026-11-07. Read in full: the Blueprint Function Libraries page including its three code blocks. The second
source (`UBlueprintFunctionLibrary` API page) returns empty text and was dropped.
Removed as not on the page: the `WorldContext` meta explanation and `GetWorldFromContextObject` example,
`ExpandEnumAsExecs`, `Keywords`, `CompactNodeTitle`, `CallableWithoutWorldContext`, the claim that Blueprint-only
libraries cannot be called from C++, the library vs subsystem advice, the module-dependency and pure-node
re-evaluation gotchas, and the Verify checklist.
Method: documentation only; no commands were run.
