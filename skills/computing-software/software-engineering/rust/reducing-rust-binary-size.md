---
id: computing-software.software-engineering.rust.reducing-rust-binary-size
name: reducing-rust-binary-size
category: computing-software
field: software-engineering
product: rust
tags: [rust, rust-performance, rust-binary-size, binary-size, opt-level, strip, lto, cargo-bloat]
level: practitioner
status: docs-checked
description: "Shrink Rust binaries with release profile settings, strip, panic=abort, cargo-bloat, build-std and avoiding fmt and monomorphisation bloat."
sources:
  - https://github.com/johnthagen/min-sized-rust
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Reducing binary size

**Goal:** the smallest binary that is acceptable, with numbers.

```toml
[profile.release]
opt-level = "z"        # optimise for size; "s" is sometimes smaller, so try both (default is 3, for speed)
lto = true             # link-time optimisation, often removes dead code
codegen-units = 1      # default is 16 for release; 1 allows more size optimisation
panic = "abort"        # drops unwinding code (changes panic behaviour)
strip = true           # Rust 1.59+; before that run strip on the binary
```

Build with `cargo build --release`. Measure with `cargo-bloat` (what takes most of the space) and `cargo-llvm-lines` (number and size of instantiations of each generic function).

Nightly-only extras: `-Zlocation-detail=none` removes file/line/column details of panics; `-Zfmt-debug=none` turns `#[derive(Debug)]` and `{:?}` into no-ops (it ruins `dbg!`, `assert!`, `unwrap` output); `build-std` rebuilds the standard library from source:

```bash
rustup toolchain install nightly
rustup component add rust-src --toolchain nightly
rustc -vV     # note the host target triple
RUSTFLAGS="-Zlocation-detail=none -Zfmt-debug=none" cargo +nightly build \
  -Z build-std=std,panic_abort -Z build-std-features="optimize_for_size" \
  --target <HOST_TRIPLE> --release
```

`panic_abort` in `build-std` is what makes the `panic = "abort"` option work. For an executable under 20 KB, `core::fmt` must be removed (`#![no_main]`, manual stdio, careful use of `libstd`); `#![no_std]` with `libc` goes smaller still, at the cost of much `unsafe` code and most crates.

Optional compression: `upx --best --lzma target/release/app` (UPX claims 50-70%, depends on the executable).

## Gotchas
- `panic = "abort"` is the one release setting listed here that changes program behaviour (no unwinding, no helpful backtrace); `prefer-dynamic` is not a size fix (no stable ABI).
- UPX-packed binaries have been flagged by heuristic antivirus software.
- Binary-size runs before and after must use the same target and flags.

## Verify
Compare the size of `target/release/app` before and after each change, and record it in CI to catch regressions.

## Checked
2026-11-08. Read in full: min-sized-rust README (johnthagen/min-sized-rust, raw README). Confirmed: release profile settings and defaults, strip and Rust 1.59, panic=abort behaviour note, nightly flags, build-std commands, UPX options and antivirus warning, cargo-bloat and cargo-llvm-lines descriptions, prefer-dynamic limits. Removed (not on the page): the Cargo profiles reference source, bloat flags, source-level crate swaps (regex-lite, miniserde), the dyn Trait advice, glibc versus musl size claim, `lto = "fat"`, UPX startup cost, split-debuginfo advice.
Method: documentation only; no commands were run.
