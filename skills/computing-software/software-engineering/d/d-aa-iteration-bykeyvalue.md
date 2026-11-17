---
id: computing-software.software-engineering.d.d-aa-iteration-bykeyvalue
name: d-aa-iteration-bykeyvalue
category: computing-software
field: software-engineering
product: d
tags: [d-aa-iteration-bykeyvalue, associative-arrays, bykey, byvalue, bykeyvalue, aa-iteration, keys, values, sorted-output, d]
level: practitioner
status: docs-checked
description: "Walk AAs with foreach, .byKey, .byValue, .byKeyValue, .keys/.values and produce deterministic sorted output; avoid mutating while iterating."
sources:
  - https://dlang.org/spec/hash-map.html
  - https://dlang.org/phobos/object.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Iterating associative arrays and sorted output

Goal: iterate AAs correctly and deterministically.

- `foreach (k, v; aa)` and `foreach (k, ref v; aa)` to mutate values in place.
- Lazy ranges: `aa.byKey`, `aa.byValue`, `aa.byKeyValue` (elements have `.key`, `.value`); `byKey`/`byValue`/`byKeyValue` return forward ranges.
- Eager arrays: `aa.keys`, `aa.values` allocate copies; `aa.dup` clones.
- Sorted output: `foreach (k; aa.keys.sort) writeln(k, aa[k]);` (`import std.algorithm : sort`; `.sort` yields a SortedRange, use `.array` if needed) or `aa.byKeyValue.array.sort!((a,b) => a.key < b.key)`.
- Counting: `aa[key]++` on a possibly-new key, as in the spec's pair-counting example.
- Convert with `std.array.assocArray(zip(keys, vals))`.

Gotchas:
- The aggregate of a `foreach` must be loop invariant: do not add or remove keys in the loop body; collect keys first.
- Iteration order is unspecified (`keys` and `values` agree with each other only while the AA is not reorganized); sort for tests.

Verify: unittest compares `aa.byKey.array.sort` to a fixed array.

## Checked

Date 2026-11-02. Confirmed byKey/byValue/byKeyValue forward ranges, foreach over AAs and the loop-invariant aggregate rule (Associative Arrays spec). Removed the V.init/idup claims, the no-allocation claim, and the cross-compiler ordering claim (order is only unspecified).

Method: documentation only; no commands were run.
