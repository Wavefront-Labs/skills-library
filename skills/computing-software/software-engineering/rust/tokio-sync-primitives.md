---
id: computing-software.software-engineering.rust.tokio-sync-primitives
name: tokio-sync-primitives
category: computing-software
field: software-engineering
product: rust
tags: [rust, tokio-sync, tokio-mutex, semaphore, broadcast, watch-channel, oneshot, notify, async]
level: advanced
status: verified
description: "Choose tokio::sync primitives: std vs tokio Mutex, RwLock, Semaphore for concurrency limits, oneshot, mpsc, broadcast and watch channels, and Notify."
sources: ["https://docs.rs/tokio/latest/tokio/sync/index.html", "https://docs.rs/tokio/latest/tokio/sync/struct.Mutex.html#which-kind-of-mutex-should-you-use", "https://tokio.rs/tokio/tutorial/shared-state", "https://tokio.rs/tokio/tutorial/channels"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# tokio sync primitives

**Goal:** pick the right coordination tool for async code so tasks neither block worker threads
nor deadlock across `.await`.

## Which Mutex
- `std::sync::Mutex` (or `parking_lot`) is correct and faster when the lock is **never held across
  an `.await`**: lock, mutate, drop, all synchronously. Tokio's docs recommend this as the default.
- `tokio::sync::Mutex` when the guard must be held across `.await` (e.g. serialising access to a
  connection while awaiting I/O). Its `lock()` is async and fair (FIFO). Slower.
- Holding a std `MutexGuard` across `.await` makes the future `!Send` (compile error on spawn) -
  that error is protecting you; restructure with a block scope or switch type.
```rust
{ let mut m = state.lock().unwrap(); m.count += 1; }   // guard dropped before await
do_io().await;
```
- `tokio::sync::RwLock`: many readers or one writer, async, write-preferring (fair).

## Semaphore: limit concurrency
```rust
let sem = Arc::new(Semaphore::new(10));
for job in jobs {
    let permit = sem.clone().acquire_owned().await?;   // waits when 10 are in flight
    tokio::spawn(async move { run(job).await; drop(permit); });
}
```
Also the building block for connection limits and rate limiting; `close()` makes waiters error out
for shutdown.

## Channels
| Channel | Shape | Typical use |
|---|---|---|
| `oneshot` | 1 value, 1 sender, 1 receiver | request/response to an actor, task result |
| `mpsc` (bounded) | many senders, 1 receiver, backpressure | work queues, actor mailboxes |
| `mpsc::unbounded_channel` | no backpressure | only when producers are naturally bounded |
| `broadcast` | many to many, every receiver gets every value (Clone) | event fan-out, shutdown signals |
| `watch` | single latest value, receivers see changes | config reloads, state/health status |

Actor request/response:
```rust
enum Cmd { Get { key: String, reply: oneshot::Sender<Option<String>> } }
let (tx, rx) = oneshot::channel();
cmd_tx.send(Cmd::Get { key, reply: tx }).await?;
let value = rx.await?;
```
- Bounded `mpsc::channel(n)`: `send().await` waits when full (backpressure). `try_send` to shed load.
  The receiver gets `None` once all senders drop: the natural shutdown signal.
- `broadcast`: slow receivers get `RecvError::Lagged(n)` and skip messages; size the buffer and
  handle Lagged.
- `watch`: `rx.changed().await` then `rx.borrow_and_update()`; do not hold the borrow across await
  (it holds a read lock).

## Notify
`Notify::notify_one()` / `notify_waiters()` with `notified().await` - a low-level wakeup without
data, used to build other primitives. A `notify_one` with no waiter stores a single permit (two calls still store one) that
the next `notified().await` consumes immediately; `notify_waiters` stores nothing.

## Gotchas
- Never call `blocking_lock`/`blocking_recv` inside async context (panics); they are for sync code
  interacting with async.
- Lock ordering still matters with async mutexes; deadlocks are just harder to see (no thread blocked).
- `tokio::sync` primitives are runtime-agnostic and work in any executor.

## Verify
- [ ] No std MutexGuard lives across `.await` (clippy `await_holding_lock`).
- [ ] Channels are bounded unless there is a documented reason.
- [ ] broadcast receivers handle `Lagged`.

## Checked
- rustc/cargo 1.99.1 (stable, Windows msvc, edition 2024), tokio 1.54.0, futures 0.3.34, rayon 1.12.0, thiserror 2.0.21, anyhow 1.0.104, color-eyre 0.6.5.
- Ran: `notify_one()` before `notified().await` completed immediately; `notify_waiters()` with no waiter stored nothing (the later `notified()` timed out); two `notify_one()` calls then two `notified()` calls: the second timed out (one permit, not two). `broadcast::channel(2)` after 5 sends: first `recv()` returned `Err(Lagged(3))`, the next `Ok(3)`. `watch`: `changed().await` then `borrow_and_update()` returned 5. A `Semaphore::new(3)` with `acquire_owned` over 10 tasks peaked at 3 in flight; `close()` made `acquire()` return `Err`. The `oneshot` reply actor returned `Some("K")`. `try_send` on a full bounded mpsc returned `Err`. `blocking_lock()` inside a spawned async task panicked ("Cannot block the current thread from within a runtime"). Two `RwLock` read guards coexisted.
- tokio Mutex docs (docs.rs, fetched): "Contrary to popular belief, it is ok and often preferred to use the ordinary Mutex"; the tokio Mutex is "fair" and lock order is FIFO. RwLock docs say write-preferring. A std `MutexGuard` across `.await` in `tokio::spawn` is a compile error (see async-rust-with-tokio).
