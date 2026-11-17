---
id: computing-software.web-development.leptos.deploy-non-root-path
name: deploy-non-root-path
category: computing-software
field: web-development
product: leptos
tags: [leptos, rust, deployment, router, base-path, hydration-scripts, trunk]
level: practitioner
status: docs-checked
description: "Serve a Leptos app from a non-root path like /my-app by setting Router base, HydrationScripts root, set_server_url for server functions, and Trunk public-url."
sources: [https://book.leptos.dev/deployment/sub_path.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deploy a Leptos app at a non-root path

Goal: serve the app at, say, `/my-app` instead of `/`.

## 1. Router `base`

```rust
<Router base="/my-app">
    <Routes fallback=|| "Not found.">
        <Route path=path!("/") view=Home/>
        <Route path=path!("/about") view=About/>
        <Route path=path!("/contact") view=Contact/>
    </Routes>
</Router>
```

Behind a reverse proxy the server may think it serves `/` while the browser sees `/my-app`. Then choose `base` by feature:

```rust
let base = if cfg!(feature = "hydrate") { "/my-app" } else { "/" };
// <Router base> ...
```

## 2. HydrationScripts `root`

With SSR, `<HydrationScripts/>` loads the JS/WASM. If those are served from a subdirectory, pass that base path as its `root` prop.

## 3. Server function URL

Server functions send requests to `/` by default. If the handler is mounted elsewhere, call `set_server_url` (in `leptos::server_fn::client`).

## 4. Trunk (CSR)

Set the public URL with `--public-url`; see the Trunk docs on asset directives.

Related: computing-software.web-development.leptos.deploy-ssr-app, computing-software.web-development.leptos.deploy-csr-static-hosts.

## Checked

2026-11-07: every claim, snippet and step above was compared with the full text of the cited Leptos book pages (https://book.leptos.dev/deployment/sub_path.html) and the book source on GitHub. Statements the pages do not state were removed or trimmed.

Method: documentation only; no commands were run.
