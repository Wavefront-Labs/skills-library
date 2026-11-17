---
id: computing-software.web-development.leptos.router-nested-routes-outlet
name: router-nested-routes-outlet
category: computing-software
field: web-development
product: leptos
tags: [leptos, rust, router, nested-routes, outlet, layout]
level: practitioner
status: docs-checked
description: "Use ParentRoute and Outlet to render layout and child views side by side, add empty-path fallbacks, and factor route groups into transparent components."
sources: [https://book.leptos.dev/router/17_nested_routing.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: model layouts (list plus detail, tabs) with nested routes instead of duplicated flat routes.

## Key idea
Nested routes are a layout tool, not just a way to avoid retyping paths: a single URL can match several routes, all rendered at once. Changing `/users` and `/users/:id` into

```rust
<ParentRoute path=path!("/users") view=Users>
    <Route path=path!(":id") view=UserProfile/>
    <Route path=path!("") view=NoUser/>
</ParentRoute>
```

means `/users/3` renders `<Users/>` and `<UserProfile/>`, and `/users` renders `<Users/>` and `<NoUser/>`. Without the `path!("")` route, plain `/users` would not match anything.

## Outlet
A parent does not render its children automatically; place `<Outlet/>` where the matched child should appear. It renders nothing if no nested route matches. Forgetting it is a common reason nested routes seem not to work.

```rust
view! {
  <div style="display: flex">
    <For each=contacts key=|c| c.id children=|c| todo!()/>
    <Outlet/>
  </div>
}
```

Nesting can go deeper (`ParentRoute` inside `ParentRoute`, e.g. contacts > :id > tabs `""`, `address`, `messages`).

## Factoring routes out
Move a route subtree into a transparent component:

```rust
#[component(transparent)]
fn ContactInfoRoutes() -> impl MatchNestedRoutes + Clone {
    view! {
      <ParentRoute path=path!(":id") view=ContactInfo>
        <Route path=path!("") view=EmailAndPhone/>
        <Route path=path!("address") view=Address/>
      </ParentRoute>
    }
    .into_inner()
    .into_any_nested_route()
}
```

`.into_inner()` strips debug info added by `view!`.

## Why
Navigating between sibling children does not re-render the parent (state such as a search box persists), and the `:id` param updates reactively, so only small text nodes change.

## Checked

2026-11-07: Read in full: router/17_nested_routing.md (Nested Routes as Layout, Why Nested Routing, Outlet, Refactoring Route Definitions with component(transparent) and into_inner, Nested Routing and Performance, and the inline CodeSandbox source). Confirmed that /users matches nothing without the empty-path child route, that Outlet renders nothing when no nested route matches, and the ContactList state-persistence point. No claims were trimmed. The live sandbox was not opened (source is inline).

Method: documentation only; no commands were run.
