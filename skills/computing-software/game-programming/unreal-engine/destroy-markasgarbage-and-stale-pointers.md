---
id: computing-software.game-programming.unreal-engine.destroy-markasgarbage-and-stale-pointers
name: destroy-markasgarbage-and-stale-pointers
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, uobject, garbage-collection, uproperty, weak-pointer, stale-pointers, game-programming]
level: practitioner
status: docs-checked
description: "Handle destroyed UObjects in Unreal: automatic nulling of UPROPERTY references, raw pointer hazards, TWeakObjectPtr, root set and UPROPERTY references that keep objects alive."
sources:
  - https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-object-handling-in-unreal-engine
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Destroyed objects and stale pointers

**Goal:** never use a pointer to an Actor or component that has been destroyed.

## What the engine does for you
When an `AActor` or `UActorComponent` is destroyed or otherwise removed from play, every reference to it
that the reflection system can see is automatically nulled. That covers `UPROPERTY` pointers and pointers
inside Unreal container classes such as `TArray`. Epic's stated benefit: null-checking becomes more
reliable, because it catches both ordinary null pointers and pointers that would have pointed at deleted
memory. The flip side is that Actor and component pointers can become null because other code destroyed them.

The same nulling happens to a `UPROPERTY` that references an asset when someone uses Force Delete on that
asset in the editor, so code that handles asset UObjects must tolerate those pointers becoming null.

## What the engine does not do
An object reference held in a raw pointer is unknown to the engine: it is not nulled and does not prevent
garbage collection. A `UObject*` need not always be a `UPROPERTY`; where you want a non-`UPROPERTY` pointer,
Epic suggests `TWeakObjectPtr`: it does not prevent garbage collection, can be queried for validity before
access, and is set to null when the object is destroyed.

```cpp
TWeakObjectPtr<AActor> Weak = Target;
if (AActor* T = Weak.Get()) { /* still alive */ }
```

## Keeping objects alive
Garbage collection builds a reference graph from a root set; anything not reachable is removed. In practice
you need a `UPROPERTY` reference (a plain pointer, or an Unreal container of object pointers such as
`TArray<UObject*>`) to keep an object alive. Actors and components are usually an exception: an Actor is
referenced by its Level and a component by its Actor. Remove an Actor with `Destroy()`; destroy a component
with `DestroyComponent()`, though components are usually destroyed with their owning Actor.

## Rules
- Hold Actor and component references in `UPROPERTY` members or Unreal containers, or in `TWeakObjectPtr`.
- Null-check before use; a null check catches destroyed objects only for references the engine tracks.
- Never keep a raw `UObject*` across frames without a `UPROPERTY` or weak pointer.

## Not verified here
`IsValid`, `MarkAsGarbage`, `TObjectPtr` behaviour, garbage-collection console commands and pending-kill
settings in UE5 are not described on the cited page, whose API-reference sibling is unreadable; consult the
current engine API reference and source for those.

## Verify
- [ ] No raw `UObject*` members outside `UPROPERTY` unless weakly held and documented.
- [ ] Code handling assets tolerates null after Force Delete.

## Checked
Checked 2026-11-08 against the Unreal Object Handling page.
Confirmed: automatic reference nulling and its limits, Force Delete note, `TWeakObjectPtr` behaviour, root set
and `UPROPERTY` keep-alive rule, `Destroy` and `DestroyComponent`.
Removed because the page does not state them: `IsValid` and `MarkAsGarbage` semantics, `gc.PendingKillEnabled`,
debugging commands (`obj gc`, `obj refs`, `-stompmalloc`), delegate binding behaviour, iteration advice, and the
unreadable API-reference source.
Method: docs-only read of cited pages, 2026-11-08
