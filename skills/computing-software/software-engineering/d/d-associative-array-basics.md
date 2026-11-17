---
id: computing-software.software-engineering.d.d-associative-array-basics
name: d-associative-array-basics
category: computing-software
field: software-engineering
product: d
tags: [d-associative-array-basics, associative-arrays, associative-array, aa, hash-map, in-operator, remove, get, require, update, d]
level: intro
status: docs-checked
description: "Create and use V[K] associative arrays: literals, in-operator lookup, get with default, remove, require, update, and key type rules (opEquals and toHash)."
sources:
  - https://dlang.org/spec/hash-map.html
  - https://dlang.org/phobos/object.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Associative array basics: declare, insert, lookup, remove

Goal: use built-in hash maps correctly.

```d
int[string] count;
count["a"] = 1;
if (auto p = "a" in count) ++*p;     // pointer or null
int n = count.get("z", 0);           // default without insert
count.require("b", 5);               // insert if missing, return ref
count.update("a", () => 1, (ref int v) { ++v; });
count.remove("a");
```
- Literal: `auto m = ["x": 1, "y": 2];`; `.length` (read-only), `.clear()` removes all keys and values from every reference to the same AA (`destroy(aa)` only nulls your reference).
- Reading a missing key with `m["q"]` throws `RangeError`; use `in` or `get`.
- Key types need `opEquals` and `toHash` (structs get them automatically if members do); do not mutate a key after insertion.
- `.dup` copies, assignment aliases.
- Initialise: an AA variable is null until first assignment; passing a null AA by value then inserting does not affect the caller (pass `ref`).

Gotchas:
- Ordering is unspecified.

Verify: unittest checks `"missing" !in m` and a get default.

## Checked

Date 2026-11-02. Confirmed against the Associative Arrays spec page and the object module page: literals, in/remove, keys/values/length, get/require/update, clear. Removed the unconfirmed claim that AAs are unusable in @nogc and the old-compiler clear() remark.

Method: documentation only; no commands were run.
