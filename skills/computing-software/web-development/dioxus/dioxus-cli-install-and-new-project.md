---
id: computing-software.web-development.dioxus.dioxus-cli-install-and-new-project
name: dioxus-cli-install-and-new-project
category: computing-software
field: web-development
product: dioxus
tags: [dioxus, dx, dioxus-cli, cargo-binstall, dx-new, dx-serve, dx-doctor, wasm32-unknown-unknown]
level: intro
status: docs-checked
description: "Install the Dioxus CLI (dx), scaffold a project with dx new, add the wasm target, and run dx serve; covers the template prompts, Cargo features and files the template creates."
sources:
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/guides/tools/index.md
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/guides/tools/creating.md
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/tutorial/new_app.md
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/tutorial/tooling.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Install dx and create a Dioxus project

Goal: get the `dx` CLI, scaffold an app and serve it.

## Install
```bash
cargo binstall dioxus-cli     # prebuilt binary (Windows, macOS, Linux)
cargo install dioxus-cli      # fallback if no cargo-binstall or no prebuilt binary
dx --help                     # overview of commands
dx --version                  # check it matches the guide
dx doctor                     # diagnose installed tools and system config
```
Commands listed by `dx --help`: new, serve, bundle, build, run, init, doctor, print, translate, fmt, check, config, self-update, tools, components. Global options: `--verbose`, `--trace`, `--json-output`, `--log-to-file`, `--locked`, `--offline`, `--frozen`.

Checklist before starting: Rust and Cargo, the wasm32-unknown-unknown target, an up-to-date dioxus-cli, and system-specific dependencies.

## Create and run
```bash
dx new hot_dog                                   # follow the prompts
dx new --template gh:dioxuslabs/dioxus-template  # use a different template
rustup target add wasm32-unknown-unknown         # WASM target must be installed
cd hot_dog
dx serve
```
`dx new` clones the dioxus-template repository. `dx serve` prints the address it serves on (the tutorial shows http://127.0.0.1:8080) plus code warnings.

Template choices: Bare-bones (main.rs plus an assets folder), Jumpstart (components, views, suggested structure), Workspace (cargo workspace with a crate per platform). The tutorial answers: fullstack false, router false, TailwindCSS true, LLM prompts false, default platform Web.

## What you get
Cargo.toml, Dioxus.toml (bundling and deploy config), README.md, assets/ (favicon.ico, header.svg, main.css), src/main.rs. Dioxus dependency: `dioxus = { version = "0.7.0" }`. Template features:
```toml
[features]
default = ["web"]
web = ["dioxus/web"]
desktop = ["dioxus/desktop"]
mobile = ["dioxus/mobile"]
```
`dx serve --desktop` makes dx call `cargo build --no-default-features --features desktop`.

## Gotchas
- `dx new` is optional: Dioxus apps are ordinary Rust projects and can be built with cargo.
- If a `tailwind.css` exists at the app root, dx runs the TailwindCSS CLI automatically when serving and building.

## Checked
Checked 2026-11-07 against the 0.7 Tools page, Create a Project page, new_app tutorial page and tooling tutorial page (all read in full). Confirmed: binstall and cargo install, command list and global options, template choices and tutorial answers, files created, features block, dx serve --desktop cargo call, tailwind.css detection. Nothing removed.
Method: documentation only; no commands were run.
