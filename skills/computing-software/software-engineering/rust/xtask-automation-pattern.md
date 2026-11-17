---
id: computing-software.software-engineering.rust.xtask-automation-pattern
name: xtask-automation-pattern
category: computing-software
field: software-engineering
product: rust
tags: [rust, rust-cargo-build, rust-xtask, xtask, automation, build-scripts, workspace]
level: practitioner
status: docs-checked
description: "Replace Makefiles and shell scripts with an xtask crate: a workspace binary invoked through a cargo alias for codegen, release and CI tasks."
sources:
  - https://github.com/matklad/cargo-xtask
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# xtask automation pattern

**Goal:** project tasks written in Rust, cross-platform, no extra tools.

Layout:

```text
Cargo.toml          # [workspace] members = ["crates/*", "xtask"]
.cargo/config.toml  # [alias] xtask = "run --package xtask --"
xtask/Cargo.toml
xtask/src/main.rs
```

```rust
fn main() -> anyhow::Result<()> {
    let task = std::env::args().nth(1);
    match task.as_deref() {
        Some("dist") => dist(),
        Some("ci")   => { cmd("cargo", &["fmt", "--check"])?; cmd("cargo", &["clippy", "--all-targets", "--", "-D", "warnings"])?; cmd("cargo", &["test", "--workspace"]) }
        _ => { eprintln!("tasks: dist, ci"); std::process::exit(2) }
    }
}
fn cmd(prog: &str, args: &[&str]) -> anyhow::Result<()> {
    let status = std::process::Command::new(prog).args(args).status()?;
    anyhow::ensure!(status.success(), "{prog} {args:?} failed");
    Ok(())
}
```

Run with `cargo xtask ci`. The binary should expect a task name as its first positional argument; tasks can use any crates.io crate and can run `cargo` (use the `CARGO` environment variable to get the right `cargo`). Define tasks as subcommands of the single `xtask` binary (the alternative is a separate binary and alias per task). Commit the `xtask` directory and `.cargo/config.toml`. Helper libraries: `xshell` (ergonomic "bash" scripting in Rust), `duct` (child processes with pipelines and IO redirection).

When to use something else: if `cargo build` and `cargo test` are enough, skip xtasks; a short bash script is fine if you do not need to support Windows. xtasks are not an officially recommended cargo workflow, but a common pattern (cargo itself uses it).

## Gotchas
- The xtask crate compiles on first use; keep its compile time small.
- xtasks do not hook into the cargo lifecycle: to post-process `cargo build`, define `cargo xtask build` that calls `cargo build`. They are project-local, not usable from dependencies.
- If `xtask` is not a workspace member, the `cargo xtask` alias works only from the project root (the workspace layout is usually better and lets you share dependencies).

## Verify
`cargo xtask ci` works from a clean checkout, with no tools beyond `cargo` and `rustc`.

## Checked
2026-11-08. Read in full: cargo-xtask README (matklad/cargo-xtask, raw README). Confirmed: alias, layout, workspace membership, subcommand convention, CARGO variable, limitations, xshell and duct, when not to use. Removed (not on the page): the `--quiet` alias flag, `publish = false`, CARGO_MANIFEST_DIR advice, clap, just/make and build.rs guidance, Windows npm.cmd and default-members tips, the cargo config alias source.
Method: documentation only; no commands were run.
