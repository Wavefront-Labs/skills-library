---
id: computing-software.game-programming.unreal-engine.uobject-memory-and-smart-pointers
name: uobject-memory-and-smart-pointers
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, ue5, uobject, garbage-collection, tweakobjectptr, tsharedptr, tuniqueptr, tstrongobjectptr, async-loading, streamable-manager, fgcobject, memory-management, pending-kill, isvalid, game-programming]
level: advanced
status: draft
description: "Pick the right pointer type for Unreal UObjects vs plain C++ objects, and load assets asynchronously without stalling or leaking."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-smart-pointer-library", "https://dev.epicgames.com/documentation/en-us/unreal-engine/asynchronous-asset-loading-in-unreal-engine"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# UObject lifetimes, smart pointers, and async loading in Unreal

**Goal:** know which of Unreal's several pointer types to reach for — UObjects
have their own GC and must never be mixed with the standard C++ smart pointer
family — and load assets without a hitch on the main thread.

## Two separate pointer worlds — do not cross them
Unreal has two unrelated ownership systems:
- **UObjects** (anything deriving `UObject`: Actors, Components, UAssets) are
  managed by Unreal's own garbage collector. Use `UPROPERTY()` raw pointers
  (owning, strong reference), `TWeakObjectPtr<T>` (non-owning, auto-nulls when
  the object is collected, check `.IsValid()`), or `TStrongObjectPtr<T>` (owning,
  for a UObject held by a non-UObject/non-UPROPERTY context like a plain C++
  class or a static — forces it to survive GC passes that would otherwise collect
  it since nothing reflects a raw pointer in a plain class).
- **Everything else** (plain C++ structs/classes, non-UObject game logic) uses
  the **standard smart pointer library**: `TSharedPtr<T>`, `TSharedRef<T>`,
  `TWeakPtr<T>`, `TUniquePtr<T>` — Unreal's own implementations of
  shared_ptr/unique_ptr semantics, used because Epic predates/avoids STL
  dependency in some build configs, not interchangeable with `std::shared_ptr`.
- **Never** wrap a `UObject*` in `TSharedPtr` — UObject lifetime is GC's job;
  wrapping it in a second, incompatible ownership system produces double-free or
  use-after-free bugs that are extremely hard to trace back to the mismatch.

## The classic GC crash and how to actually fix it
"Random crash a minute or two into play, accessing garbage memory" is almost
always a `UObject*` held somewhere GC can't see: a raw pointer field on a plain
C++ struct, a `TArray<UObject*>` on a non-UObject class, a static/global raw
pointer. Fix by either making the holder itself a `UPROPERTY`-bearing UObject,
using `TStrongObjectPtr` for the non-reflected holder case, or switching to
`TWeakObjectPtr` plus an `IsValid()` check if you don't actually need to keep it
alive. `FGCObject`/`AddReferencedObjects` is the escape hatch for a plain C++
class that must hold strong UObject references and can't become a UObject
itself (rare; most code should just become a UObject or use TStrongObjectPtr).

## Async asset loading
Loading a large asset synchronously (`LoadObject<T>`, a hard reference resolved
at load time) blocks the game thread and shows up as a hitch or a loading-screen
stall. For anything not needed instantly:
```cpp
TSoftObjectPtr<UStaticMesh> SoftMesh;   // reference that doesn't force-load the asset
FStreamableManager& Streamable = UAssetManager::GetStreamableManager();
Streamable.RequestAsyncLoad(SoftMesh.ToSoftObjectPath(),
    FStreamableDelegate::CreateUObject(this, &AMyActor::OnMeshLoaded));
```
`TSoftObjectPtr`/`TSoftClassPtr` store a path, not a hard reference — using them
instead of `TObjectPtr`/raw UPROPERTY pointers for optional or large content
(cosmetics, level-specific meshes) keeps them out of the always-loaded reference
graph, which matters directly for both memory and cook/package size (a hard
reference chain pulls everything it points to into the same package or forces it
resident). Cancel outstanding `RequestAsyncLoad` handles on actor destruction —
a completed-callback firing on a destroyed/`BeginDestroy`'d actor is a crash.

## Verify
- [ ] No raw `UObject*` lives on a non-UObject class or a static without
      `TStrongObjectPtr`/`FGCObject` backing it.
- [ ] `TSharedPtr`/`TWeakPtr` used only for non-UObject types; grep confirms no
      `TSharedPtr<AActor>` or similar in the codebase.
- [ ] Large/optional assets referenced as `TSoftObjectPtr`, loaded via
      `FStreamableManager`, with the callback checking the requesting actor is
      still valid before using the loaded asset.
- [ ] A play session of several minutes with `gc.CollectGarbageEveryFrame 1`
      (stress test) shows no crash — this flags dangling-reference bugs that a
      normal GC cadence hides for a while.
