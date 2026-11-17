---
id: computing-software.web-development.dioxus.dioxus-router-routes-layouts-redirects
name: dioxus-router-routes-layouts-redirects
category: computing-software
field: web-development
product: dioxus
tags: [dioxus, router, routable, route, layout, outlet, link, nest, redirect, catch-all]
level: practitioner
status: docs-checked
description: "Build a Dioxus Router app: Routable enum, catch-all 404 route, layout with Outlet, Link, nested routes with URL params, external links, redirects."
sources:
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/router-example/first-route.md
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/router-example/building-a-nest.md
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/router-example/navigation-targets.md
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/router-example/redirection-perfection.md
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/tutorial/routing.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Dioxus Router: routes, layouts, params, redirects

Goal: type-safe routing. Enable the feature in Cargo.toml: `dioxus = { version = "0.7.0", features = ["fullstack", "router"] }` (the tutorial adds "router" this way).

## Routes and Router
```rust
#[derive(Routable, Clone)]
enum Route {
    #[route("/")]
    Home {},
}

fn App() -> Element {
    rsx! { Router::<Route> {} }
}

#[component]
fn Home() -> Element {
    rsx! { h1 { "Welcome to the Dioxus Blog!" } }
}
```
Each variant needs `#[route(path)]` and a component of the same name in scope. With no match the router renders nothing unless you add a catch-all:
```rust
#[route("/:..route")]
PageNotFound { route: Vec<String> },
```

## Layout with Outlet and Link
`#[layout(NavBar)]` wraps the following variants until `#[end_layout]`; the layout renders child routes where it places `Outlet::<Route> {}`.
```rust
#[component]
fn NavBar() -> Element {
    rsx! {
        nav { Link { to: Route::Home {}, "Home" } }
        Outlet::<Route> {}
    }
}
```
Use `Link` instead of `<a>`: an anchor causes a full-page reload and can point at a missing page; with the Route enum the compiler rejects links to pages that do not exist. Without any Outlet the current route renders where `Router {}` is declared.

## Nested routes and URL parameters
```rust
#[derive(Routable, Clone)]
enum Route {
    #[layout(NavBar)]
        #[route("/")]
        Home {},
        #[nest("/blog")]
            #[layout(Blog)]
            #[route("/")]
            BlogList {},
            #[route("/post/:name")]
            BlogPost { name: String },
            #[end_layout]
        #[end_nest]
    #[end_layout]
    #[route("/:..route")]
    PageNotFound { route: Vec<String> },
}

#[component]
fn BlogPost(name: String) -> Element { rsx! { h2 { "Blog Post: {name}" } } }
```
Link with params: `Link { to: Route::BlogPost { name: "Blog post 1".into() }, "Read" }`.

## External links
`Link { to: "https://dioxuslabs.com", "ExternalTarget target" }`. A NavigationTarget is Internal (a Route) or External (like an href; triggers a browser page reload, so not for in-app navigation).

## Redirects
Redirect attributes take a path and a closure returning a Route:
```rust
#[nest("/myblog")]
    #[redirect("/", || Route::BlogList {})]
    #[redirect("/:name", |name: String| Route::BlogPost { name })]
#[end_nest]
```

## Checked

2026-11-09. Confirmed against the Dioxus 0.7 router-example pages (first-route, building-a-nest, navigation-targets, redirection-perfection), the routing tutorial and the first_route, catch_all, nested_routes, dynamic_route, external_link and full_example .rs examples: the router feature line, Routable and Router, the nothing-rendered default and catch-all route, layout and Outlet, Link versus anchor, nest and URL parameters, Internal and External navigation targets, and redirect attributes. Removed the unsupported claim that Link to a plain path string also works.

Method: documentation only; no commands were run.
