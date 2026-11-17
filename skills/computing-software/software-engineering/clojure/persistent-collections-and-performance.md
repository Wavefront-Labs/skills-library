---
id: computing-software.software-engineering.clojure.persistent-collections-and-performance
name: persistent-collections-and-performance
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, vectors, maps, sets, lists, persistent, structural-sharing, conj, sorted-map, persistent-collections, clojure-data-structures]
level: practitioner
status: docs-checked
description: "Choose between list, vector, hash/sorted map and set using the documented cost model of Clojure's immutable persistent collections, and how conj behaves on each."
sources: ["https://clojure.org/reference/data_structures"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Persistent collections

**Goal:** pick the right collection and know its documented cost model.

All Clojure collections are immutable and persistent: "modified" versions are created efficiently by sharing
structure, and they are thread-safe.

## Choosing
| Need | Use | Documented behaviour |
| --- | --- | --- |
| indexed access, append | vector | access by index in log32N hops; `count` O(1); `conj` adds at the end; `rseq` reverses; a vector is a function of its indices |
| prepend, stack | list | `count` O(1); `conj` adds at the front; `peek`/`pop` support stack use; `seq` of an empty list is nil |
| keyed lookup | hash map | log32N access; `count` O(1); a map is a function of its keys; nil keys and values allowed |
| ordered keys | sorted map / sorted set | logN access; keys must be Comparable or use a supplied Comparator; `rseq` supported |
| membership | set `#{...}` | unique values; `contains?`, `disj`, `get`; a set is a function of its members |

- `conj` on a map accepts a map, a MapEntry or a two-item vector; an existing entry may be overwritten.
- Array maps keep key order but have linear lookup, so they suit only very small maps, and become hash maps
  after `assoc` modifies them. Do not rely on ordering of ordinary maps or sets (printed set order may differ
  from input).
- `clojure.set` provides union, difference and intersection.
- Equality is by value and collections conform to Java `hashCode()` specifications.

## Gotchas
- `(conj '(1 2) 0)` prepends; `(conj [1 2] 0)` appends.

## Self-check
`(let [a {:x [1]} b (update a :x conj 2)] [a b])` leaves `a` unchanged.

## Checked
Method: 2026-11-08 read clojure.org/reference/data_structures. The vectors reference page returned HTTP 403 and was dropped from sources. Removed claims the page does not state: PersistentQueue, update/assoc-in/get-in/merge-with recipes, get vs nth out-of-range behaviour, count on lazy seqs, and cross-type equality examples. Table and conj claims were rewritten to the page text; the self-check example is unchanged and unverified against the page.
