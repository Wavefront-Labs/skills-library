---
id: computing-software.software-engineering.java.collections-framework-and-immutable-collections
name: collections-framework-and-immutable-collections
category: computing-software
field: software-engineering
product: java
tags: [java, java-collections, immutable-collections, list-of, sequenced-collections]
level: practitioner
status: docs-checked
description: "Use Java unmodifiable collections correctly (List.of, copyOf snapshots, toUnmodifiable collectors) and Java 21 sequenced collections (getFirst, getLast, reversed)."
sources:
  - https://docs.oracle.com/en/java/javase/21/core/creating-immutable-lists-sets-and-maps.html
  - https://openjdk.org/jeps/431
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Collections framework and immutable collections

**Goal:** keep shared collections unmodifiable and use the Java 21 sequenced collection API.

## Unmodifiable collections (Java 21 Core Libraries guide)
- `List.of`, `Set.of`, `Map.of` and `Map.ofEntries` create unmodifiable collections: elements cannot be added, removed or replaced.
- Prefer unmodifiable collections for data that does not change (space efficiency, protection from accidental modification). For data modified throughout the program use a modifiable collection: in-place changes are cheap, while changing an unmodifiable one means copying it.
- Snapshot a collection you built up with the `copyOf` family, for example `List<Item> snapshot = List.copyOf(list);`. The copy is isolated from later changes to the original; if the original is already unmodifiable, `copyOf` returns a reference to it instead of copying.
- To guarantee a stream result is unmodifiable, use the `Collectors.toUnmodifiable...` collectors (the guide lists them).
- `Collections.unmodifiableList/Set/Map` wrap an existing collection (the guide shows them applied to a variable); `copyOf` is the way to take an independent snapshot.

## Sequenced collections (JEP 431, Java 21)
- `SequencedCollection` adds `reversed()`, `addFirst`, `addLast`, `getFirst`, `getLast`, `removeFirst`, `removeLast`; `SequencedSet` and `SequencedMap` follow, the latter with `sequencedKeySet()`, `sequencedValues()` and `sequencedEntrySet()`.
- `reversed()` returns a reverse-ordered view: changes to the original show in the view and, where permitted, view changes write through.
- It replaces the old idiom `list.get(list.size() - 1)` with `getLast()`.
- Collections like `SortedSet`, which position elements by comparison, cannot support `addFirst`/`addLast`; those methods can throw `UnsupportedOperationException`.
- On `LinkedHashSet`, `addFirst`/`addLast` move an element that is already present to the new position.

## Verify
- [ ] Shared and returned collections are unmodifiable or snapshots made with `copyOf`.
- [ ] Code targeting Java 21 uses `getLast()`/`reversed()` rather than index arithmetic.

## Checked
2026-11-01. Confirmed against the Oracle Java 21 "Creating Immutable Lists, Sets, and Maps" guide and JEP 431. Removed as unconfirmed by those pages (dev.java page returned no text): implementation choice table, presizing, null handling and iteration-order claims, collection traps, record example.
Method: documentation only; no commands were run.
