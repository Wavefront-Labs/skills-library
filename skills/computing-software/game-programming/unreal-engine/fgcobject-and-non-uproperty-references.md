---
id: computing-software.game-programming.unreal-engine.fgcobject-and-non-uproperty-references
name: fgcobject-and-non-uproperty-references
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, ue5, fgcobject-addreferencedobjects, fgcobject, addtoroot, tstrongobjectptr, garbage-collection, game-programming]
level: advanced
status: draft
description: "Keep UObjects alive from non-UObject code in Unreal: FGCObject::AddReferencedObjects, TStrongObjectPtr, AddToRoot trade-offs, and diagnosing objects collected early."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-object-handling-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Runtime/CoreUObject/UObject/FGCObject", "https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Runtime/CoreUObject/UObject/TStrongObjectPtr"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# FGCObject and AddToRoot for non-UPROPERTY references

**Problem:** the GC only sees references held in `UPROPERTY` fields (and engine-known containers).
A raw `UObject*` in a plain C++ class, a Slate widget, a module, or a lambda is invisible: the object
gets collected and the pointer dangles.

## Option 1: FGCObject (preferred for owning C++ classes)
```cpp
class FMyToolState : public FGCObject {
public:
    TObjectPtr<UTexture2D> Preview = nullptr;
    TArray<TObjectPtr<UMaterialInstanceDynamic>> MIDs;

    virtual void AddReferencedObjects(FReferenceCollector& Collector) override {
        Collector.AddReferencedObject(Preview);           // nulled automatically if marked garbage
        Collector.AddReferencedObjects(MIDs);
    }
    virtual FString GetReferencerName() const override { return TEXT("FMyToolState"); }  // required
};
```
Lives as long as the C++ object; registration is automatic in the FGCObject constructor.

## Option 2: TStrongObjectPtr (single reference, RAII)
```cpp
TStrongObjectPtr<UMyData> Data(NewObject<UMyData>());   // rooted until the pointer is destroyed or Reset()
```
Simple for a few objects; each one is an FGCObject internally. Must be created/destroyed on the game thread.

## Option 3: AddToRoot / RemoveFromRoot
```cpp
Obj->AddToRoot();     // never collected ...
Obj->RemoveFromRoot();// ... until you remember this
```
Use only for true singletons for the process lifetime. Forgetting `RemoveFromRoot` leaks, and rooted
objects referencing world objects keep whole worlds alive (map change leak: "World not cleaned up").

## Inside UObjects
Use `UPROPERTY()` fields (with `TObjectPtr`). For containers the reflection system can't see (e.g. a
`TMap<FName, UObject*>` inside a USTRUCT not marked UPROPERTY), override the static
`AddReferencedObjects(UObject* InThis, FReferenceCollector&)` on the UClass.

## Non-owning references
`TWeakObjectPtr<T>` does not keep the object alive; check `IsValid()`/`Get()` before use.

## Diagnose
- `obj refs name=<ObjectName>` shows referencers; `obj gc` / `gc.CollectGarbageEveryFrame 1` forces GC
  each frame to reproduce early collection quickly.
- Crash on access to a "MarkAsGarbage"/"PendingKill" object right after GC: missing reference.
- Map change leaks: run `obj list class=World` after travel; a lingering world means something
  rooted still references it (`obj refs` on that world names the chain).

## Verify
- [ ] With `gc.CollectGarbageEveryFrame 1`, the tool/feature runs without dangling pointer crashes.
- [ ] After closing the tool, `obj list class=UMyData` count drops (no leak).
