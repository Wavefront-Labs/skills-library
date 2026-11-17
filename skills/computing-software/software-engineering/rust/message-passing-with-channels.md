---
id: computing-software.software-engineering.rust.message-passing-with-channels
name: message-passing-with-channels
category: computing-software
field: software-engineering
product: rust
tags: [rust, rust-concurrency, mpsc, crossbeam, sync-channel, bounded-channel, tokio-mpsc, worker-pool, backpressure, flume]
level: practitioner
status: verified
description: "Pass messages between Rust threads and tasks: std mpsc vs crossbeam vs tokio channels, bounded backpressure, shutdown by dropping senders, and worker pools."
sources: ["https://doc.rust-lang.org/book/ch16-02-message-passing.html", "https://doc.rust-lang.org/std/sync/mpsc/index.html", "https://docs.rs/crossbeam-channel/latest/crossbeam_channel/", "https://docs.rs/tokio/latest/tokio/sync/index.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Message passing with channels

**Goal:** structure concurrent Rust as threads/tasks that own their data and talk via
channels, with bounded queues and clean shutdown.

## Which channel
| Context | Channel |
|---|---|
| OS threads, simple | `std::sync::mpsc::sync_channel(n)` (bounded) / `channel()` (unbounded) |
| OS threads, multi-consumer or `select!` | `crossbeam_channel::bounded(n)` (std mpsc is now crossbeam-based but still single-consumer API) |
| async tasks | `tokio::sync::mpsc` (bounded), `oneshot` (one reply), `broadcast` (fan-out to all), `watch` (latest value) |
| Mixing sync and async | `flume` or tokio `blocking_send`/`blocking_recv` |

## Pipeline with backpressure
```rust
let (tx, rx) = crossbeam_channel::bounded::<Job>(100);    // producers block when full
let workers: Vec<_> = (0..num_cpus).map(|_| {
    let rx = rx.clone();
    thread::spawn(move || for job in rx { handle(job) })  // loop ends when all senders dropped
}).collect();
for job in jobs { tx.send(job)?; }
drop(tx);                                                  // signal "no more work"
for w in workers { w.join().unwrap(); }
```
Unbounded channels hide overload until memory runs out; bound them.

## Shutdown semantics
- Receivers see the end (`recv()` returns Err / iterator ends) only when ALL senders are
  dropped. A forgotten clone of `tx` (e.g. kept in main) means workers never exit.
- `send` fails when all receivers are gone; treat as "shutting down", not a panic.
- Async: combine `rx.recv()` with a `CancellationToken` in `tokio::select!`.

## Request/response
Send a `oneshot::Sender` inside the message (actor pattern):
```rust
enum Cmd { Get { key: String, reply: oneshot::Sender<Option<String>> } }
```
The actor task owns the state; no locks needed.

## Select over several channels
`crossbeam_channel::select!` (threads) or `tokio::select!` (async). Note tokio::select!
cancels the losing branches' futures; `recv()` is cancel-safe, many other futures are not.

## Verify
- [ ] Every channel is bounded or has a written justification.
- [ ] Shutdown test: dropping the producer ends all workers within a timeout.

## Checked
- rustc/cargo 1.99.1 (stable, Windows msvc, edition 2024), tokio 1.54.0, futures 0.3.34, rayon 1.12.0, thiserror 2.0.21, anyhow 1.0.104, color-eyre 0.6.5, crossbeam-channel 0.5, tokio 1.54.0.
- Ran the bounded pipeline: 4 workers over `crossbeam_channel::bounded(100)` with `for job in rx`, 1000 jobs, `drop(tx)` then join: the total 999000 matched the expected sum. A worker whose sender was still alive did not exit within 200 ms; after `drop(tx)` it exited. `send` after the receiver was dropped returned `Err`; `sync_channel(1)` `try_send` on a full queue returned `Err`; `crossbeam_channel::select!` received `Ok(7)`; `blocking_send` from an OS thread delivered to a tokio `recv()`.
- std mpsc is based on crossbeam-channel: Rust 1.67.0 release notes "Merge `crossbeam-channel` into `std::sync::mpsc`" (RELEASES.md). `flume` exists on crates.io.
