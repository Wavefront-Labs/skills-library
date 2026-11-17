---
id: computing-software.software-engineering.java.hashmap-internals-and-key-design
name: hashmap-internals-and-key-design
category: computing-software
field: software-engineering
product: java
tags: [java, java-collections, hashmap-internals, load-factor, treeification, initial-capacity, mutable-keys, linkedhashmap]
level: advanced
status: docs-checked
description: "Understand HashMap capacity, load factor, resizing and iteration order; size it with HashMap.newHashMap, use immutable keys, LinkedHashMap access order for LRU."
sources: ["https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/HashMap.html", "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/LinkedHashMap.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HashMap internals and key design

## How it works (as documented)
- The capacity is the number of buckets; the default is capacity 16 and load factor 0.75. When the number of entries exceeds load factor x current capacity, the table is rehashed to roughly twice the buckets.
- Get and put are constant time provided the hash function disperses elements properly. Many keys with the same `hashCode()` slow any hash table; when keys are `Comparable`, HashMap may use comparison order to break ties.
- Iteration order is not guaranteed and may change over time.
- Iteration costs time proportional to capacity plus size, so do not set the initial capacity too high.
- Iterators are fail-fast (`ConcurrentModificationException`) on a best-effort basis; use that only to detect bugs, never for correctness.

## Sizing
If the initial capacity is greater than the maximum number of entries divided by the load factor, no rehash ever occurs. The Javadoc says to use `HashMap.newHashMap(int numMappings)` to create a map sized for an expected number of mappings (there is also a `HashSet.newHashSet` equivalent; verify it in the Javadoc for your JDK). `new HashMap<>(n)` alone sets the capacity to `n`, so with the default 0.75 load factor it rehashes before holding `n` entries.

## Key rules
1. Keys must be effectively immutable: lookups rely on `hashCode` and `equals`, so mutating a field they use after insertion makes the entry unreachable by the original key.
2. Keep `equals` and `hashCode` consistent (see `equals-hashcode-and-comparable-contracts`).
3. Do not use arrays as keys (arrays use identity equality); wrap in `List.of(...)` or a record.
4. `BigDecimal` equality includes scale (`2.0` is not equal to `2.00`), so it surprises as a key.

## Variants
- `new LinkedHashMap<>(16, 0.75f, true)` creates an access-ordered map (the third argument is `accessOrder`: true for access order, false for insertion order); overriding `removeEldestEntry(Map.Entry)` removes stale mappings as new ones are added, which gives an LRU cache. In an access-ordered map even `get` is a structural modification. Not synchronized: wrap with `Collections.synchronizedMap(...)` at creation time, or use a cache library.
- `computeIfAbsent`, `merge`, `getOrDefault` replace get/put sequences.
- `IdentityHashMap`, `WeakHashMap`, `EnumMap` serve specialised keys.

## Gotchas
- HashMap is not synchronized: if several threads access it and at least one modifies it structurally, synchronise externally (or use `ConcurrentHashMap`).
- HashMap permits null values and one null key (and is "roughly equivalent to Hashtable, except that it is unsynchronized and permits nulls").

## Verify
Write a test inserting a mutable key, mutating it, and asserting `containsKey` fails - then replace the key with a record to fix it.

## Checked
Read the HashMap and LinkedHashMap Javadoc (Java 21): default capacity and load factor, rehash to twice the buckets, Comparable tie-breaking, newHashMap, unsynchronized, fail-fast, null handling, accessOrder constructor, removeEldestEntry, access-order get as structural modification. Removed because the Javadoc does not state them: the bucket-index formula, the 8-node/64-table treeification thresholds, "since Java 8/19" version claims, the Java 7 infinite-loop story, and the computeIfAbsent-modification warning.
Method: docs-only read of cited pages, 2026-11-08
