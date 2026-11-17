---
id: computing-software.software-engineering.rust.choosing-an-async-runtime
name: choosing-an-async-runtime
category: computing-software
field: software-engineering
product: rust
tags: [rust, rust-async, rust-runtime-choice, tokio, async-std, smol, runtime-agnostic]
level: practitioner
status: docs-checked
description: "Pick and structure around a Rust async runtime: tokio vs smol, runtime-agnostic library design, and the schedulers and drivers of the tokio runtime."
sources:
  - https://tokio.rs/tokio/tutorial
  - https://docs.rs/tokio/latest/tokio/runtime/index.html
  - https://github.com/smol-rs/smol
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Choosing an async runtime

**Goal:** a defensible runtime choice and libraries that do not lock users in.

- **tokio**: the usual default for servers. Its multi-thread scheduler runs futures on a work-stealing thread pool (one worker per CPU core by default) and the docs say most applications should use it. The tokio tutorial describes the runtime as scaling from a multi-threaded work-stealing runtime to a light-weight single-threaded one.
- **smol**: "a small and fast async runtime" that re-exports smaller crates (async-executor, async-channel and others); suited to small tools. To use tokio-based libraries with smol, wrap futures and I/O types with the `async-compat` adapter. Check the project's current status before choosing async-std for new code.

```rust
#[tokio::main]                         // multi-thread scheduler by default
async fn main() { /* ... */ }

#[tokio::main(flavor = "current_thread")]   // single thread
async fn main() { /* ... */ }

let rt = tokio::runtime::Builder::new_multi_thread()
    .worker_threads(4).enable_all().thread_name("svc").build()?;
rt.block_on(run());
```

The multi-thread scheduler needs the `rt-multi-thread` feature; the current-thread scheduler needs `rt`. When you build a runtime by hand no resource drivers are enabled, so networking and time types fail until you call `enable_io`, `enable_time` or `enable_all`. A current-thread runtime spawns no worker threads: it only runs tasks while you call `Runtime::block_on` (`Handle::block_on` does not drive it), and a `LocalSet` runs its local tasks only when awaited or driven.

Library design: take generic `impl Future` and I/O traits rather than a concrete runtime type, avoid calling `tokio::spawn` internally (return futures or accept a spawner), and feature-gate runtime bindings.

## Gotchas
- Mixing runtimes: tokio networking and timer types need a tokio runtime with drivers enabled; smol-based code needs `async-compat` to use tokio-based libraries.
- The multi-thread scheduler spawns threads for tasks and for `spawn_blocking` calls.
- A current-thread runtime that never reaches `Runtime::block_on` runs nothing.

## Verify
Run `cargo tree -d` and look for a single runtime family among tokio and smol; exercise the code under both flavors you support.

## Checked
Confirmed from the tokio runtime module page (multi-thread work-stealing scheduler, default worker per core, `rt-multi-thread` and `rt` flags, no drivers by default, `enable_io`/`enable_time`/`enable_all`, current-thread needs `Runtime::block_on`, `Handle::block_on` insufficient, LocalSet, `spawn_blocking` threads), the tokio tutorial (runtime range) and the smol README (small and fast runtime, re-exports, async-compat). Removed: the claim that async-std is discontinued, embassy/glommio/monoio, the "no reactor running" and Handle::current panic claims, the `#[tokio::test]` flavor claim, async fn in traits stable version, and the grep verify command.

Method: docs-checked 2026-11-09 against the tokio runtime docs.rs page, tokio tutorial intro and smol README.
