---
id: computing-software.web-development.litestar.litestar-sync-vs-async
name: litestar-sync-vs-async
category: computing-software
field: web-development
product: litestar
tags: [litestar, sync-vs-async, sync-to-thread, thread-pool, blocking, async, io-bound]
level: practitioner
status: docs-checked
description: "Decide whether a Litestar handler should be async, plain sync, or sync_to_thread=True, and avoid blocking the event loop."
sources: [https://docs.litestar.dev/latest/topics/sync-vs-async.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Litestar sync vs. async handlers

Goal: pick the right execution mode for each callable.

## Method

Litestar supports three modes: async callables run directly, sync callables run directly, sync callables run in a thread pool.

| Situation | Use |
|---|---|
| Does real async work (awaits other coroutines, async iteration) and no blocking calls | `async def` |
| Non-blocking, not I/O heavy | plain `def` with `sync_to_thread=False` (smallest overhead) |
| Computationally intense or I/O-bound and cannot be replaced by an async equivalent | plain `def` with `sync_to_thread=True` |

- Async is not inherently non-blocking: an async function that never awaits and does heavy computation blocks the thread for its whole runtime. Code between awaits blocks too.
- I/O-bound work (file system, network) suits async; CPU-bound work does not benefit.
- A CPU-bound loop can be made cooperative by awaiting `asyncio.sleep(0)` at the start of each iteration; useful for long tasks whose individual steps are short.
- Do not default to async: it has small overhead, and a sync function doing non-blocking work outperforms an async one. Do not default to threads either: a thread pool has very high overhead.

## Gotchas

- A thread pool makes a CPU-bound function non-blocking but does not speed it up. For regular heavy computation, offload to another process, e.g. `anyio.to_process.run_sync`.
- Litestar warns when a sync callable is used where it might block the event loop. Setting `sync_to_thread=False` tells Litestar it is non-blocking; the warning forces a deliberate choice.
- Disable the warning globally with the environment variable `LITESTAR_WARN_IMPLICIT_SYNC_TO_THREAD=0`.

## Verify

A sync callable without `sync_to_thread` triggers the warning; `sync_to_thread=False` marks it non-blocking, and `LITESTAR_WARN_IMPLICIT_SYNC_TO_THREAD=0` disables the warning globally.

## Checked

2026-11-07. Read the full cited page(s) (topics/sync-vs-async.html) and the example files they include, and confirmed the claims in this skill against that text. Rewrote the verify step to the behaviour the page states (warning, sync_to_thread=False, LITESTAR_WARN_IMPLICIT_SYNC_TO_THREAD=0).

Method: documentation only; no commands were run.
