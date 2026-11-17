---
id: computing-software.software-engineering.crystal.hash-api
name: hash-api
category: computing-software
field: software-engineering
product: crystal
tags: [hash-api, stdlib-collections, hash, hash-default, fetch, merge, transform-values, each-pair, key, dig, insertion-order, has-key, crystal]
level: intro
status: docs-checked
description: "Use Hash(K, V): literal syntax, [] vs []?, fetch, default blocks, each, delete, merge, transform_values, group and compare ordering."
sources:
  - https://crystal-lang.org/reference/
  - https://crystal-lang.org/api/
  - https://github.com/crystal-lang/crystal/tree/master/src
  - https://github.com/crystal-lang/crystal-book/tree/master/docs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hash API

Goal: use Hash well.

- Literal: `{"a" => 1}`; empty `{} of String => Int32`; `Hash(String, Int32).new(0)` default value (shared object for mutable defaults); `Hash(String, Array(Int32)).new { |h, k| h[k] = [] of Int32 }` default block.
- Read: `h["k"]` raises KeyError, `h["k"]?` nil, `h.fetch("k", d)`, `h.dig("a", "b")`, `h.has_key?`, `h.key_for(v)`.
- Write: `h["k"] = v`, `delete`, `merge(other)`, `merge!`, `update(k) { |v| ... }`, `reject!`, `select`, `transform_values`, `transform_keys`, `to_a`, `sort_by`, `group_by` (on Enumerable).
- Iteration is insertion ordered; key types need `hash` and `==`.

Gotchas:
- Mutating a key object after insertion breaks lookups.
- `Hash#each` with a block param `|k, v|` destructures the pair.
- Concurrent mutation across threads needs a Mutex.

Verify: spec count words via `Hash(String, Int32).new(0)`.

## Checked

Date 2026-11-03. Confirmed Hash#[], []?, fetch, dig, key_for, has_key?, update, merge, merge!, reject!, select, transform_values, transform_keys and the default value and default block constructors, including the warning that a default value is returned as-is (not duplicated), in the Crystal Hash source. group_by and sort_by come from Enumerable (confirmed there).

Method: documentation only; no commands were run.
