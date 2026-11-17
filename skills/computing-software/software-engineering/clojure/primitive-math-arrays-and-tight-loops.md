---
id: computing-software.software-engineering.clojure.primitive-math-arrays-and-tight-loops
name: primitive-math-arrays-and-tight-loops
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, performance, primitives, unchecked-math, arrays, aget, aset, type-hints, reflection, performance-primitives-loops, clojure-performance]
level: advanced
status: docs-checked
description: "Speed up numeric hot paths in Clojure with type hints, *warn-on-reflection*, primitive arrays, ^long/^double function hints and (sparingly) unchecked math."
sources: ["https://clojure.org/reference/java_interop"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Primitives and tight loops

**Goal:** make number-crunching code avoid reflection and boxing.

```clojure
(set! *warn-on-reflection* true)               ; default is false; warns on unresolved method calls
(defn sum-array ^long [^longs xs]
  (let [n (alength xs)]
    (loop [i 0 acc 0]
      (if (< i n) (recur (inc i) (+ acc (aget xs i))) acc))))
(def arr (long-array [1 2 3]))
```
- Type hints are metadata tags consumed by the compiler; they go on parameters, let-bound names, var names and
  expressions, and let the compiler resolve method calls at compile time (the docs show a hinted `len2` about
  ten times faster than the unhinted `len`). Static fields and static method return values need no hints.
- A function return hint goes before the parameter vector.
- Functions have limited primitive support: only `long` and `double` hints generate primitive-typed overloads,
  e.g. `(defn foo ^long [^long n] ...)`, and only for arity up to 4.
- Arrays: `aget` and `aset` are overloaded for primitive arrays; constructors include `int-array` and
  `float-array`; hints are written `^ints`, `^floats`. The docs recommend arrays mainly for interop with Java
  libraries that need them.
- Unchecked integer (int/long) operations favour speed over safety; the docs say not to rush to them unless you
  want truncating operations, since HotSpot optimises the overflow check, which throws instead of truncating.
  The dynamic var `*unchecked-math*` swaps safe operations for unchecked ones automatically.

## Self-check
Time the loop against `(reduce + coll)` on 10 million elements and compare allocation in a profiler.

## Checked
Method: 2026-11-08 read clojure.org/reference/java_interop (type hints, primitive arrays, unchecked math, primitive function hints). The datatypes-and-protocols news post was not relied on and was removed from sources. Removed unsupported claims: :warn-on-boxed mode, loop-local primitive and recur-matching rules, areduce/amap, overflow-throws example for +, collections always boxing, criterium advice, failure modes. The sum-array code was not run.
