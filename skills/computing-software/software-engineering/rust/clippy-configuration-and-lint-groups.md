---
id: computing-software.software-engineering.rust.clippy-configuration-and-lint-groups
name: clippy-configuration-and-lint-groups
category: computing-software
field: software-engineering
product: rust
tags: [rust, rust-tooling-quality, rust-clippy, clippy, lints, clippy-toml, workspace-lints]
level: practitioner
status: docs-checked
description: "Configure Clippy lint groups in Cargo.toml [lints], clippy.toml values, lint attributes with reasons, and command-line flags."
sources:
  - https://doc.rust-lang.org/clippy/configuration.html
  - https://doc.rust-lang.org/clippy/lints.html
  - https://doc.rust-lang.org/cargo/reference/manifest.html
  - https://doc.rust-lang.org/reference/attributes/diagnostics.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Clippy configuration and lint groups

**Goal:** a strict, stable lint policy that does not churn with every toolchain release.

## Groups
`clippy::correctness` is the only group whose lints are deny-by-default and abort compilation. `suspicious`, `complexity`, `perf` and `style` are warn-by-default (`clippy::all` is the set of warn-by-default lints). Opt-in groups: `pedantic` (aggressive, prone to false positives; cherry-picking is suggested), `restriction` (not recommended wholesale; Clippy warns if it finds `#![warn(clippy::restriction)]`), `nursery` (buggy or needs more work; cherry-pick) and `cargo` (suggestions for `Cargo.toml`).

## Setting levels
Three ways, per the Clippy configuration page:
1. Attributes: `#![warn(clippy::all, clippy::pedantic)]`, `#![deny(clippy::single_match)]`, or `#[allow(...)]` limited to a function or module. `allow` suppresses, `warn` warns, `deny` errors (exit with an error code, useful in CI).
2. Command line: `cargo clippy -- -A clippy::lint_name`, `-W clippy::pedantic`, `-A clippy::all -W clippy::useless_format`.
3. The `[lints]` section of `Cargo.toml`:

```toml
[lints.rust]
unsafe_code = "forbid"

[lints.clippy]
enum_glob_use = "deny"
pedantic = { level = "warn", priority = -1 }   # lower priority: overridden by higher numbers
```

Cargo's `[lints]` section is "respected as of 1.74"; the table is the part of the lint name before `::` (no `::` means `rust`). Cargo applies it only to the current package, not dependencies. In a workspace, define `[workspace.lints.*]` and have members opt in with `[lints] workspace = true`.

## clippy.toml
Looked up as `clippy.toml` or `.clippy.toml` in the directory named by `CLIPPY_CONF_DIR`, else `CARGO_MANIFEST_DIR`, else the current directory, then walking up parent directories. The page notes the file is unstable and may be deprecated. Simple `variable = value` mapping; list options such as `disallowed-names` can extend the defaults with the value `".."`. Options documented on the Lint Configuration page include `msrv` (disables lints for newer features), `cognitive-complexity-threshold`, `too-many-arguments-threshold`, `disallowed-methods` and `allow-unwrap-in-tests`.

## Local exceptions
All lint attributes accept `reason = "..."` (shown with the lint message when it fires). `#[expect(lint)]` suppresses the lint and issues a warning if the expectation is unfulfilled. `forbid` disallows later `allow`/`expect`.

## Checked
2026-11-03. Confirmed against the Clippy docs (Configuring Clippy, Lints, Lint Configuration option names), the Cargo manifest `[lints]` section and workspaces page, and the Rust Reference diagnostics attributes (reason, expect). Removed: the CI one-liner and `-D warnings` claims, rust-toolchain.toml advice, specific lint-by-name claims (`unwrap_used`, `dbg_macro`, `todo`, `module_name_repetitions`, `len_zero`, `needless_*`), the `set_var` "racy" example, the `reason` stabilisation version (1.81), and the `clippy --fix` remark.
Method: documentation only; no commands were run.
