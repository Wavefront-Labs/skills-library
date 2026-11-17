---
id: computing-software.software-engineering.julia.jl-logging-debugging
name: jl-logging-debugging
category: computing-software
field: software-engineering
product: julia
tags: [julia, jl-logging, logging-debugging]
level: practitioner
status: docs-checked
description: "Use @info/@warn/@debug with JULIA_DEBUG filtering, with_logger, @show, stack traces and InteractiveUtils helpers."
sources: ["https://docs.julialang.org/en/v1/stdlib/Logging/", "https://docs.julialang.org/en/v1/stdlib/InteractiveUtils/", "https://docs.julialang.org/en/v1/base/base/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Logging macros and inspection tools
- `@info "msg" x = 1`, `@warn`, `@error`, `@debug`; enable debug output with `ENV["JULIA_DEBUG"] = "MyModule"` (module names, comma-separated).
- `with_logger(ConsoleLogger(stderr, Logging.Debug))`.
- `@show`; `@edit`, `@less`, `varinfo`, `apropos`, `methodswith`; `stacktrace()` and `Base.catch_backtrace()`.
Verify: `JULIA_DEBUG=MyModule julia script.jl` prints debug lines.

## Checked

2026-11-03. Confirmed against: stdlib Logging (macros, `JULIA_DEBUG`, `with_logger`, `ConsoleLogger`), stdlib InteractiveUtils (`@edit`, `@less`, `varinfo`, `apropos`, `methodswith`) and Base (`@show`, `stacktrace`, `catch_backtrace`). Removed: Debugger.jl, Infiltrator.jl and LoggingExtras.jl (third-party, not on the pages read), and `JULIA_DEBUG=all` (not confirmed); the description and heading no longer mention the packages.
Method: documentation only; no commands were run.
