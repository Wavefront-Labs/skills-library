---
id: computing-software.software-engineering.erlang.ets-match-specs
name: ets-match-specs
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-ets, ets-match-specs]
level: advanced
status: docs-checked
description: "ETS selection: match patterns, select with ms_transform fun2ms, continuations, select_delete, safe_fixtable and partially bound ordered_set keys."
sources:
  - https://www.erlang.org/doc/apps/stdlib/ets.html
  - https://www.erlang.org/doc/apps/stdlib/ms_transform.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Match specifications and select
**Goal:** filter inside ETS without copying the whole table.

```erlang
-include_lib("stdlib/include/ms_transform.hrl").
MS = ets:fun2ms(fun({K, V}) when V > 10 -> K end),
Keys = ets:select(T, MS),
{Part, Cont} = ets:select(T, MS, 100),            % paged
ets:select_delete(T, ets:fun2ms(fun({_, V}) when V < 0 -> true end)).
ets:match_object(T, {'_', '$1'}).
```
- `ets:fun2ms/1` is translated by a parse transform at compile time, triggered by including `ms_transform.hrl`; without the header the fun is not translated and may fail at runtime. The resulting match spec is as efficient as a hand-written one.
- `ets:select/2` with a match specification is far more efficient than `ets:foldl/3` for filtering. In match patterns `'$1'` binds variables and `'_'` matches anything.
- `ets:tab2list/1` returns a list of all objects in the table, so it copies everything. `ets:safe_fixtable/2` fixes a `set`, `bag` or `duplicate_bag` table for safe traversal with `first/next`, `match`, `match_object` or `select`.
- A match pattern with a fully bound key becomes a single key lookup. For `ordered_set`, a partially bound key (a list or tuple with a fully bound prefix) limits the traversal to a subset of the table.
- `ets:select/3` takes a limit and returns a continuation for `ets:select/1`.

## Self-check
Insert 10000 rows and compare `ets:select/2` with `tab2list` + filter.

## Checked

2026-11-03. Confirmed in the `ets` and `ms_transform` pages: `select/2,3`, continuations, `select_delete/2`, `match_object/2`, `tab2list/1`, `safe_fixtable/2`, `foldl/3`, `fun2ms` parse transform behaviour and partially bound `ordered_set` keys. Removed: the `[{Head, Guards, Body}]` shape claim, the "blocks nothing but burns CPU" gotcha and the missed/duplicate keys claim.
Method: documentation only; no commands were run.
