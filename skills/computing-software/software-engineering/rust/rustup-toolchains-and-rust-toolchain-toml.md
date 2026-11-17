---
id: computing-software.software-engineering.rust.rustup-toolchains-and-rust-toolchain-toml
name: rustup-toolchains-and-rust-toolchain-toml
category: computing-software
field: software-engineering
product: rust
tags: [rust, rustup, rust-toolchain-toml, toolchains, nightly, components, targets, ci, reproducible-builds, rust-tooling-quality]
level: practitioner
status: verified
description: "Manage Rust compilers with rustup: stable/beta/nightly and pinned versions, rust-toolchain.toml per project, components and targets, overrides, and CI caching."
sources: ["https://rust-lang.github.io/rustup/", "https://rust-lang.github.io/rustup/overrides.html", "https://rust-lang.github.io/rustup/concepts/components.html", "https://rust-lang.github.io/rustup/concepts/profiles.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# rustup toolchains and rust-toolchain.toml

**Goal:** every developer and CI job builds a project with the same compiler, components and
targets, without manual setup.

## Basics
```bash
rustup update                         # update installed toolchains and rustup itself
rustup toolchain install 1.85.0       # specific version
rustup toolchain install nightly-2026-09-01 --profile minimal
rustup default stable
rustup show                           # active toolchain and why (override source)
cargo +nightly build                  # one-off toolchain selection
rustup run 1.85.0 cargo test
```
Profiles: `minimal` (rustc, cargo, rust-std), `default` (+ rustfmt, clippy, rust-docs), `complete`.

## rust-toolchain.toml (per project)
```toml
[toolchain]
channel = "1.85.0"          # or "stable", "nightly-2026-09-01"
components = ["rustfmt", "clippy", "rust-src"]
targets = ["wasm32-unknown-unknown", "aarch64-unknown-linux-gnu"]
profile = "minimal"
```
- Placed at the repo root; rustup auto-installs the toolchain, components and targets on first
  `cargo` invocation in that directory (rustup 1.29.1 does so with a warning; opt out with `RUSTUP_AUTO_INSTALL=0` or `rustup set auto-install disable`; tested).
- Pin an exact version for applications (reproducible builds, controlled upgrades of new clippy
  lints). Libraries often use `stable` and express their minimum via `rust-version` in Cargo.toml
  instead.
- Nightly pins must include a date; plain `nightly` drifts daily. Check component availability for a
  date at the rustup-components-history page before pinning (clippy/miri sometimes miss days).

## Override precedence (highest first)
1. `cargo +toolchain` shorthand on the command line
2. `RUSTUP_TOOLCHAIN` env var (tested: `RUSTUP_TOOLCHAIN=stable cargo +nightly` ran nightly)
3. Directory override (`rustup override set nightly` - stored in rustup settings, not the repo; tested: it beat a rust-toolchain.toml in the same directory)
4. `rust-toolchain.toml` (or legacy `rust-toolchain`) found walking up from the current dir
5. Default toolchain
`rustup show` prints which rule applied, the first thing to check when versions differ.

## Components and targets
```bash
rustup component add rust-analyzer llvm-tools-preview      # llvm-tools-preview installs the llvm-tools component
rustup +nightly component add miri                         # miri is nightly-only: unavailable for stable (tested)
rustup target add x86_64-unknown-linux-musl thumbv7em-none-eabihf
rustup target list --installed
```
A target only adds the standard library; linking for another OS/arch still needs a linker (see
cross-compilation).

## CI
- GitHub Actions: `dtolnay/rust-toolchain@stable` (or `@1.85.0`, with `components:`), or just run
  `rustup show` / `rustup toolchain install` - with rust-toolchain.toml present, any cargo command
  installs the pinned toolchain.
- Cache `~/.cargo/registry`, `~/.cargo/git` and `target/` (Swatinem/rust-cache) keyed on the
  toolchain and Cargo.lock.
- Add an MSRV job: `cargo +1.75.0 check` matching `rust-version`.

## Gotchas
- Toolchains live in `~/.rustup` (or `RUSTUP_HOME`); disk use grows with dated nightlies -
  `rustup toolchain list` then `rustup toolchain uninstall`.
- Distro-packaged rustc/cargo conflict with rustup; remove them or ensure `~/.cargo/bin` comes first
  on PATH.
- In Docker, use the `rust:<version>` image and keep rust-toolchain.toml consistent with it, or the
  build downloads a second toolchain.

## Verify
- [ ] Fresh clone + `cargo build` installs the pinned toolchain automatically.
- [ ] `rustup show` in CI logs matches rust-toolchain.toml.
