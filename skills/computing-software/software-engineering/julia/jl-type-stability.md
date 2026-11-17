---
id: computing-software.software-engineering.julia.jl-type-stability
name: jl-type-stability
category: computing-software
field: software-engineering
product: julia
tags: [julia, jl-multiple-dispatch, type-stability]
level: advanced
status: docs-checked
description: "Write type-stable functions and inspect them with @code_warntype; fix instability with zero(T), oftype and function barriers."
sources: ["https://docs.julialang.org/en/v1/manual/performance-tips/", "https://docs.julialang.org/en/v1/stdlib/InteractiveUtils/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Type stability and inference
- A function is type-stable when its return type depends only on argument types.
- Common causes of instability: `x = 0` then `x += 1.5`, containers with abstract element type, untyped non-const global variables, returning different types in branches.
- `@code_warntype f(x)` shows inferred types so `Union` and `Any` results stand out.
- Fix with `zero(T)`, `oftype`, function barriers (move the hot loop into a separate function), concrete fields.
Verify: `@inferred f(x)` in tests passes.

## Checked

2026-11-03. Confirmed against: Performance Tips (type-stable definitions, `zero`/`oftype`, function barriers, abstract containers, globals) and InteractiveUtils (`@code_warntype`). Removed: JET.jl `@report_opt`/`@report_call` (not found on the pages read) and the red/yellow colour claim; the description no longer mentions JET.
Method: documentation only; no commands were run.
