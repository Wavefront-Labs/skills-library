---
id: computing-software.software-engineering.rust.editions-and-cargo-fix-migration
name: editions-and-cargo-fix-migration
category: computing-software
field: software-engineering
product: rust
tags: [rust, rust-modules-crates, rust-editions, editions, edition-2024, cargo-fix, migration]
level: practitioner
status: docs-checked
description: "Migrate a Rust crate between editions with cargo fix --edition, the order of steps, and what the automatic migration does not cover."
sources:
  - https://doc.rust-lang.org/edition-guide/editions/index.html
  - https://doc.rust-lang.org/edition-guide/editions/transitioning-an-existing-project-to-a-new-edition.html
  - https://doc.rust-lang.org/cargo/commands/cargo-fix.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Editions and cargo fix --edition

**Goal:** upgrade a crate to the next edition mechanically and safely.

Editions are opt-in per crate: each crate chooses its edition in `Cargo.toml` (`edition = "2024"`), a new crate from Cargo gets the newest stable edition, a missing `edition` key means 2015, and crates of different editions interoperate seamlessly. Changes are "skin deep": all code compiles to the same internal representation.

Steps from the Edition Guide:

```bash
cargo update            # newer dependency releases may fix proc-macro / build-script edition issues
cargo test              # optional green baseline; commit separately
cargo fix --edition     # rewrites code to be compatible with the next edition
# edit Cargo.toml: edition = "2024"
cargo test              # or cargo build, to verify
cargo fmt               # reformat with the new edition's style
```

`cargo fix` prints a warning for anything it cannot fix; fix those by hand. After switching, run `cargo fix` again without `--edition` to apply any new compiler suggestions. See `cargo fix --help` / the cargo-fix page for `--all-targets`, `--all-features` and `--workspace`.

## Gotchas
- The automatic migration does not update doctests, and build-time code generation or macros may need manual updates.
- Put formatting changes in their own commit so they can be ignored in `git blame`.
- Migrating to an unstable edition needs nightly: `cargo +nightly fix --edition`, `cargo-features = ["edition20xx"]` above `[package]`, then the edition key; migrations may be incomplete.
- Read the Edition Guide chapter for the target edition for its list of changes.

## Checked
2026-11-03. Confirmed against the Edition Guide pages "What are Editions?" and "Transitioning an existing project to a new edition" (steps, default edition 2015, interoperability, doctests, unstable-edition procedure) and the cargo-fix command page (flag names). Removed: the per-edition change lists, the 1.85 / rust-version / resolver claims, workspace inheritance and CI matrix advice, which those pages do not state.
Method: documentation only; no commands were run.
