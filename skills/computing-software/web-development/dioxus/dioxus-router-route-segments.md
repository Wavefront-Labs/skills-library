---
id: computing-software.web-development.dioxus.dioxus-router-route-segments
name: dioxus-router-route-segments
category: computing-software
field: web-development
product: dioxus
tags: [dioxus, router, routable, route-attribute, dynamic-segments, catch-all, query-segments, nest]
level: practitioner
status: docs-checked
description: "Define Dioxus Router routes: Routable enum with #[route], static, dynamic, catch-all, query and hash segments, custom types, #[nest], and rendering Router and Link."
sources:
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/essentials/router/index.md
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/essentials/router/routes.md
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/essentials/router/nested.md
  - https://github.com/DioxusLabs/docsite/blob/main/packages/docs-router/src/doc_examples/router_introduction.rs
  - https://github.com/DioxusLabs/docsite/blob/main/packages/docs-router/src/doc_examples/route_customization.rs
  - https://github.com/DioxusLabs/docsite/blob/main/packages/docs-router/src/doc_examples/dynamic_segments.rs
  - https://github.com/DioxusLabs/docsite/blob/main/packages/docs-router/src/doc_examples/catch_all_segments.rs
  - https://github.com/DioxusLabs/docsite/blob/main/packages/docs-router/src/doc_examples/query_segments.rs
  - https://github.com/DioxusLabs/docsite/blob/main/packages/docs-router/src/doc_examples/hash_fragments.rs
  - https://github.com/DioxusLabs/docsite/blob/main/packages/docs-router/src/doc_examples/nest.rs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Define Dioxus Router routes

Goal: describe your pages as a type-checked `Routable` enum.

Add the feature: `dioxus = { version = "0.7", features = ["router"] }`. Each enum variant needs a component of the same name in scope (or pass another as the second argument: `#[route("/", HomePage)] Index {}`).

```rust
#[derive(Clone, Debug, PartialEq, Routable)]
enum Route {
    #[route("/")] Home,
    #[route("/about")] About,
    #[route("/user/:id")] User { id: u32 },
}

fn main() { dioxus::launch(|| rsx! { Router::<Route> {} }); }
// link with: Link { to: Route::About, "Go to About Page" }
```

## Segment kinds

Matching goes from most specific to least (static, dynamic, catch-all; query and hash always match), then by definition order.

- Static: `#[route("/hello/world")]`.
- Dynamic: `:name`, any type implementing `FromStr` (and `Display` for custom types). If parsing fails the route does not match and matching continues. Component props must include the same fields.
- Catch-all: `:..name` such as `/blog/:..segments` with `segments: Vec<String>`; must be the last path segment, not in nests. Custom types implement `FromRouteSegments` and `ToRouteSegments`.
- Query: `?:name&:surname` after all path segments, not in nests; parsing must not fail. `FromQueryArgument` is auto-implemented for `FromStr + Default` types, falling back to `Default::default()`. Capture the whole query with `?:..params` for a type implementing `From<&str>` and `Display`.
- Hash: `#:field` (e.g. `/blog#:name`) after path and query segments, not in nests; `FromHashFragment` is auto-implemented for `FromStr + Default`.

```rust
#[route("/blog/:..segments")] BlogPost { segments: Vec<String> },
#[route("/search?:query&:sort")] Search { query: String, sort: SortOrder },
```

## Nesting

Use `#[nest("/blog")]` ... `#[end_nest]` (or end of enum) to avoid repeating a prefix. A nest path cannot contain a catch-all or query segment. Dynamic segments in a nest are available to child routes and layouts, and children must include those fields:

```rust
#[nest("/blog")]
    #[nest("/:id")]
        #[route("/post")] PostId { id: usize },
    #[end_nest]
    #[route("/:id")] BlogPost { id: usize },
```

Use `#[rustfmt::skip]` on the enum to keep the indentation.

## Checked
Checked 2026-11-07 against the 0.7 Router Introduction, Defining Routes and Nested Routes pages and the router_introduction, route_customization, dynamic_segments, catch_all_segments, query_segments, hash_fragments and nest snippet files (all read in full). Confirmed: router feature, Routable derive, second-argument component, matching order, all five segment kinds with their rules, custom type traits, nest rules, #[rustfmt::skip]. Nothing removed.
Method: documentation only; no commands were run.
