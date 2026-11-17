---
id: computing-software.software-engineering.erlang.guard-expressions
name: guard-expressions
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-pattern, guard-expressions]
level: practitioner
status: docs-checked
description: "Erlang guards: allowed BIFs, comma vs semicolon, andalso/orelse, is_map_key, map_get and guard failure semantics."
sources:
  - https://www.erlang.org/doc/system/reference_manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Guard sequences and allowed guard BIFs
**Goal:** write guards that compile and behave as intended.

```erlang
f(X) when is_integer(X), X > 0 -> pos;          % comma: and
f(X) when is_atom(X); is_binary(X) -> text;     % semicolon: or
f(M) when is_map_key(id, M), map_get(id, M) > 1 -> ok.
```
- A guard sequence is guards separated by `;` (true if at least one guard is true); a guard is guard expressions separated by `,` (true if all are true).
- Guard expressions are a side-effect-free subset of expressions: variables, constants, constructors, term comparisons, arithmetic, boolean and short-circuit (`andalso`/`orelse`) expressions, and calls to the type-test BIFs and these others: `abs/1`, `bit_size/1`, `byte_size/1`, `element/2`, `float/1`, `hd/1`, `is_map_key/2`, `length/1`, `map_get/2`, `map_size/1`, `max/2` and `min/2` (OTP 26+), `node/0,1`, `round/1`, `self/0`, `size/1`, `tl/1`, `trunc/1`, `tuple_size/1`.
- If an expression or BIF call in a guard fails (bad arguments), the whole guard fails and the next guard after `;` is tried; no exception escapes.
- User-defined functions cannot be called in guards (only the BIFs above).
- Old type tests without the `is_` prefix are kept only for compatibility and are allowed only at top level, not inside boolean expressions.

## Gotchas
- `==` compares numbers by value (`5 == 5.0`); use `=:=` where exactness matters.

## Self-check
Write a function with each guard form and call it with a wrong-typed argument to see the clause is skipped.

## Checked
2026-11-02. Erlang Reference Manual "Expressions" (Guard Sequences, Guard Expressions with both BIF tables, Term Comparisons). Removed: the claim that `and`/`or` are not allowed in guards (they are boolean expressions and are allowed) and an unsupported comparison gotcha.
Method: documentation only; no commands were run.
