---
id: computing-software.software-engineering.rust.publishing-crates-and-semver-checks
name: publishing-crates-and-semver-checks
category: computing-software
field: software-engineering
product: rust
tags: [rust, cargo, crates-io, cargo-publish, cargo-semver-checks, semver, msrv, trusted-publishing, rust-semver, rust-msrv]
level: practitioner
status: docs-checked
description: "Publish Rust crates to crates.io: required metadata, package contents, dry runs, semver compatibility checks, MSRV policy, yanking and automated release tooling."
sources:
  - https://doc.rust-lang.org/cargo/reference/publishing.html
  - https://doc.rust-lang.org/cargo/reference/semver.html
  - https://github.com/obi1kenobi/cargo-semver-checks
  - https://crates.io/docs/trusted-publishing
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Publishing crates and semver checks

**Goal:** releases that downstream users can upgrade without breakage, with correct metadata and only intended files.

## 1. Metadata
```toml
[package]
name = "acme-money"
version = "1.3.0"
edition = "2024"
rust-version = "1.80"               # MSRV; cargo reports an error on older toolchains
description = "Exact money arithmetic with currencies"
license = "MIT OR Apache-2.0"
repository = "https://github.com/acme/money"
documentation = "https://docs.rs/acme-money"
readme = "README.md"
keywords = ["money", "currency", "decimal"]   # max 5
categories = ["finance"]
include = ["src/**", "Cargo.toml", "README.md", "LICENSE-*"]
```

## 2. Check what ships, then publish
```bash
cargo package --list           # files in the .crate
cargo publish --dry-run        # builds the packaged crate in isolation (catches missing files, path deps)
cargo publish
```
Path dependencies need a `version` and must be published first. Workspaces: `cargo publish --workspace` (1.90+) publishes members in dependency order.

## 3. Semver rules (Cargo's interpretation)
- `1.x.y`: minor = additive, patch = fixes. `0.x.y`: the minor is the breaking component (`0.4` -> `0.5` is breaking).
- Breaking (needs major): removing/renaming public items, adding a required trait method, adding fields to an exhaustive public struct, adding variants to a non-`#[non_exhaustive]` public enum, tightening generic bounds. The Cargo SemVer reference lists every case.
- Pre-empt future breakage: `#[non_exhaustive]` on public enums/structs that will grow, private fields, sealed traits.
- MSRV bumps: the Cargo SemVer guide does not treat raising the MSRV as a major change; state your policy in the README and set `rust-version`.

## 4. cargo-semver-checks
```bash
cargo install cargo-semver-checks --locked
cargo semver-checks                    # compares against the latest crates.io release
cargo semver-checks --baseline-rev v1.2.0
```
Run in CI on PRs. It looks up the previous version on crates.io by default and does not catch every breaking change.

## 5. Automation and auth
- release-plz or cargo-release can automate version bumps and publishing.
- crates.io trusted publishing from GitHub Actions uses `rust-lang/crates-io-auth-action` to obtain a temporary token that is revoked when the job ends, avoiding long-lived tokens; otherwise use scoped tokens.

## 6. Mistakes
- `cargo yank --version 1.3.0` prevents new lockfiles from selecting it; existing lockfiles still work. Publish 1.3.1 with the fix; you cannot delete or overwrite versions.

## Gotchas
- Re-exported dependency types make that dependency's major version part of your public API; bumping it is breaking for you.
- Removing a Cargo feature is a major change, and so is switching from `no_std` support to requiring `std`.

## Verify
- `cargo publish --dry-run` and `cargo semver-checks` pass in CI on the release PR, and `cargo +<msrv> check` succeeds.

## Checked

2026-10-25. Checked against the Cargo Book (publishing: `cargo package --list`, `cargo publish --dry-run`, `cargo yank --version`, yank does not delete code; manifest: at most 5 keywords and 5 categories, `rust-version`, `path` plus `version` dependencies; SemVer reference: 0.y.z rules, new enum variants without `non_exhaustive`, feature removal, no_std to std; MSRV not a major change), the Cargo 1.90 changelog (`cargo publish --workspace`), the cargo-semver-checks README (`--baseline-rev`, crates.io baseline by default), the crates.io category list (`finance` exists) and the crates-io-auth-action README (temporary token, revoked on job completion). Removed unconfirmed claims (default-feature and no_std remark, crate-name policy, tool descriptions).

Method: documentation only; no commands were run.
