---
id: computing-software.web-development.leptos.router-setup-and-routes
name: router-setup-and-routes
category: computing-software
field: web-development
product: leptos
tags: [leptos, rust, router, routes, routing]
level: practitioner
status: docs-checked
description: "Add leptos_router, wrap the app in Router, and declare Routes with Route path! and view, a fallback, static, :param and *wildcard paths."
sources: [https://book.leptos.dev/router/16_routes.html, https://book.leptos.dev/router/17_nested_routing.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: get URL-to-component routing working in a Leptos app.

## Method
1. Add the `leptos_router` crate. Unlike `leptos`, it has no `csr` or `hydrate` features; it has an `ssr` feature to activate for the server-side build only.
2. Import: `use leptos_router::components::{Router, Route, Routes};` (and `use leptos_router::path;` for the macro).
3. Wrap the app in one `<Router/>`, near the root. Use only one: the router drives global state, so several would be ambiguous.
4. Put `<Routes/>` where matched views should render; things outside it (nav bars) show on every page. Give it a `fallback`.

```rust
#[component]
pub fn App() -> impl IntoView {
    view! {
      <Router>
        <nav>/* ... */</nav>
        <main>
          <Routes fallback=|| "Not found.">
            <Route path=path!("/") view=Home/>
            <Route path=path!("/users") view=Users/>
            <Route path=path!("/users/:id") view=UserProfile/>
            <Route path=path!("/*any") view=|| view! { <h1>"Not Found"</h1> }/>
          </Routes>
        </main>
      </Router>
    }
}
```

`path!` accepts a static path (`/users`), named params with a colon (`/:id`), and a wildcard with an asterisk (`/user/*any`). `view` is a `Fn() -> impl IntoView`; a prop-less component can be passed directly (`view=Home` is shorthand for `view=|| view! { <Home/> }`).

## Gotchas
- The router is a separate crate from `leptos`, so everything in it is user-land code and replaceable.
- Next steps: `computing-software.web-development.leptos.router-nested-routes-outlet`, `computing-software.web-development.leptos.router-params-and-queries`.

## Checked

2026-11-07: Read in full: router/16_routes.md (Getting Started, Providing the Router, Defining Routes, the five-route snippet and the view shorthand note) and the CodeSandbox source inside router/17_nested_routing.md, which is where `use leptos_router::path;` appears (16 itself only imports components); that page is now listed in sources. Confirmed: no csr or hydrate features and an ssr feature for the server build, one Router near the root, Routes fallback, static, colon and asterisk path forms, view as Fn() -> impl IntoView. No claims were trimmed. The live CodeSandbox was not opened (its source is inline on the page).

Method: documentation only; no commands were run.
