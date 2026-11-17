---
id: computing-software.software-engineering.v-lang.v-map-iteration-and-ordering
name: v-map-iteration-and-ordering
category: computing-software
field: software-engineering
product: v-lang
tags: [v-map-iteration-and-ordering, maps, map iteration, for k v in, keys, values, sort keys, ordered map, v-lang]
level: practitioner
status: docs-checked
description: "Iterate V maps with for key, value in m, ignore keys or values with _, rely on insertion order, and update entries safely."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Iterating maps and ordering

Goal: traverse maps predictably.

- `for key, value in m { println('${key} -> ${value}') }`.
- Ignore a half with an underscore: `for key, _ in m { }` or `for _, value in m { }`. Keys as an array: `m.keys()`.
- Maps are ordered by insertion, like Python dictionaries. The docs call the order a guaranteed language feature but note it may change; sort keys for output that must stay stable (`mut ks := m.keys(); ks.sort()`).
- Indexing returns a copy of the stored value, so to update an entry assign through the key (`m[k] = new_value`) or mutate `m[key]` directly.
- Iterating a reference to a map (`for key, value in &m`) gives pointers to the entries for ordinary element types.
- A mutable loop value in a loop over a mutable map writes through to the map entry.

Verify: build a map, sort its keys and assert the order.

## Checked

Date: 2026-11-03. Confirmed in the V documentation (doc/docs.md, "Map for", "Maps", "Shared objects"). Removed as not stated: deleting or resizing a map inside the loop being unsafe, the `for k, mut v in m` spelling, converting a map to a sorted array of pairs, and the remark about `str()` form.

Method: documentation only; no commands were run.
