---
id: computing-software.software-engineering.concurrency.event-loops-and-async-io
name: event-loops-and-async-io
category: computing-software
field: software-engineering
product: concurrency
tags: [concurrency, concurrency-models, async-io, event-loop, non-blocking-io, epoll, io-uring]
level: practitioner
status: gated
description: "Choose between event-loop async I/O and threads: how epoll/kqueue/IOCP/io_uring loops work, C10K trade-offs, blocking-the-loop bugs, offloading CPU work and diagnosis."
sources:
  - https://nodejs.org/en/learn/asynchronous-work/event-loop-timers-and-nexttick
  - https://docs.python.org/3/library/asyncio-dev.html
  - https://man7.org/linux/man-pages/man7/epoll.7.html
  - https://unixism.net/loti/what_is_io_uring.html
  - https://tokio.rs/tokio/tutorial
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Event loops and async I/O vs threads

## How an event loop works
One (or a few) threads run a loop: ask the OS which sockets are ready (`epoll` on Linux, `kqueue` on BSD/macOS, IOCP on Windows, or submit/complete queues with `io_uring`), run the callbacks/coroutines that can make progress, repeat. Thousands of connections cost a small state object each instead of a thread stack (default 1-8 MB virtual per OS thread (gated: unconfirmed, source is paywalled or blocked)).
Runtimes: Node.js (libuv), Python asyncio/uvloop, Netty/Vert.x, Rust Tokio, .NET async (IOCP/epoll under the thread pool), nginx.

## Threads (or virtual threads) instead
- Thread-per-request is simpler: sequential code, normal stack traces, blocking libraries work.
- Costs: memory per thread and context switches limit you to thousands, not hundreds of thousands, of concurrent connections.
- **Virtual threads/green threads** (Java 21 Loom, Go goroutines, Erlang processes) give thread-style code with event-loop-like scalability: the runtime parks them on blocking I/O. Often the best of both for new services in those languages.

## Decision guide
| Workload | Choice |
|---|---|
| Many concurrent, mostly idle connections (websockets, proxies, chat) | event loop or virtual threads |
| I/O-bound APIs with moderate concurrency | either; pick what the ecosystem does well |
| CPU-bound work | threads/processes sized to cores; never on the loop |
| Heavy use of blocking libraries (JDBC, legacy SDKs) | threads/virtual threads, or offload |

## The cardinal rule: never block the loop
One blocking call (sync file read, `time.sleep`, a CPU-heavy JSON parse, a sync DB driver, `requests.get` inside asyncio) stalls every connection on that loop.
- Offload: Node `worker_threads`; Python `await asyncio.to_thread(fn)` or `loop.run_in_executor` (process pool for CPU); Tokio `spawn_blocking`; Vert.x `executeBlocking`.
- Use async-native drivers (asyncpg, aiohttp/httpx async, R2DBC, async Redis clients).
- Function colouring: async functions can only be awaited from async code; keep sync/async boundaries at the edges.

## Diagnosing a blocked loop
- Node: `perf_hooks.monitorEventLoopDelay()` (run on Node 20: a 300 ms busy loop showed max delay 315 ms), `--cpu-prof`, clinic.js doctor; event loop lag metric.
- Python: `asyncio.run(main(), debug=True)` / `PYTHONASYNCIODEBUG=1` logs callbacks slower than `loop.slow_callback_duration` (default 100 ms; run on Python 3.14: a `time.sleep(0.3)` in a coroutine logged `took 0.302 seconds`); py-spy dump shows what the loop thread is doing.
- Tokio: `tokio-console` shows tasks that do not yield; Netty: `BlockHound` fails tests on blocking calls in event-loop threads (both projects exist on GitHub; behaviour not run here (gated: unconfirmed, source is paywalled or blocked)).

## io_uring
Linux 5.1+ submission/completion rings for truly asynchronous file and network I/O with batched syscalls; used by Tokio-uring, glommio, liburing, Netty's io_uring transport. Some container runtimes disable it via seccomp for security reasons - check before relying on it.

## Verify
- [ ] Event loop lag metric exported and alerted (for example p99 > 50 ms).
- [ ] Test-time detector (BlockHound, asyncio debug mode) runs in CI.
