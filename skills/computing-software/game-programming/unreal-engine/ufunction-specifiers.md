---
id: computing-software.game-programming.unreal-engine.ufunction-specifiers
name: ufunction-specifiers
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, ue5, cpp, ufunction-specifiers, blueprintcallable, blueprintpure, blueprintnativeevent, blueprintimplementableevent, game-programming]
level: practitioner
status: draft
description: "Choose UFUNCTION specifiers: BlueprintCallable vs Pure, BlueprintImplementableEvent vs BlueprintNativeEvent with _Implementation, Exec, CallInEditor and meta for nicer nodes."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/ufunctions-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/function-specifiers"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# UFUNCTION specifiers

**Goal:** C++ functions appear in Blueprint with the right node type and override semantics.

## Calling C++ from Blueprint
```cpp
UFUNCTION(BlueprintCallable, Category = "Combat")
void ApplyDamage(float Amount, AActor* Instigator);           // exec pins, can have side effects

UFUNCTION(BlueprintPure, Category = "Combat")
float GetHealthPercent() const;                               // no exec pins; re-evaluated per connected use

UFUNCTION(BlueprintCallable, BlueprintPure = false)           // const function that should still get exec pins
bool TryFindTarget(AActor*& OutTarget) const;                  // non-const ref params become output pins
```
- `BlueprintPure` functions run **once per consuming pin**, every time; never make expensive or random
  functions pure.
- `const` functions are pure by default when BlueprintCallable; force exec pins with `BlueprintPure = false`.
- Output params: non-const references. Pass-by-ref input: `UPARAM(ref) TArray<int32>& Items`.
- `UPARAM(DisplayName = "Target")` renames pins.

## Blueprint implementing C++ events
```cpp
UFUNCTION(BlueprintImplementableEvent, Category = "FX")
void OnHitFX(const FHitResult& Hit);                 // no C++ body; Blueprint implements (or nothing happens)

UFUNCTION(BlueprintNativeEvent, Category = "Interaction")
bool CanInteract(APawn* Who) const;                    // C++ default + Blueprint override
virtual bool CanInteract_Implementation(APawn* Who) const;   // define this in the .cpp
```
- Call a NativeEvent as `CanInteract(Who)` (dispatches to Blueprint override if any), never
  `_Implementation` directly unless you mean "skip Blueprint".
- In the Blueprint override, "Add call to parent function" runs the C++ implementation.
- Interface functions use the same specifiers; call with `IMyInterface::Execute_CanInteract(Obj, Who)`.

## Other specifiers
- `CallInEditor`: button in Details panel (editor utilities on actors).
- `Exec`: console command on PlayerController, Pawn, HUD, GameMode, CheatManager, GameInstance.
- `Server` / `Client` / `NetMulticast` + `Reliable`/`Unreliable` + `WithValidation`: RPCs.
- `BlueprintAuthorityOnly`, `BlueprintCosmetic`.
- Meta: `DefaultToSelf = "Target"`, `HidePin`, `AdvancedDisplay = "2"`, `ExpandEnumAsExecs = "Result"`
  (enum return becomes exec outputs), `DeterminesOutputType`, `WorldContext = "WorldContextObject"`,
  `Keywords`, `CompactNodeTitle`, `DeprecatedFunction`.

## Gotchas
- UFUNCTION parameters must be reflection-compatible (no raw pointers to non-UObjects, no std types).
- Overloaded functions can't both be UFUNCTIONs.
- Changing a signature breaks existing Blueprint nodes; deprecate and redirect (`+FunctionRedirects`).

## Verify
- [ ] Pure nodes are only used for cheap getters (no randomness, no allocations).
- [ ] NativeEvent overrides in Blueprint call parent where the C++ behaviour is required.
