---
id: computing-software.software-engineering.elixir.map-mapset-api
name: map-mapset-api
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, map, mapset, map-put, map-update, map-merge, map-fetch, map-take, map-api, elixir-collections]
level: practitioner
status: docs-checked
description: "Use Map functions (put, update, fetch, merge, take, drop, new) and MapSet for membership with correct atom-key vs string-key syntax."
sources: ["https://hexdocs.pm/elixir/Map.html", "https://hexdocs.pm/elixir/MapSet.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Map and MapSet

**Goal:** read and update maps without KeyErrors or lost keys, following the `Map`, `MapSet` and `Kernel` docs.

```elixir
m = %{name: "Ann", age: 3}
m.name                           # "Ann"; raises KeyError for a missing key
m[:name]                         # Access syntax; nil for a missing key
Map.get(m, :x, :default)         # :default
Map.fetch(m, :x)                 #=> :error  ({:ok, value} when present)
Map.fetch!(m, :x)                # raises KeyError
%{m | age: 4}                    # update syntax: only existing keys, KeyError otherwise
Map.put(m, :x, 1)
Map.put_new(m, :name, "B")       # keeps the existing value
Map.update(m, :age, 0, &(&1 + 1))   # (map, key, default, fun)
Map.merge(a, b, fn _key, v1, v2 -> v1 + v2 end)
Map.take(m, [:name])
Map.drop(m, [:age])
Map.has_key?(m, :name)
is_map_key(m, :name)             # also usable in guards
Map.pop(m, :name)
Map.new(list, fn x -> {x.id, x} end)

s = MapSet.new([1, 2])
MapSet.member?(s, 1)
MapSet.union(s, MapSet.new([3]))
```

## Rules
- Maps are the "go to" key-value structure; keys can be of any type, are compared with `===`, and duplicates are not allowed (the last one in a literal prevails).
- Key-value pairs in a map do not follow any order: never depend on iteration order.
- When the key is an atom the `key: value` shorthand works; if mixed with `=>` the shorthand must come at the end.
- `map[key]` is for dynamically created maps with any key; `map.key` is for maps with predetermined atom keys expected to be present (structs are one example). Do not add parentheses (`data.key()`), that tries to call a function on a module.
- A map pattern matches when the right-hand map contains the pattern's keys with matching values, so `%{}` matches every map; `^var` can be used as a key in a match (`%{^n => :one} = ...`).
- The update syntax `%{map | key: value}` raises `KeyError` when the key does not exist; use `Map.put/3` to add keys.

## Self-check
`%{a: 1} |> Map.put("a", 2) |> map_size()` is 2: the atom key and the string key are different keys.

## Checked
Date: 2026-11-02. Confirmed against the Map, MapSet and Kernel docs (map semantics, order, access syntax, update syntax KeyError, pattern matching, pinned keys, function names and arities). Removed: 32-key sorted/hash trie claim, atom/string key mixing advice, Map.filter and Map.keys examples, MapSet details beyond new/member?/union.
Method: documentation only; no commands were run.
