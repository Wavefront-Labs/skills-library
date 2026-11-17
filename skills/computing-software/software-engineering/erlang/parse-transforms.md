---
id: computing-software.software-engineering.erlang.parse-transforms
name: parse-transforms
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-compiler, parse-transforms]
level: sme
status: draft
description: "Erlang parse transforms: parse_transform/2, forms manipulation with erl_syntax, merl and alternatives."
sources:
  - https://www.erlang.org/doc/apps/tools/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Parse transforms and erl_syntax
**Goal:** know when a parse transform is justified and how it works.

```erlang
-module(add_log).
-export([parse_transform/2]).
parse_transform(Forms, _Options) ->
    io:format("forms: ~p~n", [length(Forms)]),
    Forms.                                   % return (modified) abstract forms
```
Use in a module with `-compile({parse_transform, add_log}).` (must be compiled first, in a different application or earlier in the build).
- Helper libraries: `erl_syntax`, `erl_syntax_lib` (syntax tools) and `merl` for quasi-quoting.
- Stdlib users: `ms_transform` (ETS `fun2ms`), `qlc`.
- Parse transforms hide control flow and break tooling; prefer macros, behaviours or plain functions.
- Order of transforms matters; transform output must still be valid for later passes.

## Gotchas
- Abstract format changes between OTP releases occasionally (new node types); pin tests per OTP version.

## Self-check
Apply a trivial transform that counts function forms and print the number.
