---
id: computing-software.software-engineering.julia.jl-threads-tasks
name: jl-threads-tasks
category: computing-software
field: software-engineering
product: julia
tags: [julia, jl-concurrency, threads-tasks]
level: advanced
status: docs-checked
description: "Start Julia with threads, write race-free parallel loops and use Tasks, Channels and locks."
sources: ["https://docs.julialang.org/en/v1/manual/multi-threading/", "https://docs.julialang.org/en/v1/manual/asynchronous-programming/", "https://docs.julialang.org/en/v1/manual/command-line-interface/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Threads.@threads, tasks and channels
- Start with `julia -t auto` or `JULIA_NUM_THREADS`; `Threads.nthreads()` checks.
- `Threads.@threads for i in 1:n ... end` splits iterations; writing to the same variable is a data race: use per-thread buffers, `Threads.Atomic`, or `ReentrantLock`.
- `Threads.@spawn f()` returns a `Task`; `fetch(t)`; `Channel{T}(n)` with `put!`/`take!`; `@sync` waits for children.
- Task-local state: avoid `threadid()`-indexed buffers, use task-local or chunked work (tasks can migrate between threads, so `threadid()` is not constant within a task).
- `Base.@lock lk begin ... end`.
Verify: run under `-t 1` and `-t 8` and compare results.

## Checked

2026-11-02. Confirmed against: Manual Multi-Threading page (-t/--threads, @threads, @spawn, data races, threadid caveat) and Asynchronous Programming. Removed: the Julia 1.7 version gate.
Method: documentation only; no commands were run.
