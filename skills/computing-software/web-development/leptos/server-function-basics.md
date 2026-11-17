---
id: computing-software.web-development.leptos.server-function-basics
name: server-function-basics
category: computing-software
field: web-development
product: leptos
tags: [leptos, rust, server-functions, server, serde]
level: practitioner
status: docs-checked
description: "Define a Leptos #[server] function, call it from the browser, return Result with ServerFnError or a custom error type, and avoid usize and serde_qs pitfalls."
sources: [https://book.leptos.dev/server/25_server_functions.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Leptos server functions: define, call, handle errors

Goal: run code that only exists on the server (database, secrets, server-only crates) and call it from client code as if it were a local async function.

## Method

Annotate a top-level `fn` with `#[server]`:

```rust
#[server]
pub async fn add_todo(title: String) -> Result<(), ServerFnError> {
    let mut conn = db().await?;
    match sqlx::query("INSERT INTO todos (title, completed) VALUES ($1, false)")
        .bind(title)
        .execute(&mut conn)
        .await
    {
        Ok(_row) => Ok(()),
        Err(e) => Err(ServerFnError::ServerError(e.to_string())),
    }
}
```

Call it from a click handler with `spawn_local`:

```rust
move |_| {
    spawn_local(async {
        add_todo("So much to do!".to_string()).await;
    });
}
```

Rules the page states:
- It must be `async` and return `Result<T, ServerFnError>` (or a custom error type), even if the server work is synchronous, because browser calls are network requests.
- It is a top-level `fn`, not a closure: no access to reactive state, only to its arguments. Arguments and return value must be serializable.
- On the server it is a normal function exposed as an HTTP endpoint; in the browser build the body is replaced by a fetch stub. Server-only dependencies like `sqlx` are fine inside the body.
- Defaults: arguments are encoded as an HTTP POST using `serde_qs`, return values as JSON via `serde_json`, mounted at a hashed URL. This keeps it compatible with `<form>` without WASM. The `#[server]` macro and the `server_fn` crate document other encodings and fixed endpoints.

## Custom error types

Any error type implementing `FromServerFnError` works:

```rust
#[derive(Debug, Clone, Deserialize, Serialize)]
pub enum AppError {
    ServerFnError(ServerFnErrorErr),
    DbError(String),
}

impl FromServerFnError for AppError {
    type Encoder = JsonEncoding;
    fn from_server_fn_error(value: ServerFnErrorErr) -> Self {
        AppError::ServerFnError(value)
    }
}

#[server]
pub async fn create_user(name: String, email: String) -> Result<User, AppError> { /* ... */ }
```

(imports: `server_fn::codec::JsonEncoding`, `serde::{Deserialize, Serialize}`, `leptos::prelude::*`.)

## Gotchas

- Security: a server function is a public API endpoint. Its body is not public, but its return value is sent to whoever calls it. Only return public data unless you authenticate, encrypt, rate limit, etc.
- Pointer-sized `isize`/`usize` in arguments or returns can cause a deserialization error between 32-bit WASM and a 64-bit server if a value does not fit in 32 bits. The page suggests fixed-size types such as `i32` or `i64`.
- `serde_qs` does not always handle `Option` types or enums with tuple variants; use the workarounds in the linked Leptos issues (3832, 4016, 4464) or switch the input encoding.

Related: computing-software.web-development.leptos.server-extractors, computing-software.web-development.leptos.action-form.

## Gaps

The page does not list the alternative encodings in detail; see the `#[server]` macro docs.

## Checked

2026-11-07: Read in full: server/25_server_functions.md (co-location and isomorphism, async and Result rules, security admonition, default serde_qs POST and serde_json encoding with hashed URL, custom errors with FromServerFnError, quirks with usize and serde_qs, issues 3832/4016/4464). Snippets are inline and match. Softened the usize rule from an imperative to the page's wording (errors when a value does not fit in 32 bits; fixed-size types mitigate). Not opened: the linked GitHub issues and docs.rs macro docs.

Method: documentation only; no commands were run.
