---
id: computing-software.software-engineering.elixir.ets-tables-types-ownership
name: ets-tables-types-ownership
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, ets, ets-new, ets-lookup, ets-insert, named-table, read-concurrency, table-owner, ordered-set, ets-tables, elixir-ets]
level: advanced
status: docs-checked
description: "Create ETS tables with the right type and access options, know owner process lifetime, and use lookup, insert and match specs."
sources: ["https://www.erlang.org/doc/apps/stdlib/ets.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ETS tables: types, access and ownership

**Goal:** fast shared in-memory tables with correct ownership.

```elixir
t = :ets.new(:cache, [:set, :public, :named_table, read_concurrency: true, write_concurrency: true])
:ets.insert(:cache, {:a, 1})
:ets.lookup(:cache, :a)              #=> [{:a, 1}]
:ets.insert_new(:cache, {:a, 2})     #=> false (key exists)
:ets.update_counter(:cache, :hits, {2, 1}, {:hits, 0})   # atomic increment with default
:ets.delete(:cache, :a) ; :ets.select(:cache, [{{:"$1", :"$2"}, [{:>, :"$2", 0}], [:"$1"]}])
:ets.tab2list(:cache) ; :ets.info(:cache, :size) ; :ets.delete(:cache)
```

## Rules
- Types: `:set` (unique keys), `:ordered_set` (sorted, unique), `:bag`, `:duplicate_bag`. Key position defaults to 1 (`keypos`).
- Access: `:public` (any process), `:protected` (default; others read), `:private` (owner only).
- A table is deleted when its owner process dies; create it in a long-lived process (a GenServer's `init/1`), or give it away with `heir`/`give_away`.
- Data is copied into and out of the table; storing huge terms is costly. Keep values small or store references.
- Operations on single objects are atomic; multi-step read-modify-write is not (use `update_counter` or serialise through one process).
- Wrap table access in one module so the table name stays private to it.

## Failure modes
- `ArgumentError` (`badarg`) after the owner died, or on a wrong table name.

## Self-check
Kill the owner process and confirm the named table disappears.

## Checked
2026-11-08: confirmed against the Erlang stdlib ets page (table types set, ordered_set, bag, duplicate_bag; protected default, keypos 1, heir and give_away, owner termination, badarg, update_counter, insert_new). Removed: the quoted error text and the defp wrapper wording.
Method: documentation only; no commands were run.
