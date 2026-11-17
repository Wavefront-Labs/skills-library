---
id: computing-software.web-development.dioxus.dioxus-fullstack-middleware-auth
name: dioxus-fullstack-middleware-auth
category: computing-software
field: web-development
product: dioxus
tags: [dioxus, fullstack, middleware, tower-http, authentication, sessions, cache-control, axum-session-auth]
level: practitioner
status: docs-checked
description: "Add middleware to Dioxus fullstack via router layers or #[middleware], wire session auth with a layer and server function extractor, and avoid cache busting."
sources:
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/essentials/fullstack/middleware.md
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/essentials/fullstack/authentication.md
  - https://github.com/DioxusLabs/docsite/blob/main/packages/docs-router/src/doc_examples/server_function_middleware.rs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Middleware and authentication in Dioxus fullstack

Goal: run code before and after requests, and attach sessions for auth.

Dioxus adds no bespoke middleware wrappers; it uses Axum, which leans on `tower` and `tower-http`. Two approaches: imperatively on the router in `dioxus::serve`, or declaratively per endpoint with `#[middleware]`.

## Router-level

```rust
dioxus::serve(|| async move {
    use axum::{extract::Request, middleware::Next};
    use dioxus::server::axum;
    Ok(dioxus::server::router(app)
        .layer(axum::middleware::from_fn(|request: Request, next: Next| async move {
            println!("Request: {} {}", request.method(), request.uri().path());
            let res = next.run(request).await;
            println!("Response: {}", res.status());
            res
        })))
});
```

For many layers (tower-http: `TraceLayer`, `CompressionLayer`, `SetSensitiveRequestHeadersLayer`, `ValidateRequestHeaderLayer`...) assemble a `ServiceBuilder` and pass it to `.layer(middleware)`; Axum recommends this for performance.

## Per-endpoint

```rust
#[post("/api/timeout")]
#[middleware(TimeoutLayer::new(Duration::from_secs(1)))]
pub async fn timeout() -> Result<(), ServerFnError> { /* sleeps 2s */ Ok(()) }
```

## Caching gotcha

Middleware can bust the cache, even accidentally. If a caching layer sets `Cache-Control` for `/home` and you later add a session layer, a logged-in user's page might be cached. Cache by URL is unsafe when content varies by headers (auth/session); configure your reverse proxy or write a smarter caching middleware.

## Authentication

Dioxus has no built-in auth. Sessions are usually inserted by a middleware (or a library such as `axum_session_auth` added with `.layer(AuthLayer::new(...))` and `.layer(SessionLayer::new(...))`), then read in server functions through a server-only extractor:

```rust
#[post("/api/user/login", auth: auth::Session)]
pub async fn login() -> Result<()> { auth.login_user(2); Ok(()) }

#[post("/api/user/logout", auth: auth::Session)]
pub async fn logout() -> Result<()> { auth.logout_user(); Ok(()) }
```

Authentication verifies who the user is; authorization then checks they may perform the action. Third-party services (e.g. Supabase, Firebase) are an alternative; the docs recommend none.

## Checked
Checked 2026-11-07 against the 0.7 Middleware and Authentication pages and the server_function_middleware.rs snippet file (all read in full). Confirmed: dioxus::serve router layers, from_fn, ServiceBuilder advice, #[middleware] with TimeoutLayer, Cache-Control busting caveat, axum_session_auth layers, auth::Session extractor login and logout, no built-in auth, no recommended third-party service. Nothing removed.
Method: documentation only; no commands were run.
