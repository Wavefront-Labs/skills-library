---
id: computing-software.software-engineering.erlang.function-attributes-spec
name: function-attributes-spec
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-functions, function-attributes-spec]
level: practitioner
status: docs-checked
description: "Erlang -spec contracts and naming conventions for result tuples, arity overloads and default-style wrappers."
sources:
  - https://www.erlang.org/doc/system/reference_manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Function specs and arity conventions
**Goal:** document functions so Dialyzer and readers agree.

```erlang
-spec find(Key :: atom(), [{atom(), term()}]) -> {ok, term()} | error.
find(K, L) -> case lists:keyfind(K, 1, L) of {_, V} -> {ok, V}; false -> error end.
```
- `-spec Function(ArgType1, ..., ArgTypeN) -> ReturnType.` - the arity must match the function or compilation fails. `-spec Module:Function(...)` is also allowed if `Module` is the current module.
- Argument names (`Key :: atom()`) are for documentation.
- A spec can be overloaded with several clauses separated by `;`; the argument domains should not overlap or Dialyzer warns.
- A function is identified by name and arity, so a "default argument" is written as a separate lower-arity function that calls the full one.
- Type variables in a spec relate input and output types.

## Gotchas
- Two arities with the same name are different functions; keep their jobs conceptually related.

## Self-check
Add a spec and check that a wrong arity fails to compile.

## Checked
2026-11-02. Reference Manual "Types and Function Specifications" (spec syntax, arity rule, argument names, overloading and Dialyzer warning, type variables) and "Functions" (identity by name and arity). Removed: `{ok,V}`/`error` return conventions, the "Fun!" style, the `-spec` placement rule and the `rebar3 dialyzer` self-check (not in these pages).
Method: documentation only; no commands were run.
