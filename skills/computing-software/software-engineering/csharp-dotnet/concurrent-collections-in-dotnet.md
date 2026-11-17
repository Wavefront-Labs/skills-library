---
id: computing-software.software-engineering.csharp-dotnet.concurrent-collections-in-dotnet
name: concurrent-collections-in-dotnet
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, csharp-concurrency, concurrentdictionary, concurrentqueue, blockingcollection, thread-safe-collections, lock-free]
level: practitioner
status: docs-checked
description: "Choose System.Collections.Concurrent types: ConcurrentDictionary GetOrAdd factory races, queue and stack, ConcurrentBag pools, bounded BlockingCollection."
sources: ["https://learn.microsoft.com/en-us/dotnet/standard/collections/thread-safe/", "https://learn.microsoft.com/en-us/dotnet/standard/collections/thread-safe/how-to-add-and-remove-items", "https://learn.microsoft.com/en-us/dotnet/standard/collections/thread-safe/blockingcollection-overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Concurrent collections

## Which collection
- `List<T>` and `Dictionary<TKey,TValue>` do no synchronisation; your code must lock when several threads add or remove. If threads only read a shared collection, the plain generic collections are fine.
- Use `System.Collections.Concurrent` types when several threads write. The old `ArrayList`/`Hashtable` `Synchronized` wrappers lock the whole collection on every add or remove, do not scale and are not protected from race conditions.
- `ConcurrentQueue<T>` (FIFO) and `ConcurrentStack<T>` use `Interlocked` operations rather than locks. `ConcurrentBag<T>` is an unordered thread-safe collection; Microsoft's object-pool how-to uses it to reuse objects instead of continually creating them.
- `BlockingCollection<T>` adds bounding (a maximum capacity) and blocking to any `IProducerConsumerCollection<T>`; by default it wraps a `ConcurrentQueue<T>`. Bounding stops producers running too far ahead of consumers; blocking on a full collection only happens if you gave a capacity. `GetConsumingEnumerable()` lets a consumer `foreach` items until the collection is completed.
- The concurrent types implement `ICollection` but `IsSynchronized` always returns `false` and `SyncRoot` is always `null`.

## ConcurrentDictionary
```csharp
var cache = new ConcurrentDictionary<string, Lazy<Task<Data>>>();
var data = await cache.GetOrAdd(key, k => new Lazy<Task<Data>>(() => LoadAsync(k))).Value;
cache.AddOrUpdate(key, 1, (_, old) => old + 1);
```
- `GetOrAdd` with a factory is not atomic with the add: two threads can both invoke `valueFactory`, only one result is stored, and the value returned is not guaranteed to be the one your factory created. The same applies to `AddOrUpdate`. If the factory has side effects or is expensive, store a `Lazy<T>` as above so the work runs once.
- A thread-safe collection does not make composite "check then add" sequences atomic; use the combined methods (`GetOrAdd`, `AddOrUpdate`).

## Verify
A stress test with many parallel operations against expected totals; a counter inside the factory shows how often it ran with and without the `Lazy` wrapper.

## Checked
2026-11-03. Confirmed against dotnet/docs: "Thread-safe collections" overview, "How to add and remove items from a ConcurrentDictionary" (GetOrAdd/AddOrUpdate factory race) and the BlockingCollection overview and how-to. Removed because not found in the pages read: `TryRemove(KeyValuePair)` version note, locking behaviour of `Count`/`Keys`/`ToArray`, enumeration snapshot semantics, `ConcurrentDictionary<T, byte>` as a set, `ImmutableInterlocked`, `FrozenDictionary` guidance, Channels comparison, memory-overhead remarks.
Method: documentation only; no commands were run.
