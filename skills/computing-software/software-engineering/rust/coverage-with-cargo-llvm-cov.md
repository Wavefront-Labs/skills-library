---
id: computing-software.software-engineering.rust.coverage-with-cargo-llvm-cov
name: coverage-with-cargo-llvm-cov
category: computing-software
field: software-engineering
product: rust
tags: [rust, cargo-llvm-cov, code-coverage, instrument-coverage, lcov, codecov, nextest, tarpaulin]
level: practitioner
status: docs-checked
description: "Measure Rust test coverage with cargo-llvm-cov: HTML/lcov/Codecov output, nextest and doctests, workspaces, excluding code, and coverage of external binaries."
sources:
  - https://github.com/taiki-e/cargo-llvm-cov
  - https://doc.rust-lang.org/rustc/instrument-coverage.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Coverage with cargo-llvm-cov

**Goal:** accurate source-based coverage for Rust tests, viewable locally and reported in CI.

## Install and run
```bash
cargo install cargo-llvm-cov --locked     # or cargo binstall / taiki-e/install-action in CI
rustup component add llvm-tools-preview
cargo llvm-cov                             # run tests, print summary table
cargo llvm-cov --open                      # HTML report in browser
cargo llvm-cov --workspace --all-features --lcov --output-path lcov.info
cargo llvm-cov --codecov --output-path codecov.json
```
It wraps rustc's `-C instrument-coverage` (LLVM source-based coverage) and reports line and region coverage.

## Options worth knowing
| Flag | Use |
|---|---|
| `--nextest` | run via cargo-nextest (`cargo llvm-cov nextest`) |
| `--doctests` | include doc tests (nightly-only) |
| `--branch` | branch coverage (nightly-only, optional) |
| `--ignore-filename-regex 'generated|tests/'` | exclude files |
| `--fail-under-lines 80` | fail CI under a threshold |
| `--show-missing-lines` | list uncovered lines in the terminal |
| `-p crate` / `--exclude crate` | workspace member selection |

## Excluding code
```rust
#[cfg_attr(coverage_nightly, coverage(off))]
fn debug_only_helper() {}
```
with `#![cfg_attr(coverage_nightly, feature(coverage_attribute))]` at the crate root; cargo-llvm-cov
sets `cfg(coverage_nightly)` on nightly and `cfg(coverage)` always. Prefer excluding by file regex for
generated code; avoid sprinkling attributes to game the number.

## Coverage of binaries and integration runs
```bash
source <(cargo llvm-cov show-env --sh)   # sets RUSTFLAGS, LLVM_PROFILE_FILE...
cargo llvm-cov clean --workspace
cargo build
./target/debug/myapp e2e-scenario        # run as many times as needed
cargo test
cargo llvm-cov report --html
```

## CI (GitHub Actions)
```yaml
- run: rustup update stable
- uses: taiki-e/install-action@cargo-llvm-cov
- run: cargo llvm-cov --workspace --all-features --lcov --output-path lcov.info
- uses: codecov/codecov-action@v5
  with: { files: lcov.info }
```
With `--lcov` only line coverage reaches Codecov; use `--codecov` for region coverage.

## Gotchas
- Instrumentation changes RUSTFLAGS, so it rebuilds everything into `target/llvm-cov-target`.
- Build scripts are left out of the report unless you pass `--include-build-script`; proc-macro crates are supported.
- `--doctests` and `--branch` need a nightly toolchain.

## Verify
- [ ] HTML report highlights the expected untested branches.
- [ ] lcov uploaded in CI and visible on PRs.
- [ ] Coverage numbers stable between runs (no flaky tests skipping code).

## Checked

2026-10-25. Checked against the cargo-llvm-cov README on main (options list, show-env, CI examples). Confirmed: subcommands and flags `nextest`, `--doctests`, `--branch`, `--ignore-filename-regex`, `--fail-under-lines`, `--show-missing-lines`, `--codecov`, `--open`, `--include-build-script`; `show-env --sh`; `cfg(coverage)` always and `cfg(coverage_nightly)` on nightly; default artifact dir `target/llvm-cov-target`; `taiki-e/install-action@cargo-llvm-cov` and `codecov/codecov-action@v5`; proc-macro support. Wrong in the draft and fixed: the `--export-prefix` flag (not in the README; `--sh` is documented) and the claim that proc-macro crates are not instrumented. Removed unconfirmed comparisons and behaviours (tarpaulin, killed processes, monomorphisation).

Method: documentation only; no commands were run.
