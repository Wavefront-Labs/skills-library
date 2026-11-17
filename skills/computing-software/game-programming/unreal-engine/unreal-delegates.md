---
id: computing-software.game-programming.unreal-engine.unreal-delegates
name: unreal-delegates
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, ue5, cpp, unreal-delegates, dynamic-multicast-delegate, events, blueprintassignable, game-programming]
level: practitioner
status: draft
description: "Declare and bind Unreal delegates: single vs multicast vs dynamic, BlueprintAssignable events, binding with AddUObject/AddDynamic, handles, and lifetime safety."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/delegates-and-lambda-functions-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/dynamic-delegates-in-unreal-engine"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Unreal delegates

**Goal:** decoupled events in C++ and Blueprint that don't crash on destroyed listeners.

## Kinds
| Macro | Bindings | Blueprint | Cost |
|---|---|---|---|
| `DECLARE_DELEGATE_OneParam` | one | no | cheapest; return values allowed (`_RetVal`) |
| `DECLARE_MULTICAST_DELEGATE_OneParam` | many | no | fast |
| `DECLARE_DYNAMIC_DELEGATE_OneParam` | one, by UFUNCTION name | yes (as param) | serialisable, slower |
| `DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam` | many | yes, `BlueprintAssignable` | slowest |
| `DECLARE_EVENT` | multicast, only owner can Broadcast | no | |
| `TDelegate<void(int32)>` / `TMulticastDelegate<...>` | template form (5.x) | no | |

Dynamic delegates name each param: `DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnHealthChanged, float, NewHealth, AActor*, Instigator);`

## Declare and broadcast
```cpp
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnDied, AActor*, Killer);
DECLARE_MULTICAST_DELEGATE_TwoParams(FOnAmmoChanged, int32 /*Clip*/, int32 /*Reserve*/);

UCLASS() class UHealthComponent : public UActorComponent {
    GENERATED_BODY()
public:
    UPROPERTY(BlueprintAssignable, Category = "Health") FOnDied OnDied;   // Blueprint "Bind Event"
    FOnAmmoChanged OnAmmoChanged;                                          // C++ only
    void Kill(AActor* Killer) { OnDied.Broadcast(Killer); }
};
```

## Bind
```cpp
// dynamic: handler must be a UFUNCTION
Health->OnDied.AddDynamic(this, &AMyHUD::HandleDied);          // AddUniqueDynamic avoids double binds
Health->OnDied.RemoveDynamic(this, &AMyHUD::HandleDied);

// native multicast: keep the handle to remove
FDelegateHandle H = Weapon->OnAmmoChanged.AddUObject(this, &UAmmoWidget::Refresh);   // weak: skipped if this is GC'd
Weapon->OnAmmoChanged.Remove(H);
Weapon->OnAmmoChanged.AddWeakLambda(this, [this](int32 C, int32 R) { ... });           // lambda tied to UObject lifetime
Weapon->OnAmmoChanged.AddSP(SharedThis, &FFoo::Bar);                                     // shared-pointer object
```
- Single delegates: `BindUObject`, `ExecuteIfBound(...)` (Execute on unbound asserts).
- `AddLambda` with raw `this` capture can crash after destruction; use `AddWeakLambda` / `AddUObject`.
- `AddRaw` for non-UObject, non-shared objects: you must remove it before the object dies.

## Gotchas
- `AddDynamic` on a non-UFUNCTION compiles but fails to bind at runtime ("Unable to bind delegate" ensure).
- Binding in the constructor duplicates on Blueprint recompile; bind in `BeginPlay` / `PostInitializeComponents`.
- Broadcasting while a listener removes itself is safe for multicast; listeners added during broadcast
  may or may not be called this time.
- Dynamic multicast delegates are not replicated; replicate state and broadcast in OnRep.

## Verify
- [ ] Destroying a listener actor then broadcasting does not crash.
- [ ] No double-firing after Blueprint recompiles or level reloads.
