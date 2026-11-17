---
id: computing-software.web-development.dioxus.dioxus-static-site-generation
name: dioxus-static-site-generation
category: computing-software
field: web-development
product: dioxus
tags: [dioxus, fullstack, ssg, static-site-generation, incremental-renderer, static-routes, dx-bundle, serveconfig]
level: advanced
status: docs-checked
description: "Pre-render a Dioxus site with SSG: incremental rendering in ServeConfig, a static_routes server function, and dx bundle --web --ssg."
sources:
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/essentials/fullstack/static_site_generation.md
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/essentials/fullstack/publishing.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Static site generation (SSG) with Dioxus

Goal: pre-generate every static page at build time and host without a server.

Dioxus SSG runs your app locally, queries it for a sitemap, then indexes the site with `curl` requests and caches each page's HTML on the filesystem. You may not need SSG: use it for lots of static content and no backend (docs, portfolios). Often setting `Cache-Control` headers while rendering and letting a CDN cache is enough.

## 1. Enable incremental rendering

```rust
fn main() {
    dioxus::LaunchBuilder::new()
        .with_cfg(server_only! {
            ServeConfig::builder()
                .incremental(
                    dioxus::server::IncrementalRendererConfig::new()
                        .static_dir(std::env::current_exe().unwrap().parent().unwrap().join("public"))
                        // keep wasm and assets already in public
                        .clear_cache(false)
                )
                .enable_out_of_order_streaming()
        })
        .launch(app);
}
```

## 2. List static routes

The CLI calls a server function at the endpoint `"static_routes"` and pre-renders each route returned. You must set that endpoint explicitly instead of the default generated one. Routes with no dynamic segments are included by `Route::static_routes()`.

```rust
#[server(endpoint = "static_routes", output = server_fn::codec::Json)]
async fn static_routes() -> Result<Vec<String>, ServerFnError> {
    Ok(Route::static_routes().iter().map(ToString::to_string).collect())
}
```

## 3. Bundle

```sh
dx bundle --web --ssg
```

A `public` folder appears in the dx folder; copy it to any static host such as GitHub Pages.

## GitHub Pages

In `Dioxus.toml`, point `out_dir` at `docs` and set `base_path` to your repo name:

```toml
[application]
out_dir = "docs"
[web.app]
base_path = "your_repo"
```

The publishing page then builds with `dx build --release --features web` and `cargo run --features ssr`, commits, and pushes, with GitHub Pages set to serve the docs directory. No code is given here for the page's own static-generation sample, which was not readable.

## Checked

2026-11-09. Confirmed against the Dioxus 0.7 fullstack pages static_site_generation.md and publishing.md and the static_site_generation.rs example: how SSG works, when not to use it, the ServeConfig incremental code, the static_routes endpoint and server function, `dx bundle --web --ssg` and the public folder, and the GitHub Pages out_dir and base_path settings and build steps. The publishing page's code include (fullstack_static.rs) did not resolve, so that sample is left out.

Method: documentation only; no commands were run.
