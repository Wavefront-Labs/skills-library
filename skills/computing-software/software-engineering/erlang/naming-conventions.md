---
id: computing-software.software-engineering.erlang.naming-conventions
name: naming-conventions
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-style, naming-conventions]
level: intro
status: draft
description: "Erlang naming and layout conventions: snake_case functions and atoms, CamelCase variables, module prefixes, export grouping."
sources:
  - https://www.erlang.org/doc/apps/stdlib/
  - https://www.erlang.org/doc/apps/tools/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Naming and layout conventions
**Goal:** write code that reads like standard Erlang.

- Atoms, functions, modules: `snake_case`. Variables: `CamelCase`; ignored variables `_Name`.
- Modules live in a flat namespace: prefix with the app (`myapp_session`); name behaviours by role (`myapp_handler`).
- Predicates: `is_valid/1`; functions that raise on failure may use a `!`-free name but document it; convert functions `x_to_y/1`.
- Layout: one module per concern; group `-export` by purpose with comments; put `-spec` right above its function; keep functions short.
- Return `{ok, V}` / `{error, Reason}`; use atoms for reasons, not strings.
```erlang
-spec is_valid(binary()) -> boolean().
```

## Gotchas
- Naming a local variable like a macro or atom (e.g. `State` vs `state`) confuses readers and tools.

## Self-check
Review one module against the list and rename the worst offender.
