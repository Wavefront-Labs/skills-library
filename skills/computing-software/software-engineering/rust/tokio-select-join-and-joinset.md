---
id: computing-software.software-engineering.rust.tokio-select-join-and-joinset
name: tokio-select-join-and-joinset
category: computing-software
field: software-engineering
product: rust
tags: [rust, tokio-select, joinset, tokio-join, try-join, async, cancellation-safety, structured-concurrency, timeouts, rust-cancel-safety, rust-graceful-shutdown]
level: advanced
status: verified
description: "Combine async work in tokio: join!/try_join! for fixed concurrency, select! for races and shutdown with cancellation safety, JoinSet for dynamic task groups, and timeout."
sources: ["https://docs.rs/tokio/latest/tokio/macro.select.html", "https://docs.rs/tokio/latest/tokio/macro.join.html", "https://docs.rs/tokio/latest/tokio/task/struct.JoinSet.html", "https://tokio.rs/tokio/tutorial/select"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# tokio select!, join! and JoinSet

**Goal:** run async operations concurrently, race them, and supervise groups of tasks without
leaks or lost work.

## join! / try_join!: a fixed set, same task
```rust
let (user, orders) = tokio::join!(fetch_user(id), fetch_orders(id));
let (user, orders) = tokio::try_join!(fetch_user(id), fetch_orders(id))?; // first Err cancels the rest
```
Runs the futures concurrently on the **current task** (no spawn, no `'static` or `Send` needed),
but not in parallel across threads. For a dynamic number of futures: `futures::future::join_all` or
`try_join_all` (for large N prefer `FuturesUnordered` or JoinSet).

## select!: first to complete wins
```rust
loop {
    tokio::select! {
        biased;                                       // poll in order: shutdown first
        _ = shutdown.cancelled() => break,
        Some(msg) = rx.recv() => handle(msg).await,   // pattern: branch disabled if it does not match
        _ = ticker.tick() => flush().await,
        else => break,                                // all branches disabled
    }
}
```
- When one branch completes, **the other futures are dropped** (cancelled). This is only safe for
  cancellation-safe futures: `mpsc::Receiver::recv`, `tick`, `sleep`, `TcpListener::accept`,
  `CancellationToken::cancelled` are; `AsyncReadExt::read_exact`, `read_to_end`, and arbitrary
  `async fn`s holding partial state are not.
- To keep a non-cancel-safe operation alive across loop iterations, create it once and select on a
  pinned reference:
```rust
let op = do_long_thing();
tokio::pin!(op);
loop { tokio::select! { res = &mut op => break res, _ = interval.tick() => report_progress() } }
```
- Without `biased;` branches are polled in random order for fairness.
- Timeouts: `tokio::time::timeout(Duration::from_secs(5), fut).await` returns `Err(Elapsed)`;
  simpler than select with sleep.

## JoinSet: dynamic group of spawned tasks
```rust
let mut set = tokio::task::JoinSet::new();
for url in urls {
    let client = client.clone();
    set.spawn(async move { client.get(url).send().await });
}
while let Some(res) = set.join_next().await {
    match res {
        Ok(Ok(resp)) => handle(resp),
        Ok(Err(e)) => tracing::warn!(%e, "request failed"),
        Err(join_err) if join_err.is_panic() => std::panic::resume_unwind(join_err.into_panic()),
        Err(_) => {} // cancelled
    }
}
```
- Dropping a JoinSet **aborts** all its tasks: structured cleanup by scope. `set.abort_all()`,
  `set.shutdown().await` explicitly.
- Bound concurrency: spawn up to N, then `join_next()` before spawning more; or hold a
  `Semaphore` permit inside each task.
- `JoinHandle` from `tokio::spawn` detaches on drop (task keeps running); call `.abort()` or keep it
  in a JoinSet.

## Graceful shutdown pattern
`tokio_util::sync::CancellationToken` passed to tasks (`child_token()`), `select!` on
`token.cancelled()` in each loop, then `tracker.close(); tracker.wait().await` (`tokio_util::task::TaskTracker`,
feature `rt` of tokio-util) or drain the JoinSet with a timeout. `wait()` does not resolve until the tracker is
closed AND empty: without `close()` it hangs even when every task has finished (confirmed with a timeout).

## Verify
- [ ] Every future inside a `select!` loop is cancellation safe or pinned outside the loop.
- [ ] No unbounded `tokio::spawn` fan-out; JoinSet or semaphore limits concurrency.
- [ ] Task panics are surfaced (not silently dropped JoinHandles).

## Checked
- rustc/cargo 1.99.1 (stable, Windows msvc, edition 2024), tokio 1.54.0, futures 0.3.34, rayon 1.12.0, thiserror 2.0.21, anyhow 1.0.104, color-eyre 0.6.5, tokio-util 0.7 (feature `rt` for TaskTracker).
- Ran: `join!` of two 10 ms futures (both returned 1); `try_join!(b(), c())` returned `Err("b failed")` at 20 ms and the 200 ms `c` never finished (its print did not appear); a `select!` loop with `biased;`, a pattern branch `Some(msg) = rx.recv()` (printed `msg 1`, then the branch was disabled after the channel closed), `ticker.tick()` and a `CancellationToken` cancel (printed `shutdown`); the losing `select!` future was dropped (`loser dropped` printed); the `tokio::pin!(op)` + `&mut op` pattern completed with 42 while the interval fired 3 times; `timeout` returned `Elapsed`; dropping a JoinSet dropped its task (`joinset task dropped`); `JoinSet::shutdown().await` left `len() == 0`.
- TaskTracker with `child_token()` tasks: all three stopped; `tracker.wait()` timed out without `close()`, and returned after `close()` (the original text omitted `close()`, corrected).
- tokio source docs: `read_exact` "not cancel safe", `read` cancel safe (async_read_ext.rs). `tracing::warn!(%e, ...)` is only a call shape (tracing compiled in another snippet).
