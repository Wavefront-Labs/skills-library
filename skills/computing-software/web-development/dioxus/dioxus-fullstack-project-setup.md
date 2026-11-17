---
id: computing-software.web-development.dioxus.dioxus-fullstack-project-setup
name: dioxus-fullstack-project-setup
category: computing-software
field: web-development
product: dioxus
tags: [dioxus, fullstack, dx-serve, cargo-features, server-feature, client-server-split, optional-dependencies]
level: practitioner
status: docs-checked
description: "Configure a Dioxus fullstack Cargo.toml: server and web features, dx serve with @client and @server, build profiles, and optional server-only or client-only dependencies."
sources:
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/essentials/fullstack/project_setup.md
  - https://github.com/DioxusLabs/docsite/blob/main/packages/docs-router/src/doc_examples/server_tokio_import.rs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Set up a Dioxus fullstack project (features and dependencies)

Goal: build a client binary and a server binary from one crate with DX.

A fullstack app is at least two binaries: the client (web, desktop or mobile) and the server (renders initial HTML and runs server functions). Treat the server as another platform. `dx new` with fullstack generates the flags below; from scratch you add them yourself.

```toml
[dependencies]
dioxus = { version = "0.7", features = ["fullstack"] }

[features]
web = ["dioxus/web"]
server = ["dioxus/server"]
# desktop = ["dioxus/desktop"]   mobile = ["dioxus/mobile"]
```

DX detects a server variant by looking for a Cargo feature named `server`. With `fullstack` enabled it splits your command into two `cargo build` commands, one per platform. Platform flags (`--web`, `--desktop`, `--ios`) enable the matching feature. Examples from the docs:

```sh
dx serve --features "spicy" --release
dx serve --example dogs
dx serve --web        # target wasm32-unknown-unknown, features="web", profile="wasm-dev"
dx serve --desktop    # features="desktop", profile="desktop-dev"
```

## Per-target args

```sh
dx serve @client --ios --features "optimizations" @server --bin server
dx serve @client --bin dog-app @server --bin pet-api   # workspace with a dedicated server crate
```

Profiles used: web-dev/web-release, server-dev/server-release, desktop-dev/desktop-release, ios-dev/ios-release, android-dev/android-release. `--hotpatch` hot-reloads both client and server.

## Server-only and client-only dependencies

Crates like tokio cannot compile to WebAssembly; a required `tokio` with the full feature set breaks the web build with cryptic errors. Make it optional and enable it from the server feature:

```toml
tokio = { version = "1", features = ["full"], optional = true }
server = ["dioxus/server", "dep:tokio"]
web-sys = { version = "0.3.60", features = ["console"], optional = true }
web = ["dioxus/web", "dep:web-sys"]
```

Then gate imports and uses with `#[cfg(feature = "server")]` (or put them in a module with that attribute). Server function bodies already compile only with the server feature.

## Checked
Checked 2026-11-07 against the 0.7 Project Setup page and the server_tokio_import.rs snippet file (both read in full). Confirmed: server feature detection, platform flags enabling features, the two-build split, @client and @server, the profile list, --hotpatch for client and server, optional tokio and web-sys with dep: features, cfg gating and server function bodies. Nothing removed.
Method: documentation only; no commands were run.
