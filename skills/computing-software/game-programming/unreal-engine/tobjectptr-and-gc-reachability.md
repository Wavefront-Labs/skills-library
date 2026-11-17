---
id: computing-software.game-programming.unreal-engine.tobjectptr-and-gc-reachability
name: tobjectptr-and-gc-reachability
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, ue5, uobject, tobjectptr, unreal-garbage-collection, uproperty, addreferencedobjects, gc-reachability, dangling-pointer, incremental-gc, game-programming]
level: practitioner
status: draft
description: "Keep UObjects alive and pointers valid in UE5: TObjectPtr UPROPERTY members, what the GC can and cannot see, AddReferencedObjects, and debugging collected-object crashes."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-5-migration-guide", "https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-object-handling-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/garbage-collection-in-unreal-engine"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# TObjectPtr and GC reachability

**Goal:** no UObject used by your code is ever collected while you still point at it, and no stale
pointer survives after it is collected.

## How the UE garbage collector decides
Mark-and-sweep from roots (the root set, `AddToRoot`, objects referenced by the engine, the world).
It follows **only references it can see**:
- `UPROPERTY()` members (raw `UObject*`, `TObjectPtr<>`, `TArray/TMap/TSet` of them, structs with
  UPROPERTY members).
- References reported in `AddReferencedObjects` (for `UObject` subclasses or `FGCObject` holders).
A raw pointer member **without** `UPROPERTY()` is invisible: the object may be collected and your
pointer dangles (no nulling). That is the most common UE crash.

## Member declarations in UE5
```cpp
UCLASS()
class AMyTurret : public AActor
{
    GENERATED_BODY()
    UPROPERTY(EditAnywhere) TObjectPtr<UStaticMeshComponent> Barrel;   // strong, GC-visible
    UPROPERTY() TArray<TObjectPtr<AActor>> Targets;                     // container also visible
    UPROPERTY(Transient) TObjectPtr<UMaterialInstanceDynamic> FlashMID; // not saved, still referenced
    TWeakObjectPtr<AActor> LastAttacker;                                // non-owning, auto-invalidates
};
```
- `TObjectPtr<T>` replaces raw `T*` for UPROPERTY members in UE5: same size in shipping builds, adds
  access tracking and lazy-load support in the Editor. Function parameters and locals stay raw `T*`.
- When an Actor/Component is destroyed, UPROPERTY references to it are nulled during GC (pending-kill
  objects are cleared), so always check `IsValid(Ptr)` (checks null and garbage flag), not just `Ptr != nullptr`.

## Non-UObject holders
A plain C++ class (Slate widget, subsystem helper, `TSharedPtr` owned manager) holding UObjects:
```cpp
class FMyCache : public FGCObject
{
public:
    TArray<TObjectPtr<UTexture2D>> Textures;
    virtual void AddReferencedObjects(FReferenceCollector& C) override { C.AddReferencedObjects(Textures); }
    virtual FString GetReferencerName() const override { return TEXT("FMyCache"); }
};
```
Or `TStrongObjectPtr<T>` for a single owned reference outside the UObject graph (main thread only).

## Creation and outers
`NewObject<UMyThing>(Outer)` - the outer is not a GC reference by itself; something must reference the
new object via UPROPERTY or it is collected next GC. Spawned actors are kept alive by the level.

## Debugging collected-object crashes
- Symptoms: access violation in a member function, object name `None`, flags containing `Garbage`.
- `obj refs name=MyObjName` console command lists referencers; `obj gc` forces GC to reproduce.
- `gc.CollectGarbageEveryFrame 1` (dev builds) makes dangling-pointer bugs crash immediately.
- `-stompmalloc` / `-mallocstomp` on the command line catches use-after-free closer to the bug.

## Verify
- [ ] Every UObject member pointer is a UPROPERTY TObjectPtr, TWeakObjectPtr, or reported via AddReferencedObjects.
- [ ] Play with `gc.CollectGarbageEveryFrame 1` for a few minutes without crashes.
- [ ] Access sites use `IsValid()` where the target can be destroyed by gameplay.
