---
id: computing-software.web-development.dioxus.dioxus-html-streaming
name: dioxus-html-streaming
category: computing-software
field: web-development
product: dioxus
tags: [dioxus, fullstack, streaming, enable-out-of-order-streaming, commit-initial-chunk, serveconfig, head-elements, suspense]
level: advanced
status: docs-checked
description: "Enable out of order HTML streaming in Dioxus SSR with enable_out_of_order_streaming, and handle head elements and HTTP status codes around commit_initial_chunk."
sources:
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/essentials/fullstack/streaming.md
  - https://github.com/DioxusLabs/docsite/blob/main/packages/docs-router/src/doc_examples/streaming.rs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HTML streaming in Dioxus fullstack

Goal: improve time-to-first-byte by sending an initial page skeleton and filling in components as their data loads.

By default fullstack waits for all suspense boundaries to resolve before sending the page. With streaming, the server sends HTML chunks as each suspense boundary resolves. It is disabled by default because it adds slight overhead and complexity; it suits pages where most data is quick but some is slow (e.g. e-commerce).

## Enable it

```rust
pub fn main() {
    dioxus::LaunchBuilder::new()
        .with_cfg(server_only! {
            dioxus::server::ServeConfig::builder().enable_out_of_order_streaming()
        })
        .launch(app);
}
```

With a custom Axum server pass the config to `serve_dioxus_application`:

```rust
let router = axum::Router::new()
    .serve_dioxus_application(
        dioxus::server::ServeConfig::builder().enable_out_of_order_streaming(),
        app,
    )
    .into_make_service();
```

## Caveats stated by the docs

- SEO and no JS: all content is still in the HTML document, so search engines can index it, but it is not visible to users without JavaScript. To support those users, disable streaming.
- Head elements (`document::Link`, `document::Meta`, `document::Title`) can only render in the initial chunk that contains `<head>`. Elements outside it are rendered by the client after hydration, invisible to search engines and no-JS users. Put them above suspense boundaries when you can.
- The initial chunk is sent after `commit_initial_chunk` is first called. The `Router` calls it automatically once suspense boundaries above it resolve; without the router, call it yourself after blocking head elements render.
- Once the initial chunk is committed you can no longer change response headers or the HTTP status. A server function that returns a 404 `HttpError` sets the status only before that point, so errors inside a dedicated `SuspenseBoundary` below the router do not propagate to the response status.

```rust
fn Home() -> Element {
    rsx! {
        SuspenseBoundary {
            fallback: |_| rsx! { "loading..." },
            // Errors here won't propagate to the response headers
            Post { id: 123 }
        }
    }
}
```

## Checked
Checked 2026-11-07 against the 0.7 Streaming page and the streaming.rs snippet file (both read in full). Confirmed: default behaviour, enable_out_of_order_streaming via with_cfg and serve_dioxus_application, SEO and no-JS caveat, head element rule, commit_initial_chunk and Router behaviour, status code limit and the SuspenseBoundary example. Nothing removed.
Method: documentation only; no commands were run.
