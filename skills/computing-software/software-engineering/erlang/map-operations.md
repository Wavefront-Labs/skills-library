---
id: computing-software.software-engineering.erlang.map-operations
name: map-operations
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-maps-records, map-operations]
level: practitioner
status: docs-checked
description: "Erlang maps: creation, update with := and =>, pattern matching, maps:get/find/put/merge/fold/iterator and ordering."
sources:
  - https://www.erlang.org/doc/system/reference_manual.html
  - https://www.erlang.org/doc/apps/stdlib/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Map syntax and the maps module
**Goal:** use maps correctly for dynamic key-value data.

```erlang
M0 = #{a => 1},
M1 = M0#{b => 2},             % add or update
M2 = M1#{a := 10},            % update existing key only, badkey otherwise
maps:get(a, M2, 0), maps:find(z, M2),      % 10, error
maps:merge(M1, #{b => 9}),                 % right side wins
maps:fold(fun(K, V, Acc) -> [{K,V}|Acc] end, [], M2),
maps:to_list(M2), maps:from_list([{x,1}]), maps:keys(M2), maps:remove(a, M2).
```
- `M#{K => V}` adds or replaces; `M#{K := V}` raises `badkey` if `K` is absent. A non-map `M` raises `badmap`.
- `1` and `1.0` are different keys (`M#{1.0 := b}` fails if only `1` exists).
- The Efficiency Guide calls maps with at most 32 elements small maps: avoid more than 32 elements if you can, since larger maps use more memory and keys can no longer be shared between instances.
- `maps:iterator/2` accepts `ordered` (map key order) or `reversed`; otherwise do not rely on iteration order.
- `maps:filtermap/2` is in stdlib.
- In patterns use `:=` only; the key may be any guard expression with bound variables.

## Gotchas
- `=>` never raises `badkey`, `:=` does.

## Self-check
Run the snippet and confirm `:=` on a missing key raises badkey.

## Checked
2026-11-02. Erlang Reference Manual "Expressions" (Map Expressions: update semantics, badkey/badmap, key comparison, patterns), Efficiency Guide "Maps" (32-element small map threshold), STDLIB `maps` module docs (iterator orders, filtermap). Removed: the flat-array/HAMT implementation claim, the "recent OTP" iterator hedge, and the unverified list of other maps functions.
Method: documentation only; no commands were run.
