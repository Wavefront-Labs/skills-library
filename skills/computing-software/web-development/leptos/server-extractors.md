---
id: computing-software.web-development.leptos.server-extractors
name: server-extractors
category: computing-software
field: web-development
product: leptos
tags: [leptos, rust, extractors, axum, actix, server-functions]
level: practitioner
status: docs-checked
description: "Use leptos_axum::extract and leptos_actix::extract inside Leptos server functions to read request data such as method, query, headers and connection info."
sources: [https://book.leptos.dev/server/26_extractors.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Use Actix and Axum extractors in server functions

Goal: read typed request data (method, query string, headers, cookies, connection info) inside a `#[server]` function.

## Method

Leptos integrates with Actix Web (`leptos_actix`) and Axum (`leptos_axum`). Each provides an `extract` helper that works like a handler's argument list; routes are plugged in with `.leptos_routes()`.

Actix:

```rust
#[derive(Deserialize, Debug)]
struct MyQuery { foo: String }

#[server]
pub async fn actix_extract() -> Result<String, ServerFnError> {
    use actix_web::dev::ConnectionInfo;
    use actix_web::web::Query;
    use leptos_actix::extract;

    let (Query(search), connection): (Query<MyQuery>, ConnectionInfo) = extract().await?;
    Ok(format!("search = {search:?}\nconnection = {connection:?}",))
}
```

Axum:

```rust
#[server]
pub async fn axum_extract() -> Result<String, ServerFnError> {
    use axum::{extract::Query, http::Method};
    use leptos_axum::extract;

    let (method, query): (Method, Query<MyQuery>) = extract().await?;
    Ok(format!("{method:?} and {query:?}"))
}
```

The page's snippets place the `use` lines inside the function body.

The page says the same `extract()` pattern gives access to headers, cookies, database connection pools, and more.

## Data-loading idea

Plain Axum/Actix handlers extract everything near the top of the request, before rendering. Leptos pushes loading down to the leaves: a component calls a server function that extracts what it needs, so a button can refresh only its own data and routes do not have to declare all their data up front.

## Gotchas

- The Axum `extract` function only supports extractors whose state is `()`. For extractors needing `State`, use `extract_with_state`; see computing-software.web-development.leptos.server-state-and-context.

Related: computing-software.web-development.leptos.server-function-basics.

## Checked

2026-11-07: Read in full: the book chapter server/26_extractors.md (Server Frameworks, Using Extractors, Actix and Axum Extractors, Axum State, Generic State, Data-Loading Patterns); the Actix and Axum snippets are inline on the page and match. Trimmed the claim that the `use` lines keep server-only crates out of the client build (the page does not say why they are inside the body) and softened the headers/cookies/pools sentence to what the page says. Added the page's `extract_with_state` pointer. Not opened: the linked docs.rs pages and the session_auth_axum example.

Method: documentation only; no commands were run.
