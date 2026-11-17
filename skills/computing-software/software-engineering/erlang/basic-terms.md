---
id: computing-software.software-engineering.erlang.basic-terms
name: basic-terms
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-types, basic-terms]
level: intro
status: docs-checked
description: "Erlang scalar types: integer, float, atom, binary, pid, reference and port with type-test BIFs."
sources:
  - https://www.erlang.org/doc/system/reference_manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Numbers, atoms, bit strings and references
**Goal:** know the primitive term types and test them.

- Type tests: `is_integer/1`, `is_float/1`, `is_number/1`, `is_atom/1`, `is_binary/1`, `is_bitstring/1`, `is_pid/1`, `is_reference/1`, `is_port/1`, `is_function/1,2`.
- Integer vs float equality: `1 == 1.0` is `true`, `1 =:= 1.0` is `false`. Prefer `=:=` / `=/=` for exact comparison.
- Float to integer: `round/1`, `trunc/1`, `floor/1`, `ceiling/1`. Integer to float: `float/1`.
- References come from `make_ref/0` and are unique among connected nodes.
```erlang
is_integer(10),  10 / 4,  10 div 4,  10 rem 4.   % true, 2.5, 2, 2
```
- Float errors: `1/0` raises `badarith`; floats never become infinity or NaN in Erlang.

## Gotchas
- `/` always returns a float; use `div` for integer division.

## Self-check
In the shell, check `1 == 1.0`, `1 =:= 1.0`, and `#{1 => a}` lookup with `1.0`.

## Checked
2026-11-02. Confirmed: system/data_types.html: =:=, make_ref/is_reference, is_function/1,2, badarith on float overflow/division.
Removed: OTP 20 note and map-key gotcha (not confirmed in the page).
Method: documentation only; no commands were run.
