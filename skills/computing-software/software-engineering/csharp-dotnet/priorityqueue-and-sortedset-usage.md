---
id: computing-software.software-engineering.csharp-dotnet.priorityqueue-and-sortedset-usage
name: priorityqueue-and-sortedset-usage
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, csharp-collections, priorityqueue-sortedset, priorityqueue, sortedset, sorteddictionary, sortedlist]
level: practitioner
status: docs-checked
description: "Choose .NET PriorityQueue<TElement,TPriority>, SortedSet, SortedDictionary and SortedList: min-heap order, .NET 9 Remove for priority updates, complexity trade-offs."
sources: ["https://learn.microsoft.com/en-us/dotnet/core/whats-new/dotnet-6", "https://learn.microsoft.com/en-us/dotnet/core/whats-new/dotnet-9/libraries", "https://learn.microsoft.com/en-us/dotnet/standard/collections/sorted-collection-types", "https://learn.microsoft.com/en-us/dotnet/standard/collections/when-to-use-generic-collections"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PriorityQueue and sorted collections

## PriorityQueue (.NET 6+)
`PriorityQueue<TElement, TPriority>` holds items with a priority and dequeues the **lowest priority value first** (it is a min heap, implemented as an array heap).

- Array heaps do not support priority updates efficiently, which made them awkward for Dijkstra-style algorithms. **.NET 9 adds `Remove`**, which lets you emulate a priority update (remove the item, enqueue it again with the new priority) at **O(n)** time; Microsoft says this suits education, prototyping and cases where asymptotic performance is not a blocker.

## Sorted collections
- `SortedList<K,V>` and `SortedDictionary<K,V>` keep entries sorted by key using an `IComparer<T>`, implement `IDictionary`, and do not have the O(1) insert and lookup of hash tables. Both retrieve in O(log n).
  - `SortedList`: keys and values are indexed (efficient indexed retrieval); insertion and removal are generally O(n), but O(log n) when data arrive already in sorted order (appended at the end, if no resize is needed); uses less memory.
  - `SortedDictionary`: no indexed retrieval; insertion and removal are O(log n); uses more memory. Microsoft calls it a useful alternative to `SortedList`.
- `SortedSet<T>` is a self-balancing tree that keeps data sorted after insertions, deletions and searches, and implements `ISet<T>` (as does `HashSet<T>`).
- For concurrent sorted access, Microsoft suggests adding sorting logic to a class derived from `ConcurrentDictionary`. `ImmutableSortedSet` and `ImmutableSortedDictionary` are the immutable counterparts.
- For values that contain their own key, `KeyedCollection<TKey,TItem>` gives list-and-dictionary behaviour.

## Verify
Test a scheduler: enqueue shuffled priorities and assert ascending dequeue order. Test an updated priority through `Remove` followed by `Enqueue`.

## Checked
2026-11-03. Confirmed against dotnet/docs: What's new in .NET 6 (PriorityQueue min heap), What's new in .NET 9 libraries (PriorityQueue.Remove, array heap, O(n) update emulation), Sorted collection types and Commonly used collection types. Removed because not found there (API reference pages are not in dotnet/docs): 4-ary heap detail, enqueue/dequeue/peek complexities, `EnqueueRange`, `TryDequeue`/`TryPeek` usage, stability and tie-break advice, thread-safety remarks, `GetViewBetween` and `Reverse` details, comparer pitfalls, and the claim "No decrease-key or remove" (wrong since .NET 9, which added `Remove`).
Method: documentation only; no commands were run.
