---
id: computing-software.software-engineering.erlang.compound-terms
name: compound-terms
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-types, compound-terms]
level: intro
status: docs-checked
description: "Erlang compound types: tuples, proper and improper lists, cons cells, strings as lists, and the type-ordering rule."
sources:
  - https://www.erlang.org/doc/system/reference_manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tuples, lists, maps and funs
**Goal:** pick the right container and compare terms predictably.

- Term order across types: number < atom < reference < fun < port < pid < tuple < map < nil < list < bit string. `nil` is `[]`.
- Tuples compare by size first, then element by element; lists compare element by element; maps compare by size, then keys in ascending key order, then values.
- Integers and floats share one order (`5 == 5.0`); `=:=` and `=/=` distinguish them.
```erlang
lists:sort([b, 1, "x", {a}, 2.0]).   % [1,2.0,b,{a},"x"]
```
- `[H | T]` builds a list by prepending. `++` copies its left operand, so build lists by prepending and `lists:reverse/1` at the end.

## Gotchas
- Appending in a loop with `Acc ++ [X]` copies the growing accumulator every iteration (quadratic).

## Self-check
Sort a mixed list in the shell and match it against the ordering rule above.

## Checked
2026-11-02. Reference Manual "Expressions" (Term Comparisons: type order, tuple/list/map rules, int/float comparison), Efficiency Guide "List Handling" (`++` copies its left operand, build in reverse). Removed: O(1)/O(n) complexity claims for tuples and lists, improper-list and `length/1` `badarg` claims (not in these pages).
Method: documentation only; no commands were run.
