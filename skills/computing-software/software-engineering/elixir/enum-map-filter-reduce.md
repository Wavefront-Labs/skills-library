---
id: computing-software.software-engineering.elixir.enum-map-filter-reduce
name: enum-map-filter-reduce
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, enum, map, filter, reduce, group-by, frequencies, sort-by, chunk-every, zip, enum-essentials, elixir-enum-stream]
level: practitioner
status: docs-checked
description: "Use the Enum module idiomatically: map/filter/reduce, group_by, frequencies, sort_by, chunk_every, zip, max_by; all are eager."
sources: ["https://hexdocs.pm/elixir/Enum.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enum functions: map, filter, reduce, group_by

**Goal:** transform enumerables with the right Enum function instead of reduce for everything.

```elixir
Enum.map(1..3, &(&1 * 2))
Enum.filter(list, &(&1 > 1)) ; Enum.reject(list, &is_nil/1)
Enum.reduce(list, %{}, fn x, acc -> Map.update(acc, x, 1, &(&1 + 1)) end)
Enum.frequencies(~w(a b a))                 #=> %{"a" => 2, "b" => 1}
Enum.group_by(users, & &1.role, & &1.name)
Enum.sort_by(users, & &1.age, :desc)
Enum.chunk_every(1..6, 2) ; Enum.zip([1, 2], [:a, :b]) ; Enum.with_index(list, 1)
Enum.max_by(users, & &1.age, &>=/2, fn -> nil end)   # 3rd arg is the sorter, 4th the empty fallback
Enum.flat_map(list, &[&1, &1]) ; Enum.uniq_by(list, & &1.id) ; Enum.into(list, %{})
Enum.find(list, default, &(&1 > 3)) ; Enum.any?(list, pred) ; Enum.sum(list) ; Enum.count(list, pred)
```

## Rules
- Enum functions are eager and each pass creates an intermediate list; chain many with `Stream` or a single `reduce`/`for`.
- They work on anything implementing `Enumerable` (lists, maps as `{k, v}` tuples, ranges, streams).
- Enum functions run in linear time, including `count/1`, `member?/2` and `at/2`; a data type may supply a faster variant.
- `Enum.sort/2` accepts `:asc`/`:desc` (shorthand for `&<=/2` and `&>=/2`) or a module such as `Date` (also `{:desc, Date}`). The sort is stable only if the sorter returns true for equal values.

## Failure modes
- `Enum.EmptyError` for `Enum.max/3` or `max_by/4` on an empty enumerable without an `empty_fallback`; `Protocol.UndefinedError` for non-enumerables.

## Self-check
`Enum.map(%{a: 1}, fn {k, v} -> {k, v + 1} end)` returns a list of tuples, not a map; pipe into `Enum.into(%{})`.

## Checked
2026-11-03: confirmed against the Enum module docs (signatures of `max_by/4`, `find/3`, `with_index/2`, `sort/2` sorters and stability, linear time note, `EmptyError`, `Enum.sort(dates, Date)`). Fixed: `max_by` third argument is the sorter, not the empty fallback. Removed: the `Map.new/2` suggestion and the `File.stream!`/MapSet Enumerable list.
Method: documentation only; no commands were run.
