---
id: computing-software.software-engineering.julia.jl-try-catch-exceptions
name: jl-try-catch-exceptions
category: computing-software
field: software-engineering
product: julia
tags: [julia, jl-errors, try-catch-exceptions]
level: practitioner
status: docs-checked
description: "Throw and catch typed exceptions, use finally for cleanup, define custom exceptions and capture backtraces."
sources: ["https://docs.julialang.org/en/v1/manual/control-flow/", "https://docs.julialang.org/en/v1/base/base/", "https://docs.julialang.org/en/v1/stdlib/Test/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# try, catch, finally and custom exceptions
- `try ... catch e; if e isa KeyError ... else rethrow() end; finally ... end`.
- Define `struct MyError <: Exception; msg::String; end` and `Base.showerror`.
- `error("msg")` throws `ErrorException`; `throw(ArgumentError("..."))`; `@assert` may be disabled at some optimisation levels, so use `throw` for argument checks.
- `catch_backtrace()` captures the stack inside `catch`; `showerror(stdout, e, catch_backtrace())`.
Verify: `@test_throws ArgumentError f(-1)` (Test stdlib).

## Checked

2026-11-03. Confirmed against: Manual Control Flow (try/catch/finally, `rethrow`, `throw`), Base (`error`, `ErrorException`, `Exception`, `showerror`, `catch_backtrace`, `@assert`) and stdlib Test (`@test_throws`). Removed: the claim that exceptions are slow relative to returns and the `Union{T,Nothing}` advice (no supporting text on the pages read); the description no longer says "avoid exceptions for control flow".
Method: documentation only; no commands were run.
