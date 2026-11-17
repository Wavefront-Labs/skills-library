---
id: computing-software.software-engineering.csharp-dotnet.collections-immutable-and-frozen
name: collections-immutable-and-frozen
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, csharp-collections, frozen-collections, immutable-collections, collection-expressions, dictionary, readonly-collections]
level: practitioner
status: docs-checked
description: "Pick .NET collections by workload: List/Dictionary/HashSet, IReadOnly* interfaces vs ImmutableArray vs FrozenDictionary/FrozenSet, collection expressions and capacity tips."
sources: ["https://learn.microsoft.com/en-us/dotnet/standard/collections/", "https://learn.microsoft.com/en-us/dotnet/api/system.collections.frozen", "https://learn.microsoft.com/en-us/dotnet/api/system.collections.immutable", "https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/collection-expressions"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Collections: immutable and frozen

**Goal:** the right collection for read-heavy lookups, shared state and APIs, without
accidental mutation or wasted allocations.

## Everyday types
| Need | Type |
|---|---|
| ordered, indexed | `List<T>` (presize: `new List<T>(n)`) |
| key lookup | `Dictionary<TKey, TValue>` (use `TryGetValue`) |
| membership | `HashSet<T>` |
| FIFO / LIFO / priority | `Queue<T>`, `Stack<T>`, `PriorityQueue<TElement, TPriority>` |
| sorted | `SortedDictionary`, `SortedSet` |
| concurrent | `ConcurrentDictionary`, `ConcurrentQueue`, `Channel<T>` |
Pass a comparer for case-insensitive keys: `new Dictionary<string, int>(StringComparer.OrdinalIgnoreCase)`.

## Read-only vs immutable vs frozen
- `IReadOnlyList<T>` / `IReadOnlyDictionary<,>`: an interface promise - callers can't mutate
  through it, but the owner (or a cast) can. `AsReadOnly()` wraps without copying.
- `ImmutableArray<T>`, `ImmutableList<T>`, `ImmutableDictionary<,>`: never change; "mutations"
  return new instances with structural sharing. Use builders for bulk construction.
- `FrozenDictionary<,>` / `FrozenSet<T>` (System.Collections.Frozen, .NET 8+): built once (`ToFrozenDictionary()`) and never changed. Suited to configuration and static lookups that live for the app lifetime; measure before choosing them over `Dictionary` for speed.
```csharp
private static readonly FrozenDictionary<string, Handler> Routes =
    new Dictionary<string, Handler> { ["/a"] = A, ["/b"] = B }.ToFrozenDictionary(StringComparer.Ordinal);
```

## Collection expressions
```csharp
int[] a = [1, 2, 3];
List<string> names = [];
ImmutableArray<int> ia = [1, 2, 3];
int[] merged = [..a, ..other, 42];        // spread
```
Collection expressions are target-typed; the spread element `..` inlines another collection.

## API design
Accept the most general interface you need (`IEnumerable<T>` if you iterate once,
`IReadOnlyCollection<T>` if you need Count); return concrete or read-only types that callers
can't corrupt your state through. Avoid enumerating an `IEnumerable<T>` more than once.

## Gotchas
- Modifying a `List`/`Dictionary` during `foreach` throws `InvalidOperationException`.
- `ConcurrentDictionary` value factories (`AddOrUpdate`, `GetOrAdd`) may be called more than once under contention; wrap values in `Lazy<T>` if creation must happen once.

## Verify
- [ ] Static lookup tables use `FrozenDictionary`/`FrozenSet`.
- [ ] Public properties don't expose mutable internal lists.

## Checked

Checked 2026-10-25 against dotnet/docs (standard/collections, collection-expressions) and dotnet/dotnet-api-docs (FrozenDictionary, ConcurrentDictionary) on main.
Confirmed: `System.Collections.Frozen` types ship from .NET 8 (assembly 8.0.0.0); collection expression spread element `..`; `ConcurrentDictionary` factories may be called multiple times; collection type selection table categories.
Removed as unconfirmed: relative read/write speed claims for immutable and frozen collections, `CollectionsMarshal.GetValueRefOrAddDefault`, the C# 12 label, CA1851 rule id, `Dictionary` enumeration order note.

Method: documentation only; no commands were run.
