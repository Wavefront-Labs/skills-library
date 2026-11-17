---
id: computing-software.web-development.leptos.ssr-modes-and-streaming
name: ssr-modes-and-streaming
category: computing-software
field: web-development
product: leptos
tags: [leptos, rust, ssr, streaming, suspense, resources, seo]
level: practitioner
status: docs-checked
description: "Pick a Leptos SSR rendering mode (sync, async, in-order, out-of-order, partially blocked) per route with ssr=SsrMode and use blocking resources for SEO."
sources: [https://book.leptos.dev/ssr/23_ssr_modes.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: choose how async data is rendered on the server and set it per route.

## Modes
1. Synchronous: serve a shell with `<Suspense/>` fallbacks; load data on the client (`LocalResource`). Fast TTFB, but slow data and no async data in `<title>`/`<meta>`.
2. Async (`SsrMode::Async`): load all resources on the server, render in one sweep. Good for meta tags; blank page until everything loads.
3. In-order streaming: send HTML up to each `<Suspense/>`, wait, continue. Something shows early, but no fallbacks and hydration cannot begin until the whole page arrives.
4. Out-of-order streaming (the default): send the synchronous shell with fallbacks, load on the server, stream resolved fragments and swap them in. Needs JavaScript (a small inline script with a `<template>`).
5. Partially blocked (`SsrMode::PartiallyBlocked`): like out-of-order, but a `<Suspense/>` reading a blocking resource is resolved on the server and included in the initial HTML, so it works without JS. Useful with several `<Suspense/>`; with one, or all blocking, it is a slower async.

Use a serialisable `Resource` where possible; `LocalResource` is for non-serialisable data and is a deoptimisation otherwise.

## Setting a mode
```rust
<Routes fallback=|| "Not found.">
    <Route path=path!("") view=HomePage/>
    <Route path=path!("/post/:id") view=BlogPost ssr=SsrMode::Async/>
</Routes>
```
For nested routes the most restrictive mode wins: async, then in-order, then out-of-order.

## Blocking resources
`Resource::new_blocking` still loads asynchronously, but reading it under a `<Suspense/>` blocks the HTML stream (including the shell) until resolved, letting `<Title/>` and `<Meta/>` render in the real head. Other `<Suspense/>` sections with normal resources stream later:

```rust
let post_data = Resource::new_blocking(/* load blog post */);
let comments_data = Resource::new(/* load comments */);
```
Wrap each read in `Suspend::new(async move { ... post_data.await ... })` inside its own `<Suspense/>`, and use `ssr=SsrMode::PartiallyBlocked` on the route.

## Checked

2026-11-07: Read in full: ssr/23_ssr_modes.md (all five modes with pros and cons, Using SSR Modes, nested-route most-restrictive rule, Blocking Resources, the BlogPost example, PartiallyBlocked route). Confirmed out-of-order as the default, the JS requirement and inline script note, SsrMode::Async and SsrMode::PartiallyBlocked names, Resource::new_blocking, and the LocalResource deoptimisation note. No claims were trimmed. The linked ssr_modes example and the embedded videos were not opened.

Method: documentation only; no commands were run.
