---
id: computing-software.software-engineering.rust.reducing-allocations-and-heap-profiling
name: reducing-allocations-and-heap-profiling
category: computing-software
field: software-engineering
product: rust
tags: [rust, rust-performance, rust-allocations, allocations, heap-profiling, dhat, jemalloc]
level: practitioner
status: docs-checked
description: "Find and reduce heap allocations in Rust with DHAT, counting allocators, capacity hints, SmallVec and allocator swaps."
sources:
  - https://nnethercote.github.io/perf-book/heap-allocations.html
  - https://docs.rs/dhat
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Reducing allocations and heap profiling

**Goal:** locate allocation hot spots with data, then remove them.

Measure first. If a general-purpose profiler shows `malloc`/`free` as hot, reducing the allocation rate or swapping the allocator is worth trying. The `dhat` crate (heap and ad hoc profiling, release builds only) is set up like this:

```rust
// Cargo.toml: dhat as a dependency; [profile.release] debug = 1; [features] dhat-heap = []
#[cfg(feature = "dhat-heap")]
#[global_allocator]
static ALLOC: dhat::Alloc = dhat::Alloc;
fn main() {
    #[cfg(feature = "dhat-heap")]
    let _profiler = dhat::Profiler::new_heap();
    run();
}
// cargo run --release --features dhat-heap  -> dhat-heap.json, load it in DHAT's dh_view.html
```

`dhat::Alloc` is slower than the normal allocator, so enable it only while profiling. The crate measures only what happens within `main`. DHAT itself comes with Valgrind and works on Linux and some other Unixes.

Common fixes from the Rust Performance Book:
- `Vec::with_capacity`, `Vec::reserve`, `Vec::reserve_exact` (and `String::with_capacity`) when you know the length; a new `Vec` grows by quasi-doubling (0, 4, 8, 16, ...), which the book says is unspecified.
- Reuse a "workhorse" collection: declare it outside the loop and call `clear()`, which keeps capacity; or take `&mut Vec` instead of returning a new one.
- `SmallVec<[T; N]>` (smallvec crate) for many short vectors; `ArrayVec` (arrayvec) if you know the maximum length. SmallVec is slightly slower than `Vec` for normal operations and can be larger, so benchmark.
- `clone_from` instead of `a = b.clone()` can reuse the existing allocation.
- `Cow` to mix borrowed and owned data without allocating for the borrowed case.
- Avoid `format!` when a string literal will do (it allocates a `String`).
- `BufRead::read_line` with a reused `String` instead of `lines()`, which allocates per line.
- Rc/Arc `clone` only bumps a reference count, but Rc/Arc for rarely shared values can increase allocations.

Alternative allocators (for example jemalloc via `tikv-jemallocator`) can improve allocation performance without code changes; see the book's build-configuration chapter and benchmark on your target.

## Gotchas
- The book reports, from rustc experience, that cutting about 10 allocations per million instructions gave a measurable gain (about 1%); results vary.
- Use the profile to decide which `clone` or `to_owned` calls matter; many are fine.
- Keep tests guarding allocation counts with dhat's heap usage testing (`HeapStats::get`, `dhat::assert_eq!`).

## Verify
Compare `total_blocks` and `max_bytes` (`HeapStats`) or the DHAT viewer's totals before and after; confirm wall-clock improvement with a benchmark.

## Checked
2026-11-09. Confirmed against the Rust Performance Book Heap Allocations chapter (profiling advice, Vec growth, SmallVec, ArrayVec, with_capacity, clone_from, Cow, workhorse collections, read_line, format!) and the docs.rs dhat 0.3.3 crate page (setup, release-only, debug = 1, dhat-heap.json, dh_view.html, HeapStats fields). Removed: `valgrind --tool=dhat`, heaptrack, cargo flamegraph, tinyvec, `Box<[T]>`, `Arc<str>`, `iter().copied()`, `write!` buffer advice, mimalloc code and "double-digit gains", musl and `#[global_allocator]` process-wide notes (not stated on the pages). The alternative-allocator chapter was only searched, not read in full.
Method: documentation only; no commands were run.
