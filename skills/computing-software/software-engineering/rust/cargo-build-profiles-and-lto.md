---
id: computing-software.software-engineering.rust.cargo-build-profiles-and-lto
name: cargo-build-profiles-and-lto
category: computing-software
field: software-engineering
product: rust
tags: [rust, cargo, cargo-profiles, lto, codegen-units, release-optimization, panic-abort, debug-info, rust-codegen-units]
level: practitioner
status: verified
description: "Tune Cargo profiles: release vs dev settings, LTO and codegen-units, opt-level, panic=abort, debug info and split-debuginfo, custom profiles and faster dev builds."
sources:
  - https://doc.rust-lang.org/cargo/reference/profiles.html
  - https://nnethercote.github.io/perf-book/build-configuration.html
  - https://doc.rust-lang.org/rustc/codegen-options/index.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Cargo build profiles: release, LTO and codegen-units

**Goal:** fast iteration in development and maximally fast/small binaries for release, with debuggability where needed.

## 1. Defaults
| Setting | dev | release |
|---|---|---|
| opt-level | 0 | 3 |
| debug | true (full) | false |
| codegen-units | 256 | 16 |
| lto | false (thin-local) | false (thin-local) |
| incremental | true | false |
| overflow-checks | true | false |

## 2. A tuned release profile
```toml
[profile.release]
lto = "fat"            # whole-program optimisation; "thin" gets most of the gain with faster builds
codegen-units = 1      # better optimisation, slower compile
panic = "abort"        # smaller, faster; no unwinding (catch_unwind stops working)
strip = "symbols"      # or "debuginfo"
debug = "line-tables-only"   # keep file:line in backtraces and profilers at low size cost
```
Measure on your workload: LTO + `codegen-units=1` trades longer compile and link time for (usually) faster and smaller binaries; the size of the gain varies and no figure is given here.

## 3. Custom profiles
```toml
[profile.profiling]
inherits = "release"
debug = true           # full symbols for perf/flamegraph
strip = false

[profile.dist]
inherits = "release"
lto = "fat"
codegen-units = 1
```
`cargo build --profile profiling`; output in `target/profiling/`.

## 4. Faster dev builds
```toml
[profile.dev]
debug = "line-tables-only"     # much faster linking than full debug
[profile.dev.package."*"]
opt-level = 2                  # optimise dependencies once; your crate stays at 0 (big win for games, image, crypto)
[profile.dev.build-override]
opt-level = 3                  # proc-macros and build scripts run faster
```
Also: a faster linker (`mold`/`lld`; lld is default on x86_64 Linux since Rust 1.90), `cargo check` in the edit loop, `sccache` in CI.

## 5. Target CPU
`RUSTFLAGS="-C target-cpu=native"` (or `x86-64-v3`) enables AVX2 etc.; only for binaries run on known hardware, never for distributed binaries.

## Gotchas
- Profile settings in member crates of a workspace are ignored (warning); set them at the root.
- `panic = "abort"` in a library has no effect; the final binary decides. Tests always unwind.
- `overflow-checks = false` in release means arithmetic wraps silently; use `checked_*`/`wrapping_*` explicitly where it matters, or enable overflow-checks in release for safety-critical code.
- PGO/BOLT (`cargo-pgo`) can add further speed on top of LTO for hot services; measure it.

## Verify
- `hyperfine` or criterion benchmarks compare profiles on real workloads, `ls -l target/release/app` shows the size change, and backtraces still show file:line with line-tables debug info.
