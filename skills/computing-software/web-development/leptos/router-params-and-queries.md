---
id: computing-software.web-development.leptos.router-params-and-queries
name: router-params-and-queries
category: computing-software
field: web-development
product: leptos
tags: [leptos, rust, router, params, query-string, hooks]
level: practitioner
status: docs-checked
description: "Read route params and URL query strings in Leptos with use_params, use_query, and the untyped map hooks, deriving Params on structs and handling Option or Result."
sources: [https://book.leptos.dev/router/18_params_and_queries.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: read `:id`-style params and `?q=` queries reactively.

## Method
Four hooks in `leptos_router::hooks`: `use_params` / `use_params_map` and `use_query` / `use_query_map`. Queries are readable from any `<Route/>` view; params from the route that defines them or its nested children.

Typed: derive `Params` (from `leptos_router::params::Params`, plus `use leptos::Params;` as on the page) on a flat struct; each field is parsed with `FromStr`.

```rust
#[derive(Params, PartialEq)]
struct ContactParams { id: Option<usize> }

#[derive(Params, PartialEq)]
struct ContactSearch { q: Option<String> }

let params = use_params::<ContactParams>();
let query = use_query::<ContactSearch>();

let id = move || {
    params.read().as_ref().ok()
        .and_then(|params| params.id)
        .unwrap_or_default()
};
```

Typed hooks return `Memo<Result<T, _>>` (a Memo so it follows URL changes; a Result because parsing can fail).

Untyped: return `Memo<ParamsMap>`, whose `.get()` gives `Option<String>`:

```rust
let params = use_params_map();
let id = move || params.read().get("id");
```

## Gotchas
- On stable Rust only `Option<T>` fields work; with the `nightly` feature you can use `T` or `Option<T>`.
- `Params` is deliberately lighter and less flexible than `serde` (flat string map only).
- Handling the Option/Result forces you to decide what a missing or invalid value means, and navigating between paths for the same route yields fine-grained updates without re-rendering the wrapping component.

## Checked

2026-11-07: Read in full: router/18_params_and_queries.md including its inline CodeSandbox source. Confirmed the four hooks, the Params derive at leptos_router::params::Params with use leptos::Params, FromStr per field, Memo<Result<T, _>> versus Memo<ParamsMap>, the stable Option<T> versus nightly T note, and the fine-grained-update rationale. No claims were trimmed. Not opened: the docs.rs pages for the hooks.

Method: documentation only; no commands were run.
