---
id: computing-software.web-development.leptos.islands-server-children-and-context
name: islands-server-children-and-context
category: computing-software
field: web-development
product: leptos
tags: [leptos, rust, islands, children, context, serde, routing]
level: practitioner
status: docs-checked
description: "Pass server-rendered children and serialized props into Leptos islands, share signals between islands via context, and handle client navigation without a router."
sources: [https://book.leptos.dev/islands.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Islands: server children, props, context, routing

Goal: compose small interactive islands around server-only content.

## Server-only code in components

In islands mode a `#[component]` body runs only on the server (unless used in an island), so server APIs work inline, for example `std::fs::read_to_string(filename)`. Island props and `children` can come from that server code without being in the WASM binary. Islands hydrate their own content, not the children passed in ("donuts", not islands).

## Props need serde

An island's props are serialized to JSON in `data-props`. If the build fails with `can't find crate for serde`, run `cargo add serde --features=derive`.

```rust
#[island]
fn Tabs(labels: Vec<String>, children: Children) -> impl IntoView { /* ... */ }
```

## Context between islands

```rust
#[island]
fn Tabs(labels: Vec<String>, children: Children) -> impl IntoView {
    let (selected, set_selected) = signal(0);
    provide_context(selected);
    // buttons call set_selected.set(index)
    /* ... {children()} */
}

#[island]
fn Tab(index: usize, children: Children) -> impl IntoView {
    let selected = expect_context::<ReadSignal<usize>>();
    view! { <div style:display=move || if selected.get() == index { "block" } else { "none" }>{children()}</div> }
}
```

On the server side, build the tab list lazily (`let tabs = move || ...` and call `{tabs()}` inside `<Tabs>`) so the parent island has provided context before each `Tab` looks for it.

Guideline: wrap only the interactive piece in `#[island]` and pass the inert remainder as `children`.

## Routing and redirects

Islands avoid a client router. The `islands_router` example in the repo adds a small JS router that fetches and diffs server-rendered pages, supporting links and forms. Without a router, server-function `redirect()` is not followed on the client; add one:

```rust
set_redirect_hook(|url| {
    window().location().set_href(url);
});
```

Benefits listed: roughly 50% smaller WASM in the demo, less double serialization (HTML plus JSON for resources), easy server-only APIs, less `#[server]`/Suspense boilerplate.

Previous: computing-software.web-development.leptos.islands-setup.

## Checked

2026-11-07: every claim, snippet and step above was compared with the full text of the cited Leptos book pages (https://book.leptos.dev/islands.html) and the book source on GitHub. Statements the pages do not state were removed or trimmed.

Method: documentation only; no commands were run.
