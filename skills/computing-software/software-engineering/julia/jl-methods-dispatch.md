---
id: computing-software.software-engineering.julia.jl-methods-dispatch
name: jl-methods-dispatch
category: computing-software
field: software-engineering
product: julia
tags: [julia, jl-multiple-dispatch, methods-dispatch]
level: practitioner
status: docs-checked
description: "Define methods on argument types, avoid method ambiguities and extend Base functions properly."
sources: ["https://docs.julialang.org/en/v1/manual/methods/", "https://docs.julialang.org/en/v1/manual/style-guide/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Writing methods and resolving ambiguity
- Dispatch uses all arguments' runtime types; the most specific applicable method wins.
- Extend functions with `import Base: show` or `Base.show(io::IO, x::T) = ...`; defining `show` in your own module name creates a new unrelated function.
- Ambiguity errors (`MethodError: ... is ambiguous`) are fixed by adding the intersecting method.
- Do not over-constrain types: annotate for dispatch, not performance; `f(x::Number)` rather than `f(x::Float64)` unless needed.
- Inspect with `methods(f)` and `@which f(1, 2)`.
Verify: `Test.detect_ambiguities(MyModule)`.

## Checked

2026-11-02. Confirmed against: Manual Methods and Style Guide pages (dispatch, ambiguities, extending Base functions, avoiding over-constrained types); Test docs for detect_ambiguities. Removed: nothing.
Method: documentation only; no commands were run.
