---
id: computing-software.software-engineering.julia.jl-threads-tasks-channels
name: jl-threads-tasks-channels
category: computing-software
field: software-engineering
product: julia
tags: [julia, threads-tasks-channels]
level: advanced
status: docs-checked
description: "Run parallel Julia code with Threads.@threads, @spawn, Channel and ReentrantLock."
sources: ["https://docs.julialang.org/en/v1/manual/multi-threading/", "https://docs.julialang.org/en/v1/manual/asynchronous-programming/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Concurrency
- Start with `julia -t auto` (or `JULIA_NUM_THREADS`); `Threads.@threads for` splits loops, `Threads.@spawn` returns a Task, `fetch`/`wait`.
- Channels: `Channel{Int}(32)`, `put!`, `take!`, `close`; iterate with `for x in ch`.
- Protect shared data with `ReentrantLock` and `lock(l) do ... end`, `Threads.Atomic`; avoid racy `Dict` writes.
- Threads run in the `:default` or `:interactive` thread pool (Multi-Threading, threadpools).
Verify: sum in parallel with a lock gives the serial result.

## Checked

2026-11-02. Confirmed against: Manual Multi-Threading and Asynchronous Programming pages (threads, Channel, locks, atomics, thread pools). Removed: the 1.9 version gate.
Method: documentation only; no commands were run.
