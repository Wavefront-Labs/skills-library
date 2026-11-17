---
id: computing-software.software-engineering.v-lang.v-option-type
name: v-option-type
category: computing-software
field: software-engineering
product: v-lang
tags: [v-option-type, option-and-result-types, option, int, none, optional, or block, if guard, nullable, v-lang]
level: practitioner
status: docs-checked
description: "Return and consume ?T options with none, unwrap with or blocks, if-guards and the ? propagation operator."
sources:
  - https://github.com/vlang/v/blob/master/doc/docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Option types ?T and none

Goal: represent "maybe a value" without null.

- Option types are declared by prepending `?` to the type: `?User`. An option stores either a value or `none`; it has no error field.
- Declare: `fn find(id int) ?User { for ... { if ... { return user } } return none }`. V wraps a plain returned value automatically.
- Consume with an `or` block: `u := find(1) or { User{} }` (default value of the same type), `u := find(1) or { return }` (early exit), `or { panic(err) }` for a forced unwrap (V has no `unwrap()`).
- Propagate with `?` after the call: the enclosing function must return an option as well. `or { return none }` also propagates absence.
- `if u := find(1) { use(u) } else { ... }` unwraps with an if guard; `u` is only in scope for the first branch. An option's `or` block and failed guard do not bind `err`.
- Create an option variable directly: `x := ?int(none)`, `?string(none)`, `?User(none)`.
- Trailing option-typed parameters can be omitted in calls; V supplies `none`: `fn connect(url string, timeout ?int)`, then `timeout or { 1000 }`.
- `?` alone on a function (return type `?`) is an option of `void`.
- `break` and `continue` in an `or` block work only inside a `for` loop.

Gotcha: use a result `!T` when the reason for failure matters; options carry no error.

Verify: `assert (find(0) or { User{id: -1} }).id == -1`.

## Checked

Date: 2026-11-02. Confirmed in the V documentation (doc/docs.md, "Option/Result types and error handling", "Handling options/results", "If unwrapping"). Removed as not stated there: "unhandled `?` in main is a compile error" (the docs say propagation in `main` panics), optional struct field syntax `name ?string` with `!= none` checks as written, the "or block must end with a value" wording.

Method: documentation only; no commands were run.
