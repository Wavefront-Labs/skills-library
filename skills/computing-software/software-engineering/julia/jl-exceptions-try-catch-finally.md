---
id: computing-software.software-engineering.julia.jl-exceptions-try-catch-finally
name: jl-exceptions-try-catch-finally
category: computing-software
field: software-engineering
product: julia
tags: [julia, exceptions-try-catch-finally]
level: practitioner
status: docs-checked
description: "Throw and catch Julia exceptions, define custom Exception subtypes, rethrow with stack traces."
sources: ["https://docs.julialang.org/en/v1/manual/control-flow/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Exceptions
- `throw(ArgumentError("x"))`, `error("msg")`, `@assert cond "msg"`.
- `try ... catch e; if e isa KeyError ... else rethrow() end; finally ... end`; `catch_backtrace()` with `rethrow`.
- Custom: `struct MyErr <: Exception; msg::String; end` plus `Base.showerror`.
Verify: `finally` runs on success and on throw.

## Checked

2026-11-02. Confirmed against: Manual Control Flow page (exceptions, try/catch/finally, rethrow, catch_backtrace) and Base docs (showerror). Removed: the cost claim about try blocks and throwing.
Method: documentation only; no commands were run.
