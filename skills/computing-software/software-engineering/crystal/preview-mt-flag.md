---
id: computing-software.software-engineering.crystal.preview-mt-flag
name: preview-mt-flag
category: computing-software
field: software-engineering
product: crystal
tags: [preview-mt-flag, multithreading, preview-mt, parallelism, threads, execution-context, -dpreview_mt, crystal]
level: advanced
status: docs-checked
description: "Crystal parallelism: execution contexts (concurrent, parallel, isolated), resizing the default context, and the legacy preview_mt, execution_context and without_mt flags."
sources:
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/guides/parallelism.md
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/syntax_and_semantics/compile_time_flags.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Parallel execution: execution contexts and the preview_mt flag

Goal: run fibers on several OS threads.

- A Crystal program is concurrent by default (one fiber at a time); parallelism is opt-in by resizing the default execution context or starting additional contexts.
- Three built-in context types: `Fiber::ExecutionContext::Concurrent` (fibers run concurrently, never in parallel with each other), `Parallel` (fibers run concurrently and in parallel, auto-scaling up to a maximum) and `Isolated` (one fiber owns a thread).
- `ctx = Fiber::ExecutionContext::Parallel.new("MULTI", maximum: 4)` then `ctx.spawn { ... }` runs fibers on up to four schedulers.
- The default context is a parallel context with parallelism 1; enable multithreading with `Fiber::ExecutionContext.default.resize(4)` (or a thread count from a CLI argument or `System.cpu_count`).
- Flags (compile-time): `preview_mt` reverts to the legacy multithreading runtime (introduced 0.28, deprecated since 1.21); `execution_context` enabled execution contexts (introduced 1.16, obsolete since 1.21); `without_mt` reverts to the legacy single-threaded runtime (introduced 1.21). Check your Crystal version before using any of them.
- Shared mutable state needs synchronisation once fibers run in parallel; prefer communication such as `Channel`.

Gotchas:
- Avoid thread locals (`@[ThreadLocal]`); the guide advises against them.
- A fiber doing CPU-heavy work in a concurrent context blocks other fibers in that context.

Verify: resize the default context and observe fibers running at the same time.

## Checked

2026-11-03. Confirmed against the Crystal book Parallelism guide (context types, `Parallel.new("MULTI", maximum: 4)`, default context and `resize`, thread-local and shared-variable advice) and the compile-time flags page (`preview_mt`, `execution_context`, `without_mt` and their versions).
Fixed: the skill presented `-Dpreview_mt` as the way to enable threads; the docs now describe it as the legacy runtime, deprecated since 1.21. Removed: `CRYSTAL_WORKERS`, `spawn(same_thread: true)` and the `Thread.current.object_id` verification.
Method: documentation only; no commands were run.
