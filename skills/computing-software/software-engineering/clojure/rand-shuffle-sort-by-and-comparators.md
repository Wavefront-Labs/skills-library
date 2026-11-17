---
id: computing-software.software-engineering.clojure.rand-shuffle-sort-by-and-comparators
name: rand-shuffle-sort-by-and-comparators
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, rand, rand-int, shuffle, sort, sort-by, compare, comparator, frequencies, group-by, partition, random-math-sorting]
level: practitioner
status: docs-checked
description: "Generate random values (rand, rand-int, rand-nth, shuffle), sort with sort/sort-by and comparators (stable), and aggregate with frequencies, group-by, partition and reduce-kv."
sources: ["https://clojure.github.io/clojure/clojure.core-api.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Random, sorting and aggregation

**Goal:** the small utilities used in almost every program.

```clojure
(rand)  (rand-int 10)  (rand-nth xs)  (shuffle xs)
(sort [3 1 2])  (sort > xs)  (sort-by :age people)  (sort-by (juxt :age :name) people)
(sort-by :n #(compare %2 %1) xs)                           ; descending via comparator
(frequencies "abca")   ;=> {\a 2, \b 1, \c 1}
(group-by even? (range 6))   (partition 2 xs)  (partition-all 2 xs)  (partition-by odd? xs)
(reduce-kv (fn [m k v] (assoc m k (inc v))) {} counts)
(max-key :n a b)  (apply max xs)  (distinct xs)  (dedupe xs)  (take-nth 2 xs)
```
- `sort` and `sort-by` return a sorted seq, use `compare` when no comparator is given, and are guaranteed stable. A supplied comparator must implement `java.util.Comparator`. If the coll is a Java array it is modified; sort a copy to avoid that.
- `compare` is like Java `compareTo` but also works for nil and compares numbers and collections in a type-independent manner; x must implement Comparable.
- `rand` returns a float from 0 (inclusive) to n (default 1, exclusive); `rand-int` an integer from 0 to n (exclusive); `rand-nth` has the performance of `nth` on the collection.
- `partition` with no pad may drop an incomplete tail (given a pad it completes the last partition as far as the pad allows); `partition-all` may include a shorter final partition.
- `group-by` returns vectors in original order; `max-key` returns the last x when several tie; `reduce-kv` works on vectors with indices as keys and returns init for an empty coll.

## Failure modes
- Comparing values that are not Comparable with `compare` (for example maps) is an error: sort with `sort-by` on a comparable key.

## Self-check
Sort people by age descending then name ascending using `sort-by` and `juxt` with negation.

## Checked
2026-11-03. Confirmed against the clojure.core API docstrings for rand, rand-int, rand-nth, shuffle, sort, sort-by, compare, frequencies, group-by, partition, partition-all, partition-by, reduce-kv, max-key, distinct, dedupe and take-nth. Removed: the java.util.Random seeding remarks, test.check seeding advice, the boolean-comparator remark, the top-N counter idiom, and the ClassCastException and IndexOutOfBounds failure modes (not on the pages read).
Method: documentation only; no commands were run.
