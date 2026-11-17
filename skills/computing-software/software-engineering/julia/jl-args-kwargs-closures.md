---
id: computing-software.software-engineering.julia.jl-args-kwargs-closures
name: jl-args-kwargs-closures
category: computing-software
field: software-engineering
product: julia
tags: [julia, jl-functions, args-kwargs-closures]
level: practitioner
status: docs-checked
description: "Use positional, optional and keyword arguments, splatting, do blocks and closures."
sources: ["https://docs.julialang.org/en/v1/manual/functions/", "https://docs.julialang.org/en/v1/manual/methods/", "https://docs.julialang.org/en/v1/manual/performance-tips/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Keyword arguments, varargs and anonymous functions
- Keyword arguments follow a `;`: `f(x; tol = 1e-6)`; they do not participate in dispatch.
- Optional positional `f(x, y = 2)` creates multiple methods; varargs `f(xs...)` and splat `f(v...)`.
- Anonymous `x -> x^2`; `map(x -> x + 1, xs)`; `do` block passes a function as first argument: `open(f) do io ... end`.
- A captured variable that is reassigned is boxed, which can lose performance; annotate its type or bind it with a `let` block (Performance Tips, captured variables).
Verify: `@code_warntype` on the function that returns the closure shows whether the captured variable is boxed.

## Checked

2026-11-02. Confirmed against: Manual pages Functions, Methods (keyword arguments do not participate in dispatch) and Performance Tips (captured variables, boxing, let blocks). Removed: the `Core.Box` name, which the manual never uses.
Method: documentation only; no commands were run.
