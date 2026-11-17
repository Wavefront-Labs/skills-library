---
id: computing-software.software-engineering.rust.send-sync-and-shared-state
name: send-sync-and-shared-state
category: computing-software
field: software-engineering
product: rust
tags: [rust, rust-concurrency, send-sync, arc-mutex, rwlock, atomics, scoped-threads, poisoning, parking-lot, lazylock, rust-arc-mutex, rust-lock-poisoning, rust-rwlock-condvar]
level: advanced
status: verified
description: "Share state across Rust threads: what Send and Sync mean, Arc<Mutex<T>> vs RwLock vs atomics, scoped threads, lock poisoning and fixing 'cannot be sent between threads'."
sources: ["https://doc.rust-lang.org/book/ch16-03-shared-state.html", "https://doc.rust-lang.org/book/ch16-04-extensible-concurrency-sync-and-send.html", "https://doc.rust-lang.org/nomicon/send-and-sync.html", "https://doc.rust-lang.org/std/thread/fn.scope.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Send, Sync and shared state

**Goal:** share data across threads with the compiler's help, choosing the cheapest
correct primitive.

## The two traits
- `T: Send` - ownership of T can move to another thread.
- `T: Sync` - `&T` can be shared between threads (i.e. `&T: Send`).
Both are auto-implemented when all fields are. Notable exceptions: `Rc` (neither),
`RefCell`/`Cell` (Send but not Sync), raw pointers (neither), `MutexGuard` (not Send).

Error "`Rc<...>` cannot be sent between threads safely" -> switch to `Arc`.
Error "`RefCell<...>` cannot be shared between threads" -> `Mutex`/`RwLock`/atomics.

## Choosing a primitive
| Data | Use |
|---|---|
| Immutable after setup | `Arc<T>` (no lock) |
| Counter / flag | `AtomicU64`, `AtomicBool` (with `Ordering::Relaxed` for pure counters) |
| Mutable, mostly writes or short sections | `Arc<Mutex<T>>` |
| Read-heavy, rare writes | `Arc<RwLock<T>>`, or `arc-swap` for whole-value replacement |
| Global lazily initialised | `static CFG: LazyLock<Config> = LazyLock::new(load);` (1.80+) / `OnceLock` |
| Work handed between threads | channels instead of shared state |

## Patterns
```rust
let state = Arc::new(Mutex::new(HashMap::new()));
let handles: Vec<_> = (0..4).map(|i| {
    let state = Arc::clone(&state);
    thread::spawn(move || { state.lock().unwrap().insert(i, i * i); })
}).collect();
for h in handles { h.join().unwrap(); }
```
Scoped threads borrow without Arc:
```rust
thread::scope(|s| { for chunk in data.chunks(1000) { s.spawn(move || process(chunk)); } });
```

## Lock hygiene
- Keep guards short: compute outside, lock, mutate, drop. `drop(guard)` explicitly
  before slow work. Never hold a std `Mutex` guard across `.await` (use
  `tokio::sync::Mutex` only if you must hold it across awaits).
- Poisoning: if a thread panics while holding a std Mutex, later `lock()` returns
  `Err(PoisonError)`. `.unwrap()` propagates the panic (usually right); `parking_lot`
  locks have no poisoning (its docs: "No poisoning, the lock is released normally on panic"; compare its README before choosing it for speed).
- Lock ordering to avoid deadlocks when taking several locks.

## Verify
- [ ] `cargo test` plus a stress test; for lock-free code, `loom` model checking.
- [ ] No `MutexGuard` held across `.await` (clippy `await_holding_lock`).

## Checked
- rustc/cargo 1.99.1 (stable, Windows msvc, edition 2024), tokio 1.54.0, futures 0.3.34, rayon 1.12.0, thiserror 2.0.21, anyhow 1.0.104, color-eyre 0.6.5.
- Ran: `Arc<Mutex<HashMap>>` with four threads inserting (len 4), `thread::scope` with `chunks(1000)` summing to 3000, a `static LazyLock<String>` (stable since 1.80.0, std source), `RefCell` and `Cell` pass a `Send` assertion, a thread that panicked while holding a std Mutex left it poisoned (`is_poisoned()` true and `lock()` returned `Err`).
- Compile-fail: `assert_sync::<RefCell<u8>>()` gives "`RefCell<u8>` cannot be shared between threads safely"; `assert_send::<Rc<u8>>()` gives "`Rc<u8>` cannot be sent between threads safely"; `assert_send::<MutexGuard<u8>>()` is rejected.
- parking_lot docs.rs: "No poisoning, the lock is released normally on panic". The earlier "faster under contention" statement was removed (the README lists features, not a benchmark).
