---
id: computing-software.software-engineering.csharp-dotnet.weakreference-and-conditionalweaktable
name: weakreference-and-conditionalweaktable
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, dotnet-memory-management, weakreference, conditionalweaktable, memory-leaks, event-handler-leaks]
level: advanced
status: docs-checked
description: "Use WeakReference and ConditionalWeakTable to attach data or cache objects without keeping them alive; short vs long weak references and their caveats."
sources: ["https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/weak-references", "https://learn.microsoft.com/en-us/dotnet/api/system.runtime.compilerservices.conditionalweaktable-2"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WeakReference and ConditionalWeakTable

```csharp
var weak = new WeakReference(obj);               // short weak reference
var strong = weak.Target as BigObject;           // null means the object was collected
if (strong is null) strong = Rebuild();          // then hold the strong reference while you use it

// attach extra state to objects you don't own, without extending their lifetime
static readonly ConditionalWeakTable<Control, ViewState> State = new();
var vs = State.GetOrCreateValue(control);        // ViewState needs a parameterless constructor
State.AddOrUpdate(control, new ViewState());
```

A weak reference lets the garbage collector collect the object while you can still reach it; it is valid only until the object is collected, and the collector can get to the object before you re-establish a strong reference, so always copy `Target` into a local and null-check that.

## ConditionalWeakTable
- Attaches a value to a managed object (the key); both `TKey` and `TValue` must be reference types.
- Keys are compared by reference (`Object.ReferenceEquals`), not by an overridden `GetHashCode`/`Equals`.
- It does not keep keys alive: the entry is removed once no references to the key exist outside the table, even if a value in the table references that key.
- Useful methods: `Add`, `AddOrUpdate`, `TryAdd`, `GetOrAdd`, `GetOrCreateValue`, `TryGetValue`, `Remove`, `Clear`. It does not implement `IDictionary<TKey,TValue>`.
- Instances are thread safe; callers need no extra locking.

## Short and long weak references
- Short (the default): the target becomes null when the object is reclaimed.
- Long (`new WeakReference(obj, true)`): the reference survives after the object's `Finalize` has run, but the object's state is unpredictable. Use only when necessary.
- If the type has no finaliser, short-reference behaviour applies.

## Guidelines from the docs
- Weak references suit large objects that are cheap to recreate (the docs' example is a large tree view rebuilt on demand).
- Avoid them for small objects: the reference itself can be as large as the target.
- Do not use them as an automatic fix for memory problems; develop a proper caching policy instead.

## Checked
2026-11-08. Confirmed against the Weak References page (short and long references, guidelines, collection race) and the ConditionalWeakTable class page (reference equality, key lifetime, method list, thread safety, class constraints). Removed as unconfirmed on those pages: WeakReference<T>/TryGetTarget and IsAlive advice, WeakEventManager, event-handler leak fixes, MemoryCache comparison, value-type and string remarks, dotnet-gcdump advice and the GC.Collect test recipe.
Method: documentation only; no commands were run.
