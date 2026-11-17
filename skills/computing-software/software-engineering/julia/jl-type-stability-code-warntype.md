---
id: computing-software.software-engineering.julia.jl-type-stability-code-warntype
name: jl-type-stability-code-warntype
category: computing-software
field: software-engineering
product: julia
tags: [julia, type-stability-code-warntype]
level: advanced
status: docs-checked
description: "Diagnose type instability in Julia using @code_warntype and @inferred, avoid untyped globals and measure with @time and @allocated."
sources: ["https://docs.julialang.org/en/v1/manual/performance-tips/", "https://docs.julialang.org/en/v1/stdlib/InteractiveUtils/", "https://docs.julialang.org/en/v1/stdlib/Test/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Type stability
- A function is type stable if its return type depends only on argument types. Look for `Any`/`Union` in `@code_warntype f(x)`.
- Avoid untyped non-const globals in hot code; pass arguments or use `const`.
- Fix `x = 0` then `x += 1.5` by `x = 0.0`, use `zero(T)`, function barriers.
- Preallocate, use `@views`, `@inbounds` (carefully), `eachindex`; measure with `@time` (run twice) and `@allocated`.
Verify: `@allocated f(x)` is 0 after the fix, called after a warm-up call.

## Checked

2026-11-03. Confirmed against: Performance Tips (type stability, globals, `zero`, function barriers, preallocation, `@views`, `@inbounds`, `@time`, `@allocated`), InteractiveUtils (`@code_warntype`) and stdlib Test (`@inferred`). Removed: Cthulhu and the BenchmarkTools `@btime f($x)` interpolation claim (the page only names BenchmarkTools as a package); the description no longer mentions Cthulhu.
Method: documentation only; no commands were run.
