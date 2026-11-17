---
id: computing-software.software-engineering.erlang.typespecs
name: typespecs
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-dialyzer, typespecs]
level: practitioner
status: docs-checked
description: "Erlang -spec, -type, -opaque, -callback, built-in types and map type syntax with := and =>."
sources:
  - https://www.erlang.org/doc/system/design_principles.html
  - https://www.erlang.org/doc/apps/tools/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Type specifications and -type/-opaque
**Goal:** write specs that carry real information.

```erlang
-type id() :: pos_integer().
-opaque queue() :: {list(), list()}.
-type opts() :: #{timeout => timeout(), retries := non_neg_integer()}.
-export_type([id/0, queue/0]).
-spec fetch(id(), opts()) -> {ok, binary()} | {error, not_found | timeout}.
```
- Predefined types include `term()`, `atom()`, `binary()`, `integer()`, `pos_integer()` (`1..`), `non_neg_integer()` (`0..`), `[T]`, `nonempty_list(T)`, `map()`, `fun((A) -> B)`, `iolist()`, `iodata()`, `timeout()` (`infinity | non_neg_integer()`), `pid()`, `reference()`, `module()` (an atom), `mfa()`, `no_return()` (same as `none()`) and `none()`.
- In map types, `:=` marks a mandatory association and `=>` an optional one.
- An opaque type's structure is not to be visible outside its defining module (only that module may depend on it); it should be exported.
- Nominal types (`-nominal`) were introduced in OTP 28.

## Gotchas
- A spec as broad as `term()` everywhere tells readers and tools little.

## Self-check
Add specs to a module and compile it to confirm the types resolve.

## Checked
2026-11-02. Reference Manual "Types and Function Specifications" (predefined and built-in type tables, map association kinds, opaque and nominal types). Removed: the Dialyzer-warns-on-inspection claim, the record-field gotcha and the "prove nothing" Dialyzer claim (not in this page).
Method: documentation only; no commands were run.
