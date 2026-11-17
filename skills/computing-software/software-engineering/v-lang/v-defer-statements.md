---
id: computing-software.software-engineering.v-lang.v-defer-statements
name: v-defer-statements
category: computing-software
field: software-engineering
product: v-lang
tags: [v-defer-statements, defer-and-goto, defer, cleanup, resource management, close, unlock, function exit, v-lang]
level: practitioner
status: docs-checked
description: "Schedule cleanup with defer that runs at function exit, in reverse order, for file handles and locks, with scope caveats."
sources:
  - https://github.com/vlang/v/blob/master/doc/docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# defer for cleanup

Goal: release resources reliably.

- `defer { f.close() }` after `mut f := os.open(path)!` runs the block when the surrounding scope ends; the docs show it firing on an early `return` and at the end of the function.
- If the function returns a value, the `defer` block runs after the return expression is evaluated (so `error(...)` text still sees the file open).
- Multiple `defer` statements in one scope run in reverse order of appearance.
- `defer` inside a loop body runs once per iteration, at the end of that iteration's scope.
- `defer(fn) { ... }` defers to the end of the function even from an inner scope (inside an `if` or `for`).
- Inside a `defer` block, `$res()` reads the returned value (single return); `$res(idx)` for multi-return.
- A panic runs the pending `defer` blocks of every function on the stack, newest first. Calling `recover()` directly in one returns the panic message (an option, `none` when there is no panic) and stops the panic; the function then returns the zero value of its result type. Signals such as a segmentation fault cannot be recovered.
- A `defer` body inherits the `unsafe` context where it is written.

Verify: print in defers and check the reversed order.

## Checked

Date: 2026-11-02. Confirmed in the V documentation (doc/docs.md, "Defer", "defer in loop scopes", "defer(fn) {}", "Recovering from panics"). Removed as not stated there: "defer is function-scoped by default" (docs say it runs when the surrounding scope ends), the claim that panics skip defers (the docs say the opposite), `mu.lock()/unlock()` pairing and manual-free examples, and the evaluation-time remark.

Method: documentation only; no commands were run.
