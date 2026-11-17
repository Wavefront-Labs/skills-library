---
id: computing-software.software-engineering.v-lang.v-nested-maps-and-struct-values
name: v-nested-maps-and-struct-values
category: computing-software
field: software-engineering
product: v-lang
tags: [v-nested-maps-and-struct-values, maps, nested map, map of arrays, map of structs, counting, group by, default value, v-lang]
level: practitioner
status: docs-checked
description: "Use maps of arrays, maps of maps and maps of structs, with counting, grouping and update patterns that respect copy-on-read."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nested maps and complex value types

Goal: model grouped data without panics.

- Missing keys return the zero value, so a count can be `c[w] = c[w] + 1`.
- Group into arrays: check first, then append or create, as in the docs: `if _ := data[key] { data[key] << value } else { data[key] = [value] }` with `mut data := map[string][]int{}`.
- Map of maps: `mut m := map[string]map[string]int{}`; assign an inner map with `m['greet'] = {'Hello': 1}`; the docs also assign `m['code']['orange'] = 123` directly.
- Map of structs: `m['a'] = User{name: 'x'}`. Postfix updates such as `m[key].level++` update the stored entry and insert a zero value first when the key is absent.
- Indexing a map returns a copy of the stored value (also with `or {}` and `if v := m[key] {}`); mutating that local copy does not change the map. Assign the modified value back or mutate `m[key]` directly.

Verify: count words in a sentence and assert the frequency map.

## Checked

Date: 2026-11-03. Confirmed in the V documentation (doc/docs.md, "Maps", nested map example, map update note on copies, and the opening note on `m[key].level++`). Removed as not stated: `map[string]&User` for shared values, large-array copy claims, and the "confirm in your version" caveats.

Method: documentation only; no commands were run.
