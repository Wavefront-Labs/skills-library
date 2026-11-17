---
id: computing-software.software-engineering.java.navigablemap-range-queries
name: navigablemap-range-queries
category: computing-software
field: software-engineering
product: java
tags: [java, java-collections, navigablemap, treemap, floorentry, ceilingkey, submap, concurrentskiplistmap]
level: practitioner
status: docs-checked
description: "Use TreeMap/NavigableMap for floor/ceiling lookups, range views (subMap, headMap, tailMap), and interval tables; know the comparator, null-key and thread-safety rules."
sources: ["https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/NavigableMap.html", "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/TreeMap.html", "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/ConcurrentSkipListMap.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NavigableMap range queries

**Use when** you need "closest key", "all keys between a and b", or tiered lookups (rate bands, time slots).

## Navigation methods
```java
NavigableMap<Integer,String> tiers = new TreeMap<>(Map.of(0, "free", 100, "pro", 1000, "enterprise"));
tiers.floorEntry(250).getValue();      // greatest key <= 250 -> "pro"
tiers.ceilingKey(250);                 // least key >= 250 -> 1000
tiers.lowerKey(100);                   // strictly less -> 0
tiers.higherKey(100);                  // strictly greater -> 1000
tiers.firstEntry();  tiers.pollLastEntry();
```
The lookups return `null` when there is no such key or entry (for example `floorKey` below the smallest key).

## Range views (backed by the map)
```java
tiers.subMap(0, true, 1000, false);    // [0, 1000)
tiers.headMap(100, true);              // keys <= 100
tiers.tailMap(100, false).clear();     // removes keys > 100 from the original map
tiers.descendingMap();                 // reverse-order view
```
Views are backed by the map: changes through one are reflected in the other. A range view throws `IllegalArgumentException` if you insert a key outside its range, or build a submap with an endpoint outside its range. For `subMap(from, fromInclusive, to, toInclusive)` with equal endpoints the result is empty unless both are inclusive.

## Interval lookup pattern
Store `start -> value`, then `var e = map.floorEntry(x); if (e != null && x < e.getValue().end())` (a placeholder `end()` accessor). This works for non-overlapping intervals only.

## Gotchas
- A sorted map compares keys with its comparator, so two keys that compare equal are the same key. The ordering must be consistent with `equals` for the map to obey the general `Map` contract; behaviour is well-defined otherwise, but the map no longer follows that contract.
- `TreeMap` is not synchronized: external synchronisation is needed if several threads access it and at least one modifies its structure (or wrap with `Collections.synchronizedSortedMap` at creation).
- `ConcurrentSkipListMap` supports concurrent access; its iterators are weakly consistent and it does not permit null keys or values.
- With natural ordering (or a comparator that does not permit nulls), a null key throws `NullPointerException`.
- `TreeMap` guarantees log(n) cost for `containsKey`, `get`, `put` and `remove`.

## Verify
Test boundary keys: an exact hit, a key below the smallest (`floorKey` returns `null`), and a key above the largest.

## Checked
2026-11-03. Confirmed against the Java SE 21 pages for NavigableMap, TreeMap and ConcurrentSkipListMap: method names and semantics, backed views, `IllegalArgumentException` for out-of-range inserts, equal-endpoint submap rule, consistency with equals, synchronisation note, weakly consistent iterators, null-key rules, log(n) cost statement.
Removed (not in the pages read): a blanket "all navigation methods are O(log n)" claim, "`size()` on a subMap is O(n)", the `String.CASE_INSENSITIVE_ORDER` example, the in-place key mutation warning, and the NavigableSet remark.
Method: documentation only; no commands were run.
