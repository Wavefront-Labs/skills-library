---
id: computing-software.web-development.leptos.cargo-leptos-ssr-project-setup
name: cargo-leptos-ssr-project-setup
category: computing-software
field: web-development
product: leptos
tags: [leptos, rust, cargo-leptos, ssr, setup, axum, actix]
level: practitioner
status: docs-checked
description: "Install cargo-leptos, add the wasm32 target, scaffold an Axum or Actix SSR template and run cargo leptos watch on localhost:3000."
sources: [https://book.leptos.dev/ssr/21_cargo_leptos.html, https://book.leptos.dev/ssr/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: start a server-rendered Leptos project.

## Why
SSR needs two binaries: one native (the server) and one compiled to WebAssembly (the browser), and the server must serve the WASM plus its JS initialiser. `cargo-leptos` coordinates this, rebuilds both halves on change, and has built-in support for Tailwind, SASS and testing. Trunk is what the CSR chapters used.

## Method
```bash
cargo install --locked cargo-leptos

# Actix template
cargo leptos new --git https://github.com/leptos-rs/start-actix
# or Axum template
cargo leptos new --git https://github.com/leptos-rs/start-axum

rustup target add wasm32-unknown-unknown

cd <your-project>
cargo leptos watch
```
When it has compiled, open `http://localhost:3000`.

## Choosing a server
Official integrations are Actix and Axum and expose the full feature set; the Leptos team defaults to Axum for new projects and the book recommends either for beginners. Community integrations (WinterCG runtimes such as Deno or Cloudflare, Spin, Viz, Pavex) may support less; check their docs. Writing your own integration is not recommended for beginners.

## Gotchas
- Without the `wasm32-unknown-unknown` target Rust cannot build the browser half.
- More features are in the cargo-leptos README, which this page only links.
- Related: `computing-software.web-development.leptos.ssr-page-load-lifecycle`.

## Checked

2026-11-07: every claim, snippet and step above was compared with the full text of the cited Leptos book pages (https://book.leptos.dev/ssr/21_cargo_leptos.html, https://book.leptos.dev/ssr/) and the book source on GitHub. Statements the pages do not state were removed or trimmed.

Method: documentation only; no commands were run.
