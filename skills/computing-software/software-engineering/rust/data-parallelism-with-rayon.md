---
id: computing-software.software-engineering.rust.data-parallelism-with-rayon
name: data-parallelism-with-rayon
category: computing-software
field: software-engineering
product: rust
tags: [rust, rust-concurrency, rayon, par-iter, data-parallelism, work-stealing, threadpool, join, cpu-bound]
level: practitioner
status: verified
description: "Parallelise CPU-bound Rust with rayon: par_iter conversions, join for divide and conquer, custom thread pools, ordering and reduction, and when it does not help."
sources: ["https://docs.rs/rayon/latest/rayon/", "https://docs.rs/rayon/latest/rayon/iter/index.html", "https://docs.rs/rayon/latest/rayon/struct.ThreadPoolBuilder.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Data parallelism with rayon

**Goal:** use all cores for CPU-heavy loops by changing `iter()` to `par_iter()`, with
the compiler guaranteeing no data races.

## Basics
```rust
use rayon::prelude::*;
let total: u64 = files.par_iter().map(|f| count_words(f)).sum();
let mut v = big_vec; v.par_sort_unstable();
let results: Vec<_> = inputs.into_par_iter().filter_map(parse).collect();   // order preserved
images.par_chunks_mut(1024).for_each(|chunk| blur(chunk));
```
Closures must be `Send + Sync` friendly: no `Rc`, no `RefCell` captured mutably. Rayon
uses a global work-stealing pool sized to logical CPUs.

## Divide and conquer
```rust
fn sum(xs: &[u64]) -> u64 {
    if xs.len() < 10_000 { return xs.iter().sum(); }       // sequential cutoff
    let (l, r) = xs.split_at(xs.len() / 2);
    let (a, b) = rayon::join(|| sum(l), || sum(r));
    a + b
}
```

## Reductions and shared output
- Prefer `map` + `reduce`/`sum`/`collect` over locking a shared `Mutex<Vec>`.
- `fold` + `reduce` for per-thread accumulators: `.fold(HashMap::new, add).reduce(HashMap::new, merge)`.
- `collect` into `Vec` preserves order; `for_each` does not run in order.

## Custom pools
```rust
let pool = rayon::ThreadPoolBuilder::new().num_threads(4).build()?;
pool.install(|| data.par_iter().for_each(work));
```
Use to cap CPU usage, or `RAYON_NUM_THREADS=4` env var for the global pool.

## When it does not help
- Tiny work per item: overhead dominates. Use `with_min_len(1024)` (only on indexed iterators: slices, `Vec`, `usize` ranges; `(0..n)` over `u64` is not indexed and `with_min_len` fails to compile) or chunk manually.
- I/O-bound work: rayon threads block; use async or a dedicated thread pool.
- Inside async runtimes: never run rayon work directly on a tokio worker; offload with
  `tokio::task::spawn_blocking` or send to rayon and await a oneshot.
- Memory-bandwidth-bound loops scale poorly beyond a few cores.

## Gotchas
- Panics in a parallel closure propagate to the caller after other tasks finish.
- Nested `par_iter` is fine (work stealing handles it), but a blocking call inside can
  deadlock the pool if everything waits on everything.

## Verify
- [ ] Benchmark (criterion) sequential vs parallel; speedup recorded.
- [ ] Results identical to the sequential version in tests (watch float summation order differences).

## Checked
- rustc/cargo 1.99.1 (stable, Windows msvc, edition 2024), tokio 1.54.0, futures 0.3.34, rayon 1.12.0, thiserror 2.0.21, anyhow 1.0.104, color-eyre 0.6.5. Ran: `par_iter().map().sum()` (equal to the sequential sum, 2999997), `par_sort_unstable`, `into_par_iter().filter_map().collect()` (order preserved: 0,2,..,18), `par_chunks_mut`, the `rayon::join` recursive sum (equal to the sequential sum), `fold(HashMap::new, ..).reduce(HashMap::new, ..)` (counts 333334/333333/333333), `ThreadPoolBuilder::new().num_threads(4)` + `install` (reported 4 threads, global pool reported 12; `RAYON_NUM_THREADS=3` gave 3), `for_each` into a Mutex<Vec> (not in order), a panic inside a parallel closure propagated to the caller via `catch_unwind`.
- `(0..100000u64).into_par_iter().with_min_len(1024)` fails ("doesn't satisfy `_: IndexedParallelIterator`"); the `usize` range works.
