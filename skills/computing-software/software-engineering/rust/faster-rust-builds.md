---
id: computing-software.software-engineering.rust.faster-rust-builds
name: faster-rust-builds
category: computing-software
field: software-engineering
product: rust
tags: [rust, sccache, cargo-build-speed, mold, cargo-chef, compile-times, cargo-timings, docker, ci-caching, rust-ci-caching, rust-release-ci]
level: advanced
status: docs-checked
description: "Cut Rust compile times: measure with cargo build --timings, faster linkers (mold/lld), sccache, dev profile tweaks, crate splitting, and cargo-chef layered Docker builds."
sources: ["https://doc.rust-lang.org/cargo/reference/timings.html", "https://github.com/mozilla/sccache", "https://github.com/rui314/mold", "https://github.com/LukeMathWalker/cargo-chef", "https://doc.rust-lang.org/cargo/reference/profiles.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Faster Rust builds

**Goal:** shorter edit-compile-test loops locally and cheaper CI, by measuring where time goes
and applying the fixes that matter.

## Measure first
```bash
cargo build --timings          # writes target/cargo-timings/cargo-timing.html
cargo llvm-lines | head        # generic code bloat (cargo-llvm-lines)
```
The timings report shows which crates are on the critical path and how parallel the build is. Big
single crates and proc-macro chains (syn) at the start are the usual culprits.

## Local loop
- `cargo check` instead of `cargo build` while editing (no codegen). rust-analyzer already runs it.
- **Faster linker** (linking dominates incremental builds of binaries):
```toml
# .cargo/config.toml
[target.x86_64-unknown-linux-gnu]
linker = "clang"
rustflags = ["-C", "link-arg=-fuse-ld=mold"]
```
  rust-lld is the default linker on `x86_64-unknown-linux-gnu` since Rust 1.90 (so try the default before adding mold).
- Dev profile:
```toml
[profile.dev]
debug = "line-tables-only"   # much less debuginfo to write; still get backtraces
[profile.dev.package."*"]
opt-level = 1                # optimise deps once, keep your crate at 0 (helps slow test runs)
```
- Split large crates into a workspace so changes rebuild less and crates compile in parallel.
  Keep generic-heavy code from being monomorphised in every downstream crate (non-generic inner
  function pattern).
- Trim features: `default-features = false` on heavy deps; `cargo tree -e features` to audit.

## sccache (shared compilation cache)
```bash
cargo install sccache --locked
export RUSTC_WRAPPER=sccache          # or [build] rustc-wrapper = "sccache" in config.toml
sccache --show-stats
```
Backends include local disk, S3, R2, GCS, Azure, Redis and the GitHub Actions cache (`SCCACHE_GHA_ENABLED=on`).
Limits: incrementally compiled crates are not cached (set `CARGO_INCREMENTAL=0` in CI),
and absolute paths must match across machines for hits unless you set `SCCACHE_BASEDIRS`.

## CI
- `Swatinem/rust-cache` caches Cargo state and `target/` keyed on a hash of Cargo.lock and Cargo.toml files; it sets
  `CARGO_INCREMENTAL=0` itself.
- Avoid rebuilding between steps: run `cargo build --all-targets` once, then test/clippy reuse it
  when flags match (different RUSTFLAGS invalidate the cache).

## Docker: cargo-chef
```dockerfile
FROM lukemathwalker/cargo-chef:latest-rust-1 AS chef
WORKDIR /app
FROM chef AS planner
COPY . .
RUN cargo chef prepare --recipe-path recipe.json
FROM chef AS builder
COPY --from=planner /app/recipe.json recipe.json
RUN cargo chef cook --release --recipe-path recipe.json   # deps only: cached layer
COPY . .
RUN cargo build --release --bin app
FROM debian:trixie-slim AS runtime
COPY --from=builder /app/target/release/app /app
ENTRYPOINT ["/app"]
```
Dependency layer is reused until Cargo.toml/Cargo.lock change. Alternatively BuildKit cache mounts:
`RUN --mount=type=cache,target=/usr/local/cargo/registry --mount=type=cache,target=/app/target cargo build --release` (BuildKit; not part of cargo-chef).

## Verify
- [ ] `--timings` before/after shows the critical path shortened.
- [ ] Incremental rebuild after a one-line change is measured and acceptable.
- [ ] CI cache hit rate visible (`sccache --show-stats` or rust-cache logs).

## Checked

2026-10-25. Checked against the Cargo Book (timings report path `target/cargo-timings/cargo-timing.html`, profiles: `line-tables-only` since 1.71, `[profile.dev.package."*"]`), the Rust 1.90 release notes (lld default on x86_64-unknown-linux-gnu), the sccache README (backends, `RUSTC_WRAPPER`, `SCCACHE_BASEDIRS`, incremental limitation) and its GHA doc (`SCCACHE_GHA_ENABLED=on`), the mold README (`-C link-arg=-fuse-ld=mold`), the Swatinem/rust-cache README (key inputs, `CARGO_INCREMENTAL=0`), the cargo-llvm-lines README and the cargo-chef README (`lukemathwalker/cargo-chef:latest-rust-1`, prepare/cook, Debian runtime stage). Removed unconfirmed items: Cranelift flag, `-Z time-passes`, macOS linker remark, distroless image, nextest and cargo-hack advice.

Method: documentation only; no commands were run.
