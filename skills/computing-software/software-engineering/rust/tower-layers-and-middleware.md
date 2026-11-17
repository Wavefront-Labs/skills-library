---
id: computing-software.software-engineering.rust.tower-layers-and-middleware
name: tower-layers-and-middleware
category: computing-software
field: software-engineering
product: rust
tags: [rust, rust-web-services, rust-tower, tower, middleware, layer, service, tower-http]
level: advanced
status: docs-checked
description: "Compose tower Services and Layers (timeout, tracing, compression) for axum, and write custom middleware with from_fn, with correct layer ordering."
sources:
  - https://docs.rs/tower
  - https://docs.rs/tower-http
  - https://docs.rs/axum/latest/axum/middleware/index.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# tower layers and middleware

**Goal:** cross-cutting behaviour (timeouts, tracing, auth) applied uniformly to a service stack.

A `tower::Service` is an asynchronous function from a request to a response; a `Layer` decorates a service, transforming the request or the response. `ServiceBuilder` composes several layers. Tower's feature-gated modules include `timeout`, `retry`, `hedge`, `balance`, `buffer`, `filter` and `steer`; enable only what you use, for example `features = ["retry", "timeout"]`.

```rust
use tower::ServiceBuilder;
use tower_http::{trace::TraceLayer, compression::CompressionLayer};

let app = Router::new().route("/", get(root)).layer(
    ServiceBuilder::new()                         // layers run top to bottom
        .layer(TraceLayer::new_for_http())
        .layer(CompressionLayer::new()),
);

// custom async middleware, simplest form
async fn auth(req: Request, next: Next) -> Result<Response, StatusCode> {
    match req.headers().get(AUTHORIZATION) {
        Some(h) if valid(h) => Ok(next.run(req).await),
        _ => Err(StatusCode::UNAUTHORIZED),
    }
}
let app = app.route_layer(axum::middleware::from_fn(auth));
```

tower-http supplies `TraceLayer`, `CompressionLayer`/`DecompressionLayer` and request-id layers (`RequestIdLayer`, `PropagateRequestIdLayer`) and a `TimeoutLayer`, as listed in axum's middleware docs. `Router::layer` and `Router::route_layer` apply to whole routers, `MethodRouter::layer`/`route_layer` to method routers. axum recommends `ServiceBuilder` over repeated `layer` calls.

## Gotchas
- Ordering: repeated `Router::layer` calls wrap all previously added routes, so middleware runs from bottom to top. A `ServiceBuilder` composes layers so they run top to bottom: the first layer sees the request first and the response passes back up through it last.
- If a layer's error type is not `Infallible` (for example a boxed error), axum needs a `HandleErrorLayer` to turn the error into a response.
- Prefer `axum::middleware::from_fn` for custom middleware; use `ServiceBuilder::map_request`, `map_response`, `then` or `and_then` for small transformations.

## Verify
Write a test that sends a request through the router and asserts the middleware effect (status, header) for both an accepted and a rejected request.

## Checked
Confirmed from the docs.rs tower page (Service, Layer, ServiceBuilder, module list, feature selection), the tower-http page (TraceLayer, CompressionLayer, DecompressionLayer) and the axum middleware page (applying layers, ServiceBuilder recommendation, ordering bottom-to-top versus top-to-bottom, from_fn, HandleErrorLayer, route_layer, request-id and timeout layers). Removed: `poll_ready` back-pressure wording, ConcurrencyLimitLayer, CorsLayer and the permissive-CORS warning, `SetRequestIdLayer::x_request_id`, the exact claim that route_layer avoids 404s, the tower-http timeout status code, the reqwest-middleware hedging note and the oneshot test.

Method: docs-checked 2026-11-09 against docs.rs tower, tower-http and the axum middleware module page.
