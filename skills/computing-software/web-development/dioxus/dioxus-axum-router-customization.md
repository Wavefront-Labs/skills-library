---
id: computing-software.web-development.dioxus.dioxus-axum-router-customization
name: dioxus-axum-router-customization
category: computing-software
field: web-development
product: dioxus
tags: [dioxus, fullstack, axum, dioxus-serve, server-router, extension, lazy, layers]
level: practitioner
status: docs-checked
description: "Customize the Axum router in Dioxus fullstack with dioxus::serve and dioxus::server::router: add routes, layers, Extension state, and Lazy<T> global resources."
sources:
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/essentials/fullstack/axum.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Customize the Axum router in Dioxus fullstack

Goal: take control of the server with `dioxus::serve` while keeping SSR, assets and server functions.

`dioxus::launch` starts a default Axum server. For more control use `dioxus::serve`, usually gated on the `server` feature:

```rust
fn main() {
    #[cfg(feature = "server")]
    dioxus::serve(|| async move {
        let mut router = dioxus::server::router(app);
        // .. customize the router, adding layers and new routes
        Ok(router)
    });

    #[cfg(not(feature = "server"))]
    dioxus::launch(app);
}
```

`dioxus::server::router` sets up static assets (the `public` directory, index.html and assets), SSR with hydration data, and server function endpoints. The same effect manually, via `DioxusRouterExt`: `.register_server_functions()`, `.serve_static_assets()` and a `.fallback(get(render_handler)...)`. To register a subset, iterate `ServerFunction::collect()` and call `func.register_server_fn_on_router(router)`.

## Add routes

```rust
let router = dioxus::server::router(app)
    .route("/submit", post(|| async { "Form submitted!" }))
    .route("/about", get(|| async { "About us" }));
```

The SSR handler is a fallback, so routes you register take priority over the Dioxus app. Handlers accept the usual Axum modifiers (`.with_state()`, `.layer()`).

## Extensions as shared state

```rust
let router = dioxus::server::router(app)
    .layer(Extension(broadcast::channel::<String>(16).0));

#[post("/api/broadcast", ext: Extension<broadcast::Sender<String>>)]
async fn broadcast_message() -> Result<()> { ext.send("New broadcast message".to_string())?; Ok(()) }
```

For per-request state, add a `middleware::from_fn` layer that inserts into `req.extensions_mut()`.

## Lazy<T> global state

Without a custom `serve`, declare a static `Lazy<T>` to hold async-initialized resources:

```rust
static DATABASE: Lazy<sqlx::SqlitePool> = Lazy::new(|| async move {
    dioxus::Ok(SqlitePoolOptions::new().max_connections(5)
        .connect_with("sqlite::memory:".parse().unwrap()).await?)
});
```

Accessing `DATABASE` blocks the current thread until the initializer finishes, so you can use it synchronously; it implements `Deref<Target = T>`. For simple synchronous data the standard `LazyLock` also works (e.g. `LazyLock<Mutex<Vec<String>>>`).

## Checked
Checked 2026-11-07 against the 0.7 Axum Router page (read in full; its code is inline). Confirmed: dioxus::serve with the server feature gate, what dioxus::server::router sets up, DioxusRouterExt methods, ServerFunction::collect(), added routes taking priority over the SSR fallback, Extension layers and middleware::from_fn, Lazy<T> and LazyLock. Nothing removed.
Method: documentation only; no commands were run.
