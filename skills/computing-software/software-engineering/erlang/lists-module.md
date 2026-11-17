---
id: computing-software.software-engineering.erlang.lists-module
name: lists-module
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-stdlib-collections, lists-module]
level: intro
status: docs-checked
description: "Erlang lists module: map, foldl, filter, keyfind, sort, usort, partition, zip, seq, enumerate, uniq and complexity notes."
sources:
  - https://www.erlang.org/doc/apps/stdlib/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# The lists module
**Goal:** use lists functions fluently.

```erlang
lists:map(fun(X) -> X * 2 end, [1,2,3]),
lists:foldl(fun(X, Acc) -> X + Acc end, 0, L),     % fun gets (Elem, Acc)
lists:filter(fun is_atom/1, L), lists:partition(fun(X) -> X > 2 end, L),
lists:keyfind(id, 1, TupleList), lists:keystore(id, 1, TL, {id, 5}),
lists:sort(fun(A, B) -> A >= B end, L), lists:usort(L),
lists:zip([1,2],[a,b]), lists:seq(1, 10, 3), lists:uniq([1,1,2]),
lists:enumerate([a,b]).   % [{1,a},{2,b}] (OTP 25+)
```
- `lists:sort/2` takes `Fun(A, B)` that returns `true` if `A` compares less than or equal to `B` in the ordering you want; the sort is stable.
- `lists:usort/1` sorts and, of elements that compare equal (`==`), keeps only the first (`lists:usort([1.0,1])` is `[1.0]`).
- `lists:uniq/1` (OTP 25+) removes duplicates preserving the order of the first occurrences: `lists:uniq([3,3,1,2,1,2,3])` is `[3,1,2]`.
- `lists:foldl/3` and `foldr/3` both call `Fun(Elem, AccIn)`; `foldr` traverses right to left.
- `lists:flatten/1` flattens a deep list.

## Gotchas
- `foldl` and `foldr` use the same fun argument order; they differ only in traversal direction.

## Self-check
Compare `lists:usort/1` and `lists:uniq/1` on `[b,a,b,c,a]`.

## Checked
2026-11-02. STDLIB `lists` module docs (sort/2 ordering fun and stability, usort, uniq with OTP 25 since tag, enumerate OTP 25 since tag, foldl/foldr, keyfind/keystore, partition, zip, seq, flatten). Removed: O(n) cost claims for nth/last/length and the iolist advice (not in the module docs).
Method: documentation only; no commands were run.
