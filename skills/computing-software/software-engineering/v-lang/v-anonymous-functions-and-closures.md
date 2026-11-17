---
id: computing-software.software-engineering.v-lang.v-anonymous-functions-and-closures
name: v-anonymous-functions-and-closures
category: computing-software
field: software-engineering
product: v-lang
tags: [v-anonymous-functions-and-closures, functions, anonymous function, closure, lambda, callback, function type, capture, v-lang]
level: practitioner
status: docs-checked
description: "Create anonymous functions, lambdas and closures with explicit capture lists, understand copy-on-capture, and pass functions as callbacks."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Anonymous functions and closures

Goal: use first-class functions safely.

- Anonymous fn: `double_fn := fn (n int) int { return n + n }`; pass it as `op fn (int) int`, call `run(5, double_fn)`. Named functions can also be passed (`run(5, sqr)`) and stored in arrays or maps (`fns := [sqr, cube]`).
- Lambda expressions `|x| x + 4` are small anonymous functions valid only inside calls to higher-order functions: `a.map(|x| x * 10)`, `f(|x| x + 4)`.
- Closures list their captures explicitly: `my_closure := fn [my_int] () { println(my_int) }`.
- Captured variables are copied when the function is created; later changes to the original are not seen. `fn [mut i] () int { i++; return i }` makes the closure's own copy mutable: the original is untouched but the change persists across calls (a counter factory returns 1, 2, 3).
- To share state with the outside, capture a reference: `mut ref := &i; fn [ref] () { println(*ref) }`.
- Callback types: `type Filter = fn (string) string`.
- For callbacks such as `os.walk` that must update caller state, use `os.walk_with_context` with a reference.

Gotchas:
- Variables must be listed in the capture list to be used; there is no implicit capture.

Verify: create a counter closure with `fn [mut i]`, call it three times and assert 1, 2, 3.

## Checked

Date: 2026-11-03. Confirmed in the V documentation (doc/docs.md, "Anonymous & higher order functions", "Lambda expressions", "Closures", and the `type Filter = fn (string) string` example). Removed as not stated: that `mut` capture shares the original by reference (the docs say the opposite), `==` comparison to `unsafe { nil }`, allocation and backend-specific closure caveats.

Method: documentation only; no commands were run.
