---
id: computing-software.software-engineering.rust.atomics-and-memory-ordering-in-rust
name: atomics-and-memory-ordering-in-rust
category: computing-software
field: software-engineering
product: rust
tags: [rust, rust-atomics, memory-ordering, atomicusize, acquire-release, seqcst, lock-free, loom]
level: advanced
status: verified
description: "Use Rust std::sync::atomic correctly: Relaxed for counters, Acquire/Release for publishing data, SeqCst when in doubt, compare_exchange loops, and testing with loom."
sources: ["https://doc.rust-lang.org/std/sync/atomic/index.html", "https://doc.rust-lang.org/nomicon/atomics.html", "https://marabos.nl/atomics/", "https://github.com/tokio-rs/loom"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Atomics and memory ordering in Rust

**Goal:** lock-free counters, flags and one-time publication that are correct on weakly ordered
CPUs (ARM), not just on x86.

## Types and operations
`AtomicBool`, `AtomicUsize`/`I64`/..., `AtomicPtr<T>`. Operations: `load`, `store`, `swap`,
`fetch_add`/`sub`/`and`/`or`/`max`, `compare_exchange(current, new, success_ord, failure_ord)`,
`compare_exchange_weak` (may fail spuriously, use in loops), `try_update(set, fetch, f)` (stable since 1.95; `fetch_update` is the old name and now warns as deprecated).
Share via `static` or `Arc<AtomicX>`; atomics are `Sync`, so `&AtomicUsize` is enough.

## Picking an Ordering
| Use case | Ordering |
|---|---|
| statistics counter, id generator (no other data depends on it) | `Relaxed` |
| publish data: writer sets a flag after writing data | `Release` store |
| consume: reader checks flag then reads data | `Acquire` load |
| read-modify-write that both consumes and publishes | `AcqRel` |
| need a single global order of several atomics (rare, e.g. Dekker-style) | `SeqCst` |
Release/Acquire create a **happens-before** edge: everything the writer did before the Release store
is visible to a reader whose Acquire load sees that store. `Relaxed` guarantees atomicity of the
variable only, nothing about other memory.

```rust
static READY: AtomicBool = AtomicBool::new(false);
static mut DATA: u64 = 0;
// writer
unsafe { DATA = 42; }
READY.store(true, Ordering::Release);
// reader
if READY.load(Ordering::Acquire) { assert_eq!(unsafe { DATA }, 42); }
```
(Prefer `OnceLock`/`OnceCell` for one-time init: they do this for you without unsafe.)

## compare_exchange loop
```rust
fn increment_capped(c: &AtomicUsize, cap: usize) -> bool {
    let mut cur = c.load(Ordering::Relaxed);
    loop {
        if cur >= cap { return false; }
        match c.compare_exchange_weak(cur, cur + 1, Ordering::AcqRel, Ordering::Relaxed) {
            Ok(_) => return true,
            Err(actual) => cur = actual,
        }
    }
}
```
Or `c.try_update(Ordering::AcqRel, Ordering::Relaxed, |v| (v < cap).then_some(v + 1)).is_ok()`
(on toolchains before 1.95 use `fetch_update`, same arguments).

## Rules of thumb
- If unsure, `SeqCst` is correct whenever a weaker ordering is; optimise only with a proof and a
  loom test. On x86-64 loads and Relaxed/Release stores all compile to a plain `mov` (rustc -O asm: Relaxed, Acquire and SeqCst loads and Relaxed/Release stores are identical; only a SeqCst store becomes `xchg`), which hides ordering bugs that appear on
  ARM.
- Atomics do not compose: two separate atomics cannot be updated together atomically. Use a Mutex,
  or pack both into one `AtomicU64`.
- Spinning: use `std::hint::spin_loop()` inside spin loops and fall back to parking
  (`std::thread::park`) or a real lock; pure spin locks are bad in user space.
- False sharing: pad hot per-thread atomics to cache lines (`crossbeam_utils::CachePadded`).
- Pointer-based lock-free structures need safe memory reclamation (`crossbeam-epoch`, hazard
  pointers, `arc-swap` for swapping Arcs). `ArcSwap` is the easy answer for read-mostly config.

## Testing with loom
```rust
#[cfg(loom)] use loom::sync::atomic::{AtomicUsize, Ordering};
#[test] #[cfg(loom)]
fn concurrent_inc() { loom::model(|| { /* spawn loom::thread, assert invariants */ }); }
```
`RUSTFLAGS="--cfg loom" cargo test --release` explores all interleavings and weak-memory
behaviours permitted by the C++20 model. Declare `loom = "0.7"` under `[target.'cfg(loom)'.dependencies]` and
add `[lints.rust] unexpected_cfgs = { level = "warn", check-cfg = ['cfg(loom)'] }` to silence the unknown-cfg
warning. `--cfg loom` rebuilds every dependency, and tokio itself fails to compile under it (it has its own
`cfg(loom)` paths), so keep model-checked code in a crate without tokio. Miri also detects data races and
emulates some weak-memory effects (its README says "some", not complete).

## Verify
- [ ] Each non-SeqCst ordering has a comment naming its paired operation.
- [ ] loom or Miri test exercises the concurrent path.
- [ ] Tested on an ARM machine/CI runner, not only x86.

## Checked
- rustc/cargo 1.99.1 (stable, Windows msvc, edition 2024), tokio 1.54.0, futures 0.3.34, rayon 1.12.0, thiserror 2.0.21, anyhow 1.0.104, color-eyre 0.6.5.
- Ran the Release/Acquire flag example across two threads (assert 42 held), the `compare_exchange_weak` capped increment with 8 threads x 1000 increments against cap 5000 (final 5000, further calls return false), and `fetch_update`: on 1.99.1 it is deprecated "renamed to `try_update` for consistency"; std source shows `try_update` `#[stable(... since = "1.95.0")]`. `try_update`/`fetch_update` with `then_some` returned the expected bool; `CachePadded` aligned to 128; `ArcSwap` and `OnceLock` snippets ran.
- `rustc -O --emit asm` for x86-64: all loads and Relaxed/Release stores are `mov`; SeqCst store is `xchg`; `fetch_add` is `lock inc` for both orderings.
- loom 0.7 model test (two threads `fetch_add`) passed with `RUSTFLAGS="--cfg loom" cargo test --release` in a crate with only loom; the same flag in a crate depending on tokio failed (`E0433` in tokio-stream's build). Miri README: "Data races and emulation of *some* weak memory effects". Miri itself was not run here.
