---
id: computing-software.software-engineering.julia.jl-loops-iteration
name: jl-loops-iteration
category: computing-software
field: software-engineering
product: julia
tags: [julia, jl-control-flow, loops-iteration]
level: practitioner
status: docs-checked
description: "Use for, while, enumerate, zip, Iterators and implement iterate for custom types."
sources: ["https://docs.julialang.org/en/v1/manual/control-flow/", "https://docs.julialang.org/en/v1/manual/interfaces/", "https://docs.julialang.org/en/v1/manual/variables-and-scoping/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# for loops, iterators and the iteration protocol
- `for (i, x) in enumerate(xs)`, `zip(a, b)`, `Iterators.product`, `Iterators.partition`, `Iterators.take`.
- Loop variables are local to the loop; assigning to a global inside a loop at top level needs `global` in scripts (soft scope rules changed in Julia 1.5 for the REPL).
- Define `Base.iterate(it, state)` returning `nothing` at the end, plus `Base.length` or `Base.IteratorSize`.
- `break`, `continue`; `@goto` exists but is rarely needed.
Verify: `collect(it)` and `length` agree.

## Checked

2026-11-02. Confirmed against: Manual Control Flow, Interfaces (iteration) and Variables and Scoping pages. Removed: nothing.
Method: documentation only; no commands were run.
