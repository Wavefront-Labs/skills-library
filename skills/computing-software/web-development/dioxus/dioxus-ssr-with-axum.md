---
id: computing-software.web-development.dioxus.dioxus-ssr-with-axum
name: dioxus-ssr-with-axum
category: computing-software
field: web-development
product: dioxus
tags: [dioxus, dioxus-ssr, ssr, axum, render-element, virtualdom, rebuild-in-place, render]
level: advanced
status: docs-checked
description: "Render Dioxus to HTML in an Axum handler with dioxus-ssr: render_element for rsx, or VirtualDom with rebuild_in_place; VirtualDom is not Send."
sources:
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/guides/utilities/ssr.md
  - https://github.com/DioxusLabs/docsite/blob/main/packages/docs-router/src/doc_examples/ssr.rs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Server-side rendering with dioxus-ssr and Axum

Goal: lower-level control than dioxus-fullstack, for web frameworks it does not support or for pre-rendering pages.

## Setup
```sh
cargo new --bin demo
cd demo
cargo add dioxus
cargo add dioxus-ssr
cargo add tokio --features full
cargo add axum
```
Run with `cargo run` rather than `dx serve`.

## Server
```rust
use axum::{response::Html, routing::get, Router};
use dioxus::prelude::*;

#[tokio::main]
async fn main() {
    let listener = tokio::net::TcpListener::bind("127.0.0.1:3000").await.unwrap();
    println!("listening on http://127.0.0.1:3000");
    axum::serve(listener, Router::new().route("/", get(app_endpoint)).into_make_service())
        .await
        .unwrap();
}
```

## Endpoint option 1: render rsx directly
```rust
async fn app_endpoint() -> Html<String> {
    Html(dioxus_ssr::render_element(rsx! { div { "hello world!" } }))
}
```

## Endpoint option 2: render a VirtualDom
```rust
async fn app_endpoint() -> Html<String> {
    fn app() -> Element {
        rsx! { div { "hello world" } }
    }
    let mut app = VirtualDom::new(app);
    // rebuild the VirtualDom before rendering
    app.rebuild_in_place();
    Html(dioxus_ssr::render(&app))
}
```

## Gotcha: VirtualDom is not Send
It uses interior mutability that is not thread-safe, so you cannot hold a VirtualDom across an await point; render it to a String immediately. For retained-state SSR (essentially LiveView), spawn the VirtualDom on its own thread and communicate via channels, or keep a pool of VirtualDoms.

## Checked

2026-11-08. Confirmed against the dioxus-ssr guide (read in full) and its ssr.rs example file: cargo add steps, Axum server, render_element, VirtualDom with rebuild_in_place and render, run with cargo run rather than dx serve, and VirtualDom not being Send. Removed the claim about the roadmap page, which was not read.

Method: documentation only; no commands were run.
