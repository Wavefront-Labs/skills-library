---
id: computing-software.software-engineering.rust.crossbeam-and-parking-lot-primitives
name: crossbeam-and-parking-lot-primitives
category: computing-software
field: software-engineering
product: rust
tags: [rust, rust-concurrency, rust-crossbeam, crossbeam, parking-lot, channels]
level: practitioner
status: docs-checked
description: "Choose crossbeam channels, scoped utilities and parking_lot locks over std equivalents when you need select, bounded MPMC queues or lighter mutexes."
sources:
  - https://docs.rs/crossbeam/
  - https://docs.rs/parking_lot/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# crossbeam and parking_lot

**Goal:** know what these crates add and when std is enough.

**crossbeam-channel**: documented as an alternative to `std::sync::mpsc` with more features and better performance. Multi-producer multi-consumer channels (senders and receivers can be cloned), `select!`, `bounded`/`unbounded`, and `after`/`tick` timer channels.

```rust
use crossbeam_channel::{bounded, select};
let (tx, rx) = bounded::<Job>(64);                 // back-pressure
for _ in 0..4 {
    let rx = rx.clone();                           // MPMC: clone receivers
    std::thread::spawn(move || for job in rx { job.run() });
}
select! {
    recv(rx) -> msg => handle(msg),
    default(Duration::from_millis(100)) => tick(),
}
```

**Other crossbeam parts**: `CachePadded` (pad and align a value to a cache line), `Backoff` (exponential backoff in spin loops), `WaitGroup`, `scope` (threads that borrow stack variables), `AtomicCell`, `ArrayQueue` (bounded MPMC) and `SegQueue` (unbounded MPMC), work-stealing `deque`, `epoch` memory reclamation, `ShardedLock`.

**parking_lot**: compact implementations of `Mutex`, `FairMutex`, `ReentrantMutex`, `RwLock` (with upgradable read guards), `RecursiveRwLock`, `Condvar` and `Once`; re-exports `lock_api`; an experimental `deadlock` module. Benchmark against `std::sync` before switching.

## Gotchas
- When all senders or all receivers are dropped the channel is disconnected; the receiver iterator ends once the channel is empty and disconnected. A forgotten clone of `tx` therefore keeps `for job in rx` workers waiting.
- A `select!` operation counts as ready even when it only returns an error because the channel is disconnected; when several are ready, one is chosen at random.
- `unbounded` channels hold any number of messages, so overload shows up as memory growth; prefer `bounded` for back-pressure.
- parking_lot primitives must not be used internally by a global allocator (their contended paths may allocate, risking recursion or deadlock).

## Verify
Run workers with a bounded queue, confirm all jobs are processed, and confirm threads exit after the last `tx` is dropped.

## Checked
2026-11-09. Confirmed on docs.rs crossbeam (component list), crossbeam-channel (bounded/unbounded, cloning, disconnection, select!, after/tick; page read in part) and parking_lot (primitive list, lock_api, deadlock module, global allocator warning). Removed: Rust 1.62 and 1.67 std changes, "no poisoning" and size claims, `try_lock_for`, `deadlock_detection` feature name, `loom` advice, and the `std::thread::scope` supersession claim, none of which those pages state.
Method: documentation only; no commands were run.
