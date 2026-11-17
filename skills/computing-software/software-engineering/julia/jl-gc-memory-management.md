---
id: computing-software.software-engineering.julia.jl-gc-memory-management
name: jl-gc-memory-management
category: computing-software
field: software-engineering
product: julia
tags: [julia, jl-memory-gc, gc-memory-management]
level: advanced
status: docs-checked
description: "Diagnose GC time and memory growth with @time, GC.gc, Base.summarysize and avoid finalizer pitfalls."
sources: ["https://docs.julialang.org/en/v1/manual/memory-management/", "https://docs.julialang.org/en/v1/manual/calling-c-and-fortran-code/", "https://docs.julialang.org/en/v1/manual/performance-tips/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GC pressure, finalizers and memory use
- `@time` reports GC percentage; high values point at allocation in loops. `Base.summarysize(x)` gives object size; `varinfo()` lists globals.
- `GC.gc()` forces a collection; `GC.@preserve x ccall(...)` keeps data alive for C calls.
- Finalizers (`finalizer(f, obj)`) run at unpredictable times; prefer explicit `close` and `do` blocks.
- `--heap-size-hint=4G` (or a percentage such as `50%`) tells the GC to collect more aggressively near that limit, which helps in containers.
Verify: `@allocated` before and after the fix.

## Checked

2026-11-02. Confirmed against: Manual Memory Management (--heap-size-hint), Calling C (GC.@preserve) and Performance Tips; Base docs for summarysize and finalizer. Removed: the Julia 1.9 version gate on --heap-size-hint.
Method: documentation only; no commands were run.
