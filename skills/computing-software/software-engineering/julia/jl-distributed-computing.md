---
id: computing-software.software-engineering.julia.jl-distributed-computing
name: jl-distributed-computing
category: computing-software
field: software-engineering
product: julia
tags: [julia, jl-concurrency, distributed-computing]
level: advanced
status: docs-checked
description: "Add worker processes, use pmap and @distributed, and load code on workers with @everywhere."
sources: ["https://docs.julialang.org/en/v1/stdlib/Distributed/", "https://docs.julialang.org/en/v1/manual/distributed-computing/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Distributed.jl and process-based parallelism
- `using Distributed; addprocs(4)`; `@everywhere include("f.jl")` or `@everywhere using <modulename>` to define code on all workers.
- `pmap(f, xs)` for expensive tasks; `@distributed (+) for i in 1:n ... end` for reductions.
- `remotecall_fetch`, `RemoteChannel`.
- Workers need the same project: `addprocs(4; exeflags = "--project")`; workers do not run `startup.jl`.
Verify: results equal the serial run.

## Checked

2026-11-03. Confirmed against: stdlib Distributed and Manual Distributed Computing (`addprocs`, `exeflags`, `@everywhere`, `pmap`, `@distributed`, `remotecall_fetch`, `RemoteChannel`, startup.jl not run on workers). Removed: `@everywhere using Pkg1` (replaced by the docs placeholder `<modulename>`), the SharedArrays claim and its description mention (not confirmed on the pages read).
Method: documentation only; no commands were run.
