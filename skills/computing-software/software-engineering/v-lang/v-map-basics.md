---
id: computing-software.software-engineering.v-lang.v-map-basics
name: v-map-basics
category: computing-software
field: software-engineering
product: v-lang
tags: [v-map-basics, maps, map, mapstringint, hash map, delete, in, key, dictionary, v-lang]
level: intro
status: docs-checked
description: "Create and use V maps: map[K]V{} and literals, set and read keys, zero values for missing keys, or-blocks, in and delete, and key type limits."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Map creation, access and deletion

Goal: use V's built-in hash map.

- Create: `mut m := map[string]int{}`; literal `m := {'a': 1, 'b': 2}`. Update syntax copies another map: `{...base_map, 'b': 88}`.
- Set `m['c'] = 3`; read `m['c']`. A missing key returns the zero value by default (`0`, `''`).
- Handle a missing key with `or`: `v := m['x'] or { 0 }` (the docs example is `or { panic('key not found') }`). `if v := m['abc'] { ... }` unwraps only when present. A module tagged `@[strict_map_index]` rejects plain `m['bad_key']` reads.
- Membership `'a' in m`; remove `m.delete('a')`; size `m.len`; clear `m.clear()`.
- `m.keys()` and `m.values()` return arrays.
- Keys can be string, rune, integer, float, voidptr, enum, or fixed arrays of those; struct keys are rejected.
- Maps are ordered by insertion; the docs call this a guaranteed language feature that may change.
- Indexing returns a copy of the stored value. Mutate `m[key]` directly or assign the modified value back.

Gotchas:
- Reading a missing key without `or` silently gives zero, which hides bugs; use `in` or `or`.
- For concurrent updates declare the map `shared` (`shared words := map[string]int{}`); statements like `m[k] = v` then take a lock.

Verify: `assert m['zz'] or { -1 } == -1`.

## Checked

Date: 2026-11-03. Confirmed in the V documentation (doc/docs.md, "Maps", "Map update syntax", "Shared objects") and vlib/builtin/map.v (`keys`, `values`, `delete`, `clear`, `len`). Removed as not stated: `or { return err }` on a map read, the "older versions" caveat on struct keys (docs now reject them), and the "adding to a non-mut map" error wording.

Method: documentation only; no commands were run.
