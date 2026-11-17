---
id: computing-software.web-development.leptos.server-state-and-context
name: server-state-and-context
category: computing-software
field: web-development
product: leptos
tags: [leptos, rust, axum, state, context, server-functions]
level: practitioner
status: docs-checked
description: "Share a database pool or app state with Leptos server functions via provide_context, or via Axum FromRef state with extract_with_state; work around generics."
sources: [https://book.leptos.dev/server/26_extractors.html, https://book.leptos.dev/server/28_async_quick_reference.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Share state with server functions (Axum): context, FromRef, generics

Goal: give server functions access to shared server data such as a connection pool.

## Often enough: Leptos context

Leptos has its own dependency injection. Provide the value when building the router:

```rust
let connection_pool = /* some shared state here */;

let app = Router::new()
    .leptos_routes_with_context(
        &leptos_options,
        routes,
        move || provide_context(connection_pool.clone()),
        {
            let leptos_options = leptos_options.clone();
            move || shell(leptos_options.clone())
        },
    )
    // etc.
```

Then read it in a server function with `use_context::<T>()` (or `expect_context`).

## When an extractor needs `State`

Provide the state both as context and as Axum router state, deriving `FromRef`, and call `extract_with_state`:

```rust
#[derive(FromRef, Debug, Clone)]
pub struct MyData {
    pub value: usize,
    pub leptos_options: LeptosOptions,
}

let app = Router::new()
    .leptos_routes_with_context(
        &app_state, routes,
        { let app_state = app_state.clone(); move || provide_context(app_state.clone()) },
        App,
    )
    .fallback(file_and_error_handler)
    .with_state(app_state);

#[server]
pub async fn uses_state() -> Result<(), ServerFnError> {
    let state = expect_context::<MyData>();
    let SomeStateExtractor(data) = extract_with_state(&state).await?;
    // todo
}
```

The page says to provide this by extending the existing `LeptosOptions` state with Axum's `FromRef` pattern (its `AppState` example derives `FromRef` and holds a `leptos_options: LeptosOptions` field next to other state).

## Generic state

Generic parameters are not supported on `#[server]` functions. Call an inner generic function from a server function that names the concrete type:

```rust
pub async do_thing_inner<TS: ThingService>() -> Result<(), ServerFnError> {
    let state = expect_context::<AppState<TS>>();
    state.thing_service.do_thing()
}

#[server]
pub async do_thing() -> Result<(), ServerFnError> {
    do_thing_inner::<ConcreteThingService<SomeDep>>().await
}
```

## Gotcha

The async quick-reference page says server function API endpoints run without the contexts the application set up, so `expect_context` and `use_context` on application-provided types will not work unless the values were provided via `.leptos_routes_with_context()`; see computing-software.web-development.leptos.async-execution-stages.

The doc snippets are partly pseudocode (for example `pub async do_thing_inner` lacks `fn`); fix when copying.

## Checked

2026-11-07: Read in full: server/26_extractors.md (Axum State, FromRef, extract_with_state, Generic State sections with their snippets) and server/28_async_quick_reference.md (the paragraph on server function endpoints running without application contexts unless provided by .leptos_routes_with_context()). Changed 'Preferred' to the page's 'can often be used instead of State', replaced the 'must extend' wording with what the AppState example shows, and rewrote the context gotcha to match the quick-reference page; added that page to sources. The page's snippets are partly pseudocode (noted in the skill). Not opened: the session_auth_axum example.

Method: documentation only; no commands were run.
