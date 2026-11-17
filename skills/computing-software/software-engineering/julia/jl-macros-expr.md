---
id: computing-software.software-engineering.julia.jl-macros-expr
name: jl-macros-expr
category: computing-software
field: software-engineering
product: julia
tags: [julia, jl-macros, macros-expr]
level: advanced
status: docs-checked
description: "Write hygienic macros, inspect expansion with @macroexpand and know when functions suffice."
sources: ["https://docs.julialang.org/en/v1/manual/metaprogramming/", "https://docs.julialang.org/en/v1/stdlib/InteractiveUtils/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Expr, quoting, macros and generated functions
- `quote ... end` and `:(...)` create `Expr`; `$x` interpolates; `dump(ex)` shows structure.
- `macro twice(ex); :($(esc(ex)); $(esc(ex))); end` uses `esc` for caller expressions; hygiene renames macro-introduced locals.
- `@macroexpand @m x` shows the result; `@code_lowered` shows lowered code.
- Prefer functions or multiple dispatch; use macros for syntax and compile-time work. In a `@generated` function body you only have access to the argument types, not their values.
Verify: test macro behaviour with `@macroexpand` and `@test`.

## Checked

2026-11-03. Confirmed against: Manual Metaprogramming (`quote`, `:()`, `$`, `dump`, `esc`, hygiene, `@macroexpand`, generated functions see types only) and InteractiveUtils (`@code_lowered`). Removed: the unsupported "prefer functions" justification detail and the word "IR" for `@code_lowered`.
Method: documentation only; no commands were run.
