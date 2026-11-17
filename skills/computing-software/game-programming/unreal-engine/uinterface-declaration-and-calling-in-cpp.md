---
id: computing-software.game-programming.unreal-engine.uinterface-declaration-and-calling-in-cpp
name: uinterface-declaration-and-calling-in-cpp
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, ue5, uinterface-cpp, uinterface, blueprintnativeevent, execute-functions, implements, game-programming]
level: practitioner
status: draft
description: "Declare Unreal UINTERFACEs in C++ and call them correctly: UInterface/IInterface pairs, BlueprintNativeEvent Execute_ calls, Implements checks and TScriptInterface."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/interfaces-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Runtime/CoreUObject/UObject/TScriptInterface"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# UINTERFACE declaration and calling in C++

## Declare
```cpp
// Interactable.h
#pragma once
#include "UObject/Interface.h"
#include "Interactable.generated.h"

UINTERFACE(MinimalAPI, Blueprintable)
class UInteractable : public UInterface { GENERATED_BODY() };

class MYGAME_API IInteractable {
    GENERATED_BODY()
public:
    UFUNCTION(BlueprintNativeEvent, BlueprintCallable, Category = "Interaction")
    void Interact(AActor* Instigator);                   // C++ implementers override Interact_Implementation
    virtual bool CanInteract() const { return true; }    // C++-only: not callable from Blueprint
};
```
Two classes: the `U` one is the reflection shell (never implement it), the `I` one holds functions.

## Implement in C++
```cpp
class AChest : public AActor, public IInteractable {
    GENERATED_BODY()
    virtual void Interact_Implementation(AActor* Instigator) override;
};
```

## Call it (the part people get wrong)
```cpp
if (Target && Target->Implements<UInteractable>()) {     // true for C++ AND Blueprint implementers
    IInteractable::Execute_Interact(Target, this);       // required for BlueprintNativeEvent/ImplementableEvent
}
// C++-only virtuals need a cast, which fails for Blueprint-only implementers:
if (IInteractable* I = Cast<IInteractable>(Target)) { I->CanInteract(); }
```
- Calling `I->Interact()` directly on a BlueprintNativeEvent asserts/crashes; always `Execute_`.
- `Cast<IInteractable>` returns null when the interface was added in a Blueprint's Class Settings.
  Use `Implements<>` + `Execute_` for anything Blueprints may implement.

## Storing references
```cpp
UPROPERTY(EditAnywhere) TScriptInterface<IInteractable> Current;   // holds UObject + interface ptr
IInteractable::Execute_Interact(Current.GetObject(), this);
```
`TScriptInterface` keeps the object reachable for GC; the interface pointer is null for Blueprint
implementers, so call through `GetObject()`.

## Specifiers
- `Blueprintable` lets Blueprints implement it; `meta = (CannotImplementInterfaceInBlueprint)` makes
  it C++-only (then plain virtuals are callable from Blueprint with BlueprintCallable).
- `BlueprintImplementableEvent` has no C++ implementation.

## Verify
- [ ] Both a C++ actor and a Blueprint actor implementing the interface respond to the same caller.
- [ ] No ensure/crash when the target is Blueprint-only.
