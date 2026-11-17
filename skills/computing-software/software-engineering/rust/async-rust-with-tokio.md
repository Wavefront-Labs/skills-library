---
id: computing-software.software-engineering.rust.async-rust-with-tokio
name: async-rust-with-tokio
category: computing-software
field: software-engineering
product: rust
tags: [rust, tokio, async, await, cancellation-safety, select-macro, spawn-blocking, tokio-runtime, mutex, async-await, futures, join-set, rust-async, rust-spawn-blocking]
level: advanced
status: verified
description: "Write correct async Rust with tokio: never block the runtime, understand cancellation safety in select!, and when to use spawn_blocking vs a blocking Mutex."
sources: ["https://tokio.rs/tokio/tutorial", "https://docs.rs/tokio/latest/tokio/macro.select.html", "https://ryhl.io/blog/actors-with-tokio/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Async Rust with tokio — the runtime, blocking, and cancellation safety

**Goal:** write async code where a blocking call doesn't stall unrelated tasks, and
`select!`/dropped futures don't silently lose data.

## 1. Never block the runtime's worker threads
Tokio's default runtime multiplexes many tasks onto a small pool of worker threads.
Any call that blocks the OS thread (`std::thread::sleep`, synchronous file I/O,
`std::sync::Mutex` held across an `.await` — see below, a CPU-heavy computation)
starves every other task scheduled on that worker, not just the caller.
```rust
tokio::time::sleep(duration).await;                 // not std::thread::sleep
let result = tokio::task::spawn_blocking(|| cpu_or_blocking_work()).await?;
```
`spawn_blocking` moves the work to a separate blocking-thread pool, sized
independently from the async worker pool — use it for any synchronous library call
you can't avoid (a blocking DB driver, CPU-bound hashing/compression) rather than
calling it directly inside an async fn.

## 2. `std::sync::Mutex` across an `.await` point is a bug waiting to happen
```rust
let guard = std_mutex.lock().unwrap();
some_async_fn().await;   // guard still held across the await — BAD
```
Holding a `std::sync::Mutex` guard across an await point can deadlock the runtime
(the task yields while holding the lock; if another task on the same thread then calls
`lock()`, it blocks the thread and the holder can never run again). `tokio::spawn`
rejects such a future at compile time because `MutexGuard` is not `Send` ("future cannot
be sent between threads safely"), but the same code compiles with `LocalSet::spawn_local`
or `block_on` (a second local task's `try_lock` fails while the first one is parked). Use `tokio::sync::Mutex` for anything that
must be held across an `.await`, or restructure to drop the std guard before
awaiting.

## 3. `select!` and cancellation safety
```rust
tokio::select! {
    res = read_from_socket() => handle(res),
    _ = tokio::time::sleep(timeout) => handle_timeout(),
}
```
`select!` polls all branches and drops every future except the one that completed —
if a dropped future had already done partial, non-idempotent work (consumed bytes
from a buffer, sent half a message), that work is lost with no way to resume. A
future is "cancellation safe" only if dropping it mid-poll leaves no partial,
unrecoverable state. Many hand-written futures and even some library methods are
NOT cancellation safe by default (check the specific method's docs — e.g. some
`tokio::io` read methods explicitly document this). The common fix: own the
in-progress state outside the future (e.g. read into a persistent buffer field that
survives across `select!` iterations) rather than inside a one-shot future that gets
dropped.

## 4. Shared state: channels over shared mutable state where possible
The "actor" pattern (one task owns the state, others message it via an `mpsc`
channel) sidesteps most lock-ordering and cancellation-safety concerns that a shared
`Mutex<State>` accessed from many tasks accumulates:
```rust
let (tx, mut rx) = tokio::sync::mpsc::channel(32);
tokio::spawn(async move {
    let mut state = State::new();
    while let Some(cmd) = rx.recv().await { state.apply(cmd); }
});
```
Reach for `tokio::sync::Mutex`/`RwLock` directly when the actor pattern's extra
indirection isn't worth it (simple, short critical sections) — it's a trade-off, not
a universal rule.

## 5. Structured task management
A `tokio::spawn`'d task detaches — if you drop its `JoinHandle` without awaiting it,
you lose the ability to observe its panic or result, and it keeps running
independently (not cancelled automatically when the spawning scope ends, unlike
structured-concurrency models in other languages). Use `JoinSet` to spawn and track a
dynamic set of tasks together, awaiting/cancelling them as a group, rather than
scattering ungoverned `tokio::spawn` calls that nothing supervises.

## Gotchas
- `#[tokio::main]` creates a multi-threaded runtime by default — if your workload is
  genuinely single-threaded (no real parallelism needed, avoiding Send/Sync
  requirements on captured data), `#[tokio::main(flavor = "current_thread")]` is
  lighter and relaxes some trait bounds.
- `tokio::spawn` requires `Send + 'static` on EVERY runtime flavor, including `current_thread`
  (a task holding an `Rc` across an await fails with "`Rc<i32>` cannot be sent between threads
  safely"). `!Send` tasks need `tokio::task::LocalSet::spawn_local` (or awaiting them directly
  in `block_on`/main).
- `tokio-console` (a separate tool) visualizes task scheduling/blocking live — use it
  before guessing which task is starving others under load.

## Verify
- [ ] No synchronous blocking call (sleep, blocking I/O, CPU-heavy work) runs
      directly inside an async fn without `spawn_blocking`.
- [ ] No `std::sync::Mutex` guard is held across an `.await` point, confirmed by
      grep/review, not just "it compiled."
- [ ] Every `select!` branch was checked against its cancellation-safety
      documentation, or restructured to own persistent state outside the dropped future.
- [ ] Every `tokio::spawn`'d task's `JoinHandle` is tracked (via `JoinSet` or
      explicit await) so panics/results aren't silently lost.

Related: computing-software.software-engineering.rust.ownership-and-borrowing,
computing-software.software-engineering.python.asyncio-concurrency-patterns

## Checked
- rustc/cargo 1.99.1 (stable, Windows msvc, edition 2024), tokio 1.54.0, futures 0.3.34, rayon 1.12.0, thiserror 2.0.21, anyhow 1.0.104, color-eyre 0.6.5. `#[tokio::main]` default flavor printed `MultiThread`.
- Ran on a `current_thread` runtime: `std::thread::sleep(300ms)` made a task that asked for a 10 ms sleep finish after 312 ms, while the same wait inside `spawn_blocking` finished in 11 ms. The mpsc actor summed 1..4 to 10. A dropped `JoinHandle` task still ran to completion. JoinSet reported a panicking task as `Err` with `is_panic()` true.
- Compile-fail tests: a std `MutexGuard` held across `.await` inside `tokio::spawn` is rejected as not Send; an `Rc` captured in `tokio::spawn` is rejected even on `current_thread` (the original skill said it compiled there: wrong, corrected). `LocalSet::spawn_local` accepted both the `Rc` and the guard, and `try_lock` failed while the guard was parked.
- tokio `AsyncReadExt` docs mark `read_exact` as "not cancel safe" in the source (`async_read_ext.rs`), and `read` as cancel safe.
