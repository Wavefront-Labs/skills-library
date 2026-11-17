---
id: computing-software.software-engineering.julia.jl-do-blocks-try-finally
name: jl-do-blocks-try-finally
category: computing-software
field: software-engineering
product: julia
tags: [julia, do-blocks-try-finally]
level: practitioner
status: docs-checked
description: "Use do-blocks to pass anonymous functions, short-circuit &&/||, and begin/let scoping in Julia."
sources: ["https://docs.julialang.org/en/v1/manual/control-flow/", "https://docs.julialang.org/en/v1/manual/functions/", "https://docs.julialang.org/en/v1/manual/variables-and-scoping/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Control constructs
- `open("f") do io ... end` passes a closure and guarantees close; `map(xs) do x ... end`.
- `cond && action`, `cond || return`; ternary `a ? b : c` needs spaces.
- `let x = 1 ... end` creates a new scope; `begin ... end` does not.
- `for i in eachindex(A)`, `enumerate`, `zip`, `break`, `continue`; loop variables are local to the loop.
Verify: file handle is closed after the do block even on error.

## Checked

2026-11-02. Confirmed against: Manual Control Flow, Functions and Variables and Scoping pages. Removed: nothing.
Method: documentation only; no commands were run.
