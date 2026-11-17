---
id: computing-software.software-engineering.erlang.funs
name: funs
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-functions, funs]
level: practitioner
status: docs-checked
description: "Erlang fun expressions: anonymous funs, closures, fun M:F/A references, named funs and calling convention."
sources:
  - https://www.erlang.org/doc/system/reference_manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Funs, closures and named funs
**Goal:** pass behaviour around as values.

```erlang
Add = fun(X) -> fun(Y) -> X + Y end end,
(Add(1))(2).                       % 3
F1 = fun lists:reverse/1,          % external fun
F2 = fun local_name/2,             % local fun
Fact = fun Self(0) -> 1; Self(N) -> N * Self(N - 1) end.
```
- The optional name of a fun must be a variable; variables in the fun head shadow the name, and both shadow variables of the surrounding clause.
- `fun Name/Arity` is sugar for a fun that calls the local function; `Name/Arity` must be an existing local function.
- `fun Module:Name/Arity` refers to the latest version of the module and does not depend on the code of the module that defines the fun. `Module`, `Name` and `Arity` can be variables (since R15).
- A fun is called as `F(Args)`; `M:F(Args)` with variable atoms is a dynamic remote call. `is_function(F, 1)` tests for a fun of arity 1.

## Gotchas
- Calling `Module:Name(...)` or an external fun always uses the latest module version; a local call stays in the current version. See the code loading chapter.

## Self-check
Build a closure counter factory in the shell and call it twice.

## Checked
2026-11-02. Erlang Reference Manual "Expressions" (Fun Expressions, Function Calls) and "Data Types" (is_function). Removed: `erlang:fun_info`, `badfun` after hot reload, funs sent between nodes, ETS storage and lazy `undef` claims (not stated in these pages).
Method: documentation only; no commands were run.
