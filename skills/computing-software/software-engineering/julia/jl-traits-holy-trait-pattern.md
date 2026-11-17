---
id: computing-software.software-engineering.julia.jl-traits-holy-trait-pattern
name: jl-traits-holy-trait-pattern
category: computing-software
field: software-engineering
product: julia
tags: [julia, traits-holy-trait-pattern]
level: advanced
status: docs-checked
description: "Implement trait-based dispatch in Julia with the Holy traits pattern: a trait function plus dispatch on trait types."
sources: ["https://docs.julialang.org/en/v1/manual/methods/", "https://docs.julialang.org/en/v1/stdlib/InteractiveUtils/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Holy traits
- Define `struct IsCallable end; struct NotCallable end`, a trait function `callability(::Type{T})`, and dispatch `f(x) = f(callability(typeof(x)), x)`.
- Lets unrelated types share behaviour without a common abstract supertype; the manual says the trait function is pure and has no performance impact.
- Prefer abstract types when a single hierarchy fits; interfaces are informal (document required methods).
Verify: `@code_warntype f(x)` shows no `Any`.

## Checked

2026-11-03. Confirmed against: Manual Methods (the Holy-trait pattern, trait functions, no performance impact) and InteractiveUtils (`@code_warntype`). Removed: the claim that the trait lookup is constant-folded (the manual says only that there is no performance impact) and the Val-types mention in the description.
Method: documentation only; no commands were run.
