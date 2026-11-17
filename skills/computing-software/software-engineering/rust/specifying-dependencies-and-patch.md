---
id: computing-software.software-engineering.rust.specifying-dependencies-and-patch
name: specifying-dependencies-and-patch
category: computing-software
field: software-engineering
product: rust
tags: [rust, cargo-dependencies, cargo-patch, cargo-toml, version-requirements, git-dependencies, path-dependencies, cargo-tree]
level: practitioner
status: docs-checked
description: "Declare Cargo dependencies precisely: caret/tilde/exact requirements, git and path deps, renames, optional and target-specific deps, [patch] overrides, and cargo tree."
sources: ["https://doc.rust-lang.org/cargo/reference/specifying-dependencies.html", "https://doc.rust-lang.org/cargo/reference/overriding-dependencies.html", "https://doc.rust-lang.org/cargo/commands/cargo-tree.html", "https://doc.rust-lang.org/cargo/reference/resolver.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Specifying dependencies and [patch]

**Goal:** dependency declarations that resolve predictably, and a clean way to test a fix in a
dependency without forking your whole tree.

## Version requirements
| Written | Means |
|---|---|
| `serde = "1.0.200"` | caret: `>=1.0.200, <2.0.0` (default) |
| `"0.4.3"` | caret on 0.x: `>=0.4.3, <0.5.0` (minor is breaking below 1.0) |
| `"~1.4.2"` | `>=1.4.2, <1.5.0` |
| `"=1.4.2"` | exact (avoid in libraries; it causes unresolvable conflicts) |
| `">=1.2, <1.5"` | range |
Write the **lowest version you actually need** (the features you use), not the latest; `Cargo.lock`
pins what you build with. `cargo update serde --precise 1.0.210` adjusts the lock.
The nightly `-Z direct-minimal-versions` flag tests that your lower bounds are real (Cargo advises against plain `-Z minimal-versions`, because many transitive dependencies lack correct lower bounds).

## Other sources
```toml
[dependencies]
mylib = { path = "../mylib", version = "0.3" }          # version used when published
fork  = { git = "https://github.com/org/fork", branch = "fix-x" }   # or tag = / rev =
json  = { package = "serde_json", version = "1" }       # rename
tokio = { version = "1", default-features = false, features = ["rt", "macros"] }
heavy = { version = "2", optional = true }              # becomes feature "heavy"

[target.'cfg(windows)'.dependencies]
windows-sys = { version = "0.59", features = ["Win32_Foundation"] }

[dev-dependencies]
proptest = "1"

[build-dependencies]
cc = "1"
```
- Crates.io rejects packages with git-only dependencies; path deps need a `version` to publish.
- Pin git deps with `rev =` for reproducibility; `Cargo.lock` records the commit anyway.
- `[workspace.dependencies]` + `dep = { workspace = true }` keeps versions in one place.

## [patch]: override a dependency everywhere in the graph
```toml
[patch.crates-io]
hyper = { git = "https://github.com/me/hyper", branch = "fix-1234" }
# or a local checkout (use one entry, not both):
# hyper = { path = "../hyper" }
```
- Applies to every crate depending on `hyper` from crates.io, including transitive ones, as long as
  the patched version satisfies their requirements (same semver-compatible version).
- Only honoured in the **root** workspace's Cargo.toml; patches in dependencies are ignored.
- Run `cargo update hyper` after adding. The version number of the patched source matters, because the resolver merges it with the versions on crates.io; check the version in the fork's Cargo.toml if the patch is not picked up.
- `[patch."https://github.com/org/repo"]` patches git sources.
- Remove the patch once upstream releases; it is a temporary measure. `[replace]` is deprecated.

## Inspecting the graph
```bash
cargo tree -i hyper                 # who depends on hyper (inverted)
cargo tree -d                       # duplicate versions of the same crate
cargo tree -e features -i serde     # which features are enabled and by whom
cargo update --dry-run --verbose    # see what would change
```
Duplicate major versions (two `syn`s) cost compile time; resolve by upgrading the laggard.

## Resolver
Edition 2021 uses resolver "2" (features of build/dev/target deps are not unified with normal deps).
Resolver "3" (Rust 1.84+, default in edition 2024) changes `resolver.incompatible-rust-versions` from `allow` to `fallback`, so the resolver prefers dependency versions compatible with your `rust-version`.
versions compatible with your `rust-version`. Virtual workspaces must set `resolver` explicitly.

## Verify
- [ ] `cargo tree -d` shows no avoidable duplicates.
- [ ] Every `[patch]` has an issue/PR link comment and is removed after upstream release.
- [ ] `cargo publish --dry-run` succeeds for published crates (no git-only deps).

## Checked

2026-10-25. Checked against the Cargo Book (specifying dependencies: caret and tilde requirements, git and path sources, crates.io rejects dependencies outside crates.io; overriding dependencies: `[patch]` root-only, version of the patched source is significant, `[replace]` deprecated; resolver versions 2 and 3 and the 1.84 requirement; unstable `minimal-versions` and `direct-minimal-versions`) and the cargo-update and cargo-tree manual pages (`--precise`, `--dry-run`, `-i`, `-d`, `-e`). Fixed an unfinished sentence in the Resolver section; `cargo update -p` is no longer shown in the manual, so the commands use the package-name form. Removed the unconfirmed `dep:` aside and the quoted warning text.

Method: documentation only; no commands were run.
