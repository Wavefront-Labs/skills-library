---
id: computing-software.web-development.dioxus.dioxus-server-functions
name: dioxus-server-functions
category: computing-software
field: web-development
product: dioxus
tags: [dioxus, fullstack, server-functions, get-macro, post-macro, extractors, path-query, filestream]
level: practitioner
status: docs-checked
description: "Define Dioxus server functions with get/post macros: argument and return types, path and query syntax, server-only extractors, client calls."
sources:
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/essentials/fullstack/server_functions.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Write Dioxus server functions

Goal: expose an Axum-compatible endpoint as a plain async Rust function callable from the client.

```rust
#[get("/api/hello-world")]
async fn hello_world() -> Result<String> {
    Ok("Hello world!".to_string())
}
```

After launching you can `curl http://127.0.0.1:8080/api/hello-world` (returns "Hello world!"), or call `hello_world().await` from client code.

## Macros and restrictions

Use `#[get]`, `#[post]`, `#[put]`, `#[delete]`, `#[patch]` or the anonymous `#[server]`. The function must be async, return `Result<T, E>`, take arguments that are `Serialize + Deserialize` or `IntoRequest + FromRequest`, and return a type that is `Serialize + Deserialize` or `IntoResponse + FromResponse`. Type errors for unsatisfied bounds can be unwieldy.

- Several plain arguments become one serializable JSON body.
- A single special body type can be used, e.g. `file: FileStream` or a `Streaming<String>` return.
- For a third-party Axum response type without `FromResponse`, call `.into_response()` and return `axum::response::Response`.

## Path and query

```rust
#[get("/api/products/{product}?color&quantity")]
async fn get_product_data(product: String, color: String, quantity: Option<i32>) -> Result<Vec<Product>> { /* */ }

#[post("/api/photos/upload?name&rating")]
async fn upload_photo(name: String, rating: i32, image: FileStream) -> Result<i32> { /* */ }
```

Dioxus generates `axum::extract::Query<T>` and `Path<T>`; values are URL-encoded and decoded, so stick to simple types.

## Server-only extractors

Hoist extractor arguments into the macro. They must implement Axum's `FromRequestParts` (or `FromRequest` if there is no client body). They are not sent by the client.

```rust
#[post("/api/user/login", auth: auth::Session)]
pub async fn login() -> Result<()> { auth.login_user(2); Ok(()) }

#[get("/api/headers", headers: dioxus::fullstack::HeaderMap)]
async fn get_headers() -> Result<String> { Ok(format!("{:#?}", headers)) }
```

Extractors can be stacked (e.g. `header: TypedHeader<Cookie>, auth: Session`), which eases migrating existing Axum handlers.

## Checked

2026-11-08. Confirmed against the Dioxus 0.7 server functions page (read in full): the macros, restrictions, JSON body from plain arguments, into_response for third-party types, path and query syntax, hoisted server-only extractors, and stacking extractors.

Method: documentation only; no commands were run.
