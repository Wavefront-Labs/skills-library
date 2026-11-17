---
id: computing-software.web-development.leptos.web-sys-and-noderef-access
name: web-sys-and-noderef-access
category: computing-software
field: web-development
product: leptos
tags: [leptos, rust, web-sys, wasm-bindgen, noderef, dom]
level: practitioner
status: docs-checked
description: "Call browser APIs from Leptos with web_sys, enable the needed cargo features and unstable-API cfg flag, and reach a typed DOM element through NodeRef."
sources: [https://book.leptos.dev/web_sys.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: use browser APIs or raw DOM elements the declarative API does not cover.

## JS libraries
`wasm-bindgen` underlies `trunk` and `cargo-leptos` and lets Rust import JS functions, classes and values (see its "importing functions from JS" docs). The page warns that React-dependent libraries, and libraries that manipulate DOM state (e.g. rich-text editors), are hard to integrate because both sides assume they own the state; separate their responsibilities. For reactive wrappers of Web APIs, the page points to the `leptos-use` crate.

## web-sys features
`web_sys` mirrors browser APIs 1:1 and is heavily feature-gated. Docs list required features per item (e.g. `DomRect` and `Element` for `get_bounding_client_rect`). Leptos already enables many; if yours is missing:

```toml
[dependencies.web-sys]
version = "0.3"
features = ["DomRect"]
```

Unstable standards (e.g. WebGPU) need `--cfg=web_sys_unstable_apis`, either per command or in `.cargo/config.toml`:

```toml
[env]
RUSTFLAGS = "--cfg=web_sys_unstable_apis"
```
(shell form: `RUSTFLAGS=--cfg=web_sys_unstable_apis cargo ...`). No stability guarantees apply.

## NodeRef
```rust
let node_ref = NodeRef::<Input>::new();
Effect::new(move |_| {
    if let Some(node) = node_ref.get() {
        leptos::logging::log!("value = {}", node.value());
    }
});
view! { <input node_ref=node_ref/> }
```
`node` is a `web_sys::HtmlInputElement`. `.get()` returns `Option` because the ref is empty until the element exists; effects run a tick after the component, so it is usually filled by then.

## Gotchas
- Translating a vanilla JS solution via the web-sys docs is the suggested approach for "how do I do X".

## Checked

2026-11-07: Read in full: web_sys.md (wasm-bindgen under trunk and cargo-leptos, JS library caveats, leptos-use, web-sys feature gating with DomRect, web_sys_unstable_apis cfg in env and RUSTFLAGS, the NodeRef Effect example and the tick caveat). Every statement matches. No claims were trimmed. Linked docs.rs pages were not opened.

Method: documentation only; no commands were run.
