---
id: computing-software.software-engineering.erlang.ets-tables
name: ets-tables
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-ets, ets-tables]
level: practitioner
status: docs-checked
description: "Erlang ETS: set, ordered_set, bag, access rights, named_table, concurrency options, ownership and heir."
sources:
  - https://www.erlang.org/doc/apps/stdlib/
  - https://www.erlang.org/doc/apps/erts/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ETS table types, access and ownership
**Goal:** pick the right ETS table configuration.

```erlang
T = ets:new(cache, [set, public, named_table, {keypos, 1},
                    {read_concurrency, true}, {write_concurrency, true}]),
true = ets:insert(T, {user1, <<"ann">>}),
[{user1, Name}] = ets:lookup(T, user1),
ets:insert_new(T, {user1, x}),                 % false, key exists
ets:update_counter(cache, hits, {2, 1}, {hits, 0}),   % atomic increment with default object
ets:delete(T).
```
- Types: `set` and `ordered_set` hold one object per key; `bag` and `duplicate_bag` allow several. `set` matches keys exactly (`1` and `1.0` differ); `ordered_set` compares keys with `==` so `1` and `1.0` are the same key.
- Access: `public`, `protected` (default: the owner reads and writes, others read) and `private`.
- A table is destroyed when its owner process terminates unless it has an `{heir, Pid, Data}`, which inherits it.
- Every insert and lookup copies the object, so avoid storing huge terms if copying dominates.
- `ets:insert_new/2` returns `false` if the key exists. `update_counter/4` takes a default object used when the key is missing.
- `ets:info(T, size)` is the number of objects and `ets:info(T, memory)` the words allocated.

## Gotchas
- When the owner crashes without an heir the cache is lost; create the table in a long-lived process.

## Self-check
Kill the owner and confirm the table disappears; then add an heir and repeat.

## Checked
2026-11-02. STDLIB `ets` docs (table types, key matching vs compare-equal, default protection, heir, copy-on-access implementation note, insert_new, update_counter/4, info items). Removed: nothing contradicted; the `{keypos, 1}` and concurrency options are as documented in the `new/2` option list.
Method: documentation only; no commands were run.
