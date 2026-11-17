---
id: computing-software.software-engineering.julia.jl-scope-globals
name: jl-scope-globals
category: computing-software
field: software-engineering
product: julia
tags: [julia, jl-modules, scope-globals]
level: practitioner
status: docs-checked
description: "Avoid non-const globals in hot code and understand hard and soft scope rules."
sources: ["https://docs.julialang.org/en/v1/manual/variables-and-scoping/", "https://docs.julialang.org/en/v1/manual/performance-tips/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Global variables and soft scope
- Untyped non-const globals are type-unstable, so functions touching them are slow; pass values as arguments or declare `const x = 1`.
- Typed globals (`x::Int = 1`, Julia 1.8 or newer) fix the type.
- Functions create hard scope; `for`, `while` create soft scope: at the REPL assignment to a global inside them works (Julia 1.5 or newer), in files it creates a new local with a warning.
- `local` and `global` keywords disambiguate.
Verify: `@btime` with and without `$` interpolation of the global.

## Checked

2026-11-02. Confirmed against: Manual Variables and Scoping page (soft and hard scope, Julia 1.5 behaviour, typed globals since Julia 1.8) and Performance Tips. Removed: nothing.
Method: documentation only; no commands were run.
