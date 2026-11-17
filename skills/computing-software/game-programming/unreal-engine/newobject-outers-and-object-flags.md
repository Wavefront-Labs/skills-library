---
id: computing-software.game-programming.unreal-engine.newobject-outers-and-object-flags
name: newobject-outers-and-object-flags
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, uobject, newobject, object-outer, object-flags, game-programming]
level: practitioner
status: draft
description: "Create UObjects correctly in Unreal with NewObject: choosing the Outer, names, flags like RF_Transient, templates, and why CreateDefaultSubobject is constructor-only."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/creating-objects-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/API/CoreUObject/UObject/NewObject"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# NewObject outers and object flags

**Goal:** runtime UObjects with correct ownership, GC behaviour, serialization and networking.

## Which creation function
| Context | Use |
|---|---|
| Inside a constructor, default subobject | `CreateDefaultSubobject<T>(TEXT("Name"))` |
| Runtime UObject (non-actor) | `NewObject<T>(Outer, Class, Name, Flags, Template)` |
| Actor | `World->SpawnActor` (never NewObject for actors) |
| Runtime component | `NewObject<UMyComp>(Actor)` + `RegisterComponent()` (+ `AddInstanceComponent`) |
| Duplicate | `DuplicateObject(Source, Outer)` |

## The Outer
- Defines the object's path and package (`Outer->GetPathName()`), and who "contains" it.
- It does **not** keep the object alive by itself — a UPROPERTY reference (or root set) does. But
  when the outer is destroyed/GC'd, inner objects with no other references go too.
- Use the owning actor/component/subsystem as outer; `GetTransientPackage()` for temporary objects
  with no owner.
- Wrong outer issues: objects saved into a level by accident (outer = level actor in editor), net
  replicated subobjects must have the owning actor in their outer chain.

## Flags
- `RF_Transient`: never saved to disk (use for runtime caches made in the editor).
- `RF_Public`, `RF_Standalone` (keeps asset alive without references; editor/asset creation only).
- `RF_ArchetypeObject` / templates: passing `Template` copies property values from another object.

```cpp
UPROPERTY() TObjectPtr<UInventory> Inventory;
Inventory = NewObject<UInventory>(this, InventoryClass, NAME_None, RF_Transient);
```

## Names
Explicit names must be unique within the outer; `NAME_None` generates one. Use
`MakeUniqueObjectName(Outer, Class, BaseName)` when you need readable unique names.

## Gotchas
- `CreateDefaultSubobject` outside a constructor asserts.
- Holding a NewObject result only in a raw pointer or local -> GC frees it at the next collection
  (random crashes later). Always store in a UPROPERTY or TStrongObjectPtr (non-UObject owners).
- NewObject on an abstract class asserts; check `Class->HasAnyClassFlags(CLASS_Abstract)`.

## Verify
- [ ] `obj gc` followed by use of the object: still valid (properly referenced).
- [ ] `obj list class=UInventory` count stable over time (no leaks via standalone flags).
