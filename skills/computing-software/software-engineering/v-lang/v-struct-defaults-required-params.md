---
id: computing-software.software-engineering.v-lang.v-struct-defaults-required-params
name: v-struct-defaults-required-params
category: computing-software
field: software-engineering
product: v-lang
tags: [v-struct-defaults-required-params, structs, default values, required, params, named arguments, config struct, v-lang]
level: practitioner
status: docs-checked
description: "Give fields defaults, force callers to set fields with @[required], and pass optional named arguments with @[params] structs."
sources:
  - https://github.com/vlang/v/blob/master/doc/docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Default values, @[required] and @[params] structs

Goal: emulate keyword arguments and safe defaults.

- Defaults: `struct Foo { n int  s string  a []int  pos int = -1 }`. All fields are zeroed by default (`n` is 0, `s` is `''`); array and map fields are allocated; `= -1` is a custom default.
- `@[required]` after the field type forces explicit initialization: `struct Foo { n int @[required] }`; `_ = Foo{}` then fails to compile.
- V has no default or named function arguments; use trailing struct literal syntax instead. `@[params]` on a struct whose type is the last function parameter lets you pass fields directly: `new_button(text: 'Click me', width: 100)`, with omitted fields taking their defaults (`height int = 20`).
- Both the struct name and braces can be omitted at the call. This only works for functions that take a struct as the last argument.
- `@[params]` also lets the trailing parameter be omitted entirely (`new_button()`). Without it you must give at least one field name, otherwise the compiler reports `error: expected 1 arguments, but got 0`.
- A keyword-named field can follow a default on the next line (`enabled bool = true`, then `in string`).

Verify: call with and without named args and assert the default applies.

## Checked

Date: 2026-11-02. Confirmed in the V documentation (doc/docs.md, "Default field values", "Required fields", "Trailing struct literal arguments"). Removed as not stated there: the old-syntax `[required]` migration remarks and the 2024 cutoff, defaults from constants/expressions, the "evaluated per initialisation" gotcha.

Method: documentation only; no commands were run.
