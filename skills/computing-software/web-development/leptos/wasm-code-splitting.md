---
id: computing-software.web-development.leptos.wasm-code-splitting
name: wasm-code-splitting
category: computing-software
field: web-development
product: leptos
tags: [leptos, rust, code-splitting, lazy, lazy-route, cargo-leptos]
level: practitioner
status: docs-checked
description: "Split a Leptos WASM binary using cargo leptos --split, the #[lazy] macro and #[lazy_route] with the LazyRoute trait to load views concurrently with data."
sources: [https://book.leptos.dev/deployment/binary_size.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WASM code splitting: #[lazy] and #[lazy_route]

Goal: load parts of the app from separate WASM chunks on demand.

Support landed in summer 2025 and the page warns bugs may still be ironed out. Three pieces work together: `cargo leptos (serve|watch|build) --split`, `#[lazy]`, and `#[lazy_route]` with `LazyRoute`.

## #[lazy]

Marks a sync or async function as loadable from a separate chunk; it always becomes async. The first call fetches the chunk, later calls run directly.

```rust
#[lazy]
fn lazy_synchronous_function() -> String { "Hello, lazy world!".to_string() }

#[lazy]
async fn lazy_async_function() -> String { "Hello, lazy async world!".to_string() }

async fn use_lazy_functions() {
    let value1 = lazy_synchronous_function().await;
    let value1 = lazy_async_function().await;
}
```

## #[lazy_route]

Lazy-load a route view concurrently with its data, avoiding a waterfall (load view, then start loading data). Nested routes each load their own data and lazy view concurrently.

```rust
use leptos::prelude::*;
use leptos_router::{lazy_route, LazyRoute};

#[derive(Debug)]
struct BlogListingRoute { titles: Resource<Vec<String>> }

#[lazy_route]
impl LazyRoute for BlogListingRoute {
    fn data() -> Self {
        Self { titles: Resource::new(|| (), |_| async { vec![/* load posts */] }) }
    }
    // lazy-loaded, concurrently with data()
    fn view(this: Self) -> AnyView {
        let BlogListingRoute { titles } = this;
        // use the resource with Suspense, etc., return .into_any()
    }
}
```

Further reading from the page: the `lazy_routes` example in the Leptos repo and a linked YouTube talk.

Related: computing-software.web-development.leptos.wasm-binary-size.

## Checked

2026-11-07: Read in full: the Code Splitting section of deployment/binary_size.md (--split flag, #[lazy] sync and async examples, #[lazy_route] with LazyRoute, the waterfall explanation, the summer 2025 caveat). Every statement and both code samples match the page. No claims were trimmed. The linked YouTube video and the lazy_routes example were not opened.

Method: documentation only; no commands were run.
