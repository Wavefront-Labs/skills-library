---
id: computing-software.software-engineering.rust.rustfmt-configuration-and-ci-checks
name: rustfmt-configuration-and-ci-checks
category: computing-software
field: software-engineering
product: rust
tags: [rust, rust-tooling-quality, rust-rustfmt, rustfmt, formatting, rustfmt-toml]
level: practitioner
status: docs-checked
description: "Configure rustfmt with rustfmt.toml: stable vs unstable options, edition and style_edition, ignore patterns and the rustfmt::skip attribute."
sources:
  - https://github.com/rust-lang/rustfmt/blob/master/Configurations.md
  - https://doc.rust-lang.org/cargo/commands/cargo-fmt.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# rustfmt configuration

**Goal:** one canonical format, enforced automatically, with minimal config.

Create a TOML file named `rustfmt.toml` or `.rustfmt.toml` and place it in the project or any parent directory. Each option is stable or unstable: stable options always work; unstable options need a nightly toolchain and `unstable_features = true` in the file (or `--unstable-features` on the command line).

```toml
# rustfmt.toml
edition = "2021"            # stable; default "2015"; values 2015, 2018, 2021, 2024
style_edition = "2021"      # stable; recommended to set explicitly for consistent formatting
max_width = 100             # stable; default 100
newline_style = "Unix"      # stable; default "Auto"; Auto, Native, Unix, Windows
use_small_heuristics = "Default"   # stable; Default, Off, Max

# unstable, nightly rustfmt + unstable_features = true:
# unstable_features = true
# imports_granularity = "Module"      # Preserve (default), Crate, Module, Item, One
# group_imports = "StdExternalCrate"  # Preserve (default), StdExternalCrate, One
# format_code_in_doc_comments = true  # default false
# ignore = ["src/types.rs", "examples"]
```

- `ignore` skips files and directories matching `.gitignore`-style patterns (Unix `/` paths); `"!path"` re-allows a path; `ignore = ["/"]` ignores everything under the directory holding `rustfmt.toml`. It is not stable (tracking issue 3395).
- `cargo fmt` formats all bin and lib files of the current crate using rustfmt; it is an external command shipped as an optional toolchain component, so it may need installing. Use `cargo fmt --help` / `rustfmt --help` for the check-only flag to enforce formatting in CI.
- The `#![rustfmt::skip]` attribute (shown in the docs) opts code out of formatting.
- Defaults follow the Rust Style Guide.

## Gotchas
- Using unstable options requires every developer and CI to run a nightly rustfmt, or the formatting results differ.
- Pin `edition`/`style_edition` explicitly so toolchain upgrades do not reformat the tree.

## Checked
2026-11-03. Confirmed against rustfmt `Configurations.md` (config file names, stable/unstable rule, `edition`, `style_edition`, `max_width`, `newline_style`, `use_small_heuristics`, `imports_granularity`, `group_imports`, `format_code_in_doc_comments`, `ignore`, `rustfmt::skip` examples) and the cargo-fmt command page. Removed: the `--check` command lines and exit-code claims, `#![cfg_attr(rustfmt, rustfmt_skip)]`, rust-analyzer `extraArgs`, the 2024 style-edition change list, macro-body limitation and the claim that `ignore` is nightly-only beyond the tracking-issue note.
Method: documentation only; no commands were run.
