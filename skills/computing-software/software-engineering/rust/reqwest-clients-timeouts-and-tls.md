---
id: computing-software.software-engineering.rust.reqwest-clients-timeouts-and-tls
name: reqwest-clients-timeouts-and-tls
category: computing-software
field: software-engineering
product: rust
tags: [rust, rust-web-services, rust-reqwest, reqwest, http-client, timeouts, tls, rustls]
level: practitioner
status: docs-checked
description: "Use reqwest well: a shared Client, connect and total timeouts, TLS feature flags, JSON, streaming bodies, redirects and proxy settings."
sources:
  - https://docs.rs/reqwest/latest/reqwest/
  - https://docs.rs/reqwest/latest/reqwest/struct.ClientBuilder.html
  - https://docs.rs/reqwest/latest/reqwest/struct.Client.html
  - https://docs.rs/reqwest/latest/reqwest/struct.Response.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# reqwest clients, timeouts and TLS

**Goal:** a correct, reusable HTTP client.

```rust
let client = reqwest::Client::builder()
    .connect_timeout(Duration::from_secs(3))
    .timeout(Duration::from_secs(15))             // total deadline; default is none
    .pool_max_idle_per_host(8)
    .user_agent(concat!(env!("CARGO_PKG_NAME"), "/", env!("CARGO_PKG_VERSION")))
    .redirect(reqwest::redirect::Policy::limited(5))
    .build()?;                                    // build once and reuse

let resp = client.post(url).bearer_auth(token).json(&body).send().await?
    .error_for_status()?;                         // turns an error status into Err
let item: Item = resp.json().await?;
```

- `Client` holds a connection pool internally, so create one and reuse it; no `Rc` or `Arc` wrapper is needed because it already uses an `Arc` internally. `reqwest::get` is for one-off requests.
- `timeout` is a total request deadline from connect start until the body finishes (default none). `read_timeout` applies to each read and resets after a successful read, which suits stalled connections when size is unknown (default none). `connect_timeout` covers the connect phase only (default none) and needs a Tokio runtime with a timer.
- Pool defaults: `pool_idle_timeout` 90 seconds, `pool_max_idle_per_host` unlimited.
- Redirects: by default up to 10 hops; `redirect(Policy)` customises it.
- TLS is used by default (`default-tls` feature). Other features: `rustls`, `native-tls`, `native-tls-vendored`. Extra server certificates go on the builder with `add_root_certificate(Certificate)`; `danger_accept_invalid_certs` exists but should be limited to tests. Cargo features `json`, `form`, `stream`, `cookies`, `gzip` and others gate their helpers.
- Proxies: system proxies from `HTTP_PROXY`, `HTTPS_PROXY`, `ALL_PROXY` (and lowercase forms) are used by default; adding a `Proxy` replaces them and `ClientBuilder::no_proxy()` disables them. SOCKS needs the `socks` feature.
- Streaming a download: `Response::bytes_stream()` (needs the `stream` feature).
- The builder also has a `retry(policy)` option; check the docs for your reqwest version before adding a separate retry layer, and only retry idempotent requests.

## Gotchas
- Creating a `Client` per request defeats connection pooling.
- No default total timeout: a stalled server can hang the task.
- `Response::text()` loads the whole body; stream when reading from untrusted servers and cap the size yourself.

## Verify
Test against a mock server that delays and returns 500s; assert timeouts with `err.is_timeout()`.

## Checked
Method: docs-checked 2026-11-09 against the reqwest crate page, ClientBuilder (timeouts, pool, proxy, redirect, TLS methods), Client and Response pages. Dropped unconfirmed claims: the `rustls-tls` feature name, musl/OpenSSL remarks, reqwest-middleware/reqwest-retry, and wiremock.
