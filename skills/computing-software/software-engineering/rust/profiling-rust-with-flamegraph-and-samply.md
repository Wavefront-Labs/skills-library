---
id: computing-software.software-engineering.rust.profiling-rust-with-flamegraph-and-samply
name: profiling-rust-with-flamegraph-and-samply
category: computing-software
field: software-engineering
product: rust
tags: [rust, cargo-flamegraph, samply, perf, profiling, flame-graphs, dhat, heaptrack, performance, rust-performance]
level: advanced
status: docs-checked
description: "Profile Rust CPU and memory: release builds with debug symbols, cargo flamegraph and perf, samply with the Firefox Profiler, and heap profiling with dhat or heaptrack."
sources: ["https://github.com/flamegraph-rs/flamegraph", "https://github.com/mstange/samply", "https://nnethercote.github.io/perf-book/profiling.html", "https://docs.rs/dhat/latest/dhat/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Profiling Rust (cargo flamegraph / samply)

**Goal:** find where a Rust program actually spends CPU time and allocations, on an optimised
build, before optimising anything.

## Build for profiling
Profile release code (debug builds have different hotspots) but keep symbols:
```toml
[profile.profiling]
inherits = "release"
debug = true            # or "line-tables-only" for smaller binaries
```
`cargo build --profile profiling`. Add `-C force-frame-pointers=yes` (RUSTFLAGS) for reliable
frame-pointer unwinding, useful with perf on stripped std. Do not set `strip = true` here.

## samply (Linux, macOS, Windows)
```bash
cargo install --locked samply
samply record ./target/profiling/myapp --input big.json
```
Opens the Firefox Profiler in the browser: call tree, inverted tree (hottest leaf functions),
flame graph, per-thread timelines, source view with per-line samples. Easiest cross-platform choice.
On Linux it needs access to perf events, for example `echo 1 | sudo tee /proc/sys/kernel/perf_event_paranoid`; macOS cannot profile signed system binaries.

## cargo flamegraph
```bash
cargo install flamegraph
cargo flamegraph --profile profiling --bin myapp -- --input big.json   # writes flamegraph.svg
cargo flamegraph --bench parse -- --bench                              # profile a benchmark
cargo flamegraph --root ...    # run with root privileges via sudo
```
Uses `perf` on Linux, `xctrace` on macOS, and the blondie library (or DTrace) on Windows. On Linux with lld (the default since Rust 1.90) or mold, build with `-Clink-arg=-Wl,--no-rosegment` (for example in `[target.x86_64-unknown-linux-gnu] rustflags`) or perf cannot generate accurate stacks. Read the SVG: width = share of samples, look for wide
plateaus near the top (functions doing the work themselves). Click to zoom, Ctrl-F to search.

## perf directly (Linux)
`perf` is a general-purpose profiler that uses hardware performance counters; Hotspot and the Firefox Profiler can view its recordings (see the Rust Performance Book profiling chapter).

## Heap profiling
- **dhat-rs**: in-process, portable.
```rust
#[cfg(feature = "dhat-heap")] #[global_allocator] static ALLOC: dhat::Alloc = dhat::Alloc;
fn main() { #[cfg(feature = "dhat-heap")] let _p = dhat::Profiler::new_heap(); /* ... */ }
```
  Writes `dhat-heap.json`, viewed in the DHAT viewer: total bytes, peak, allocation sites.
- dhat also supports heap usage testing: `dhat::assert_eq!` on `dhat::HeapStats` in tests to prevent allocation regressions.

## Async code
Stacks in tokio programs are full of runtime frames; use the inverted call tree to find leaf work,
and `tracing` spans with timing for request-level latency.

## Interpreting
- Many samples in `memcpy`/`alloc`/`drop_in_place`: reduce allocations and clones.
- Confirm wins with repeated benchmarks, not single runs.

## Verify
- [ ] Profile taken on a release-like build with symbols (function names, not addresses).
- [ ] The hot path identified accounts for a meaningful share of samples.
- [ ] Improvement confirmed by repeated benchmark runs.

## Checked

2026-10-25. Checked against the samply README (macOS, Linux and Windows; perf_event_paranoid; `cargo install --locked samply`; Firefox Profiler UI), the cargo-flamegraph README (Linux perf, macOS xctrace, Windows blondie/dtrace; `--profile`, `--bin`, `--bench`, `--root`; `--no-rosegment` needed with lld/mold), the dhat-rs source docs (`Profiler::new_heap`, `dhat-heap.json`, `dhat::assert_eq!` heap usage testing) and the Rust Performance Book (frame pointers, perf). Wrong in the draft and fixed: flamegraph uses `xctrace` on macOS, not dtrace; added the `--no-rosegment` requirement that now applies to the default Rust linker. Removed unconfirmed perf options, heaptrack, stats_alloc, tokio-console and hashing advice.

Method: documentation only; no commands were run.
