---
id: computing-software.software-engineering.erlang.custom-behaviours
name: custom-behaviours
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-modules, custom-behaviours]
level: advanced
status: docs-checked
description: "Erlang custom behaviours: -callback attributes, behaviour_info/1 and the -behaviour module attribute."
sources:
  - https://www.erlang.org/doc/system/modules.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Defining behaviours with -callback
**Goal:** define an interface other modules implement.

```erlang
-module(storage).
-callback init(Opts :: map()) -> {ok, State :: term()} | {error, term()}.
-callback get(Key :: term(), State :: term()) -> {ok, term()} | not_found.
-callback close(State :: term()) -> ok.
```
Implementer:
```erlang
-module(mem_storage).
-behaviour(storage).
-export([init/1, get/2, close/1]).
```
- `-behaviour(Behaviour).` declares the module as a callback module; the atom can be a user-defined behaviour or one of `gen_server`, `gen_statem`, `gen_event`, `supervisor`. The spelling `-behavior` is also accepted.
- Callbacks are specified either by exporting `behaviour_info(callbacks) -> Callbacks` or by a `-callback Name(Arguments) -> Result.` attribute per callback.
- The `-callback` attribute is preferred, because its extra type information can be used by tools to produce documentation or find discrepancies.
- The module attribute `-doc(Documentation)` can document a function, type or callback.

## Gotchas
- A behaviour module must declare callbacks by one of the two methods above; do not assume tooling behaviour (compiler warnings, Dialyzer checks) beyond what your OTP version's tools report, and test it.

## Self-check
Remove a required callback from the implementer and see what the compiler reports in your OTP version.

## Checked
Method: docs-checked 2026-11-09 against https://www.erlang.org/doc/system/modules.html (Behaviour Module Attribute and documentation attribute sections read). Dropped unconfirmed claims about -optional_callbacks, compiler warnings, Dialyzer return checks and function_exported/3.
