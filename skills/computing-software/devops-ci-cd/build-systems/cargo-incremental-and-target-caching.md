---
id: computing-software.devops-ci-cd.build-systems.cargo-incremental-and-target-caching
name: cargo-incremental-and-target-caching
category: computing-software
field: devops-ci-cd
product: build-systems
tags: [build-systems, cargo-incremental, compiler-caches, sccache]
level: practitioner
status: docs-checked
description: "Make Rust CI builds fast: incremental off in CI, caching target/ and the cargo registry (rust-cache), sccache, and profile settings that cut compile and link time."
sources: ["https://doc.rust-lang.org/cargo/reference/profiles.html", "https://github.com/Swatinem/rust-cache", "https://github.com/mozilla/sccache/blob/main/docs/Rust.md", "https://blog.rust-lang.org/2025/09/01/rust-lld-on-1.90.0-stable/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Cargo incremental and target directory caching

## Incremental in CI: turn it off
Incremental compilation helps local edit-compile loops but bloats `target/` and rarely helps from-
scratch CI builds. Set `CARGO_INCREMENTAL=0` in CI (rust-cache sets it automatically).

## Cache what matters
```yaml
- run: rustup toolchain install stable --profile minimal
- uses: Swatinem/rust-cache@v2
  with:
    shared-key: ci            # stable key shared across jobs
    save-if: ${{ github.ref == 'refs/heads/main' }}   # only main writes, PRs read
- run: cargo test --locked
```
rust-cache caches `~/.cargo` registry and git data and the `target/` dependency artifacts. Before saving it removes incremental artifacts, unused dependencies, anything that is not a dependency (the workspace crates are not cached) and artifacts with an mtime older than a week. The key is derived from the job, the Rust environment and a hash of `Cargo.toml`/`Cargo.lock` and toolchain files, and it can restore from an older `Cargo.lock` version.

## sccache alternative/addition
`RUSTC_WRAPPER=sccache` with a GitHub Actions, S3 or GCS backend caches per-crate compilation across jobs and runners. sccache's Rust documentation says incremental compilation must be disabled, and that crates that invoke the system linker (`bin`, `dylib`, `cdylib`, `proc-macro`) cannot be cached.

## Profile tweaks
```toml
[profile.dev]
debug = "line-tables-only"     # minimal debug info for backtraces: smaller artifacts, faster links
[profile.dev.package."*"]
opt-level = 1                  # optimise dependencies only
[profile.ci]
inherits = "dev"
debug = false
```
Custom profiles must name the profile they inherit from (`inherits`); run it with `cargo build --profile ci`.
Faster linkers cut link time: since Rust 1.90 `rustc` uses `rust-lld` by default on `x86_64-unknown-linux-gnu`; `mold` is an alternative.

## Verify
- [ ] Warm-cache CI build time is a fraction of cold; cache size stays stable across commits.

## Checked
Date: 2026-10-25. Documentation: The Cargo Book (rust-lang/cargo `doc/book/src/reference/profiles.md`, `environment-variables.md`), Swatinem/rust-cache README, mozilla/sccache `docs/Rust.md`, Rust blog "rust-lld on stable 1.90.0".
Confirmed: `incremental` profile setting and its CI cost; rust-cache sets `CARGO_INCREMENTAL=0`, its pruning rules, `shared-key`, `save-if` inputs and key contents; sccache's incremental and linker-crate limitations; `debug = "line-tables-only"` (MSRV 1.71); `inherits` for custom profiles; lld default on x86_64 Linux from 1.90.
Removed: the `dtolnay/rust-toolchain` action (replaced with plain rustup), the "build and test compile different feature sets" and "clippy shares cache only with the same flags" gotchas (not in the documentation read).
Method: documentation only; no commands were run.
