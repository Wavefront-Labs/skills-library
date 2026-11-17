---
id: computing-software.software-engineering.erlang.function-clauses
name: function-clauses
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-functions, function-clauses]
level: intro
status: docs-checked
description: "Erlang function definitions: multiple clauses, name/arity identity, tail recursion, accumulators and body recursion."
sources:
  - https://www.erlang.org/doc/system/reference_manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Function clauses, arity and recursion
**Goal:** structure code as ordered clauses and tail-recursive loops.

```erlang
sum(L) -> sum(L, 0).
sum([], Acc) -> Acc;
sum([H|T], Acc) -> sum(T, Acc + H).
```
- A function is defined by module, name and arity, so `f/1` and `f/2` are different functions. Clauses are tried top to bottom; if none matches, a `function_clause` error occurs. Separate clauses with `;` and end the last with `.`.
- Tail-recursive calls do not consume the call stack, so an infinite tail-recursive loop can run forever.
- A call whose result is combined afterwards (`1 + f(N-1)`) is not tail-recursive.
- A process main loop must be tail-recursive or its stack grows until the process terminates.

## Gotchas
- Body recursion over a long list grows the stack in proportion to the depth.

## Self-check
Run `sum/2` on a million-element list in the shell.

## Checked
2026-11-02. Reference Manual "Functions" (arity, clause order, function_clause, tail recursion), Efficiency Guide "Processes" (tail-recursive main loop). Removed: warnings_as_errors/unused-variable advice, "mutual recursion" and "try/catch breaks tail calls" claims, and the heap-allocated-stack remark (not in these pages).
Method: documentation only; no commands were run.
