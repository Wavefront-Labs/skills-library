---
id: computing-software.web-development.dioxus.dioxus-escape-hatches-eval-and-dom
name: dioxus-escape-hatches-eval-and-dom
category: computing-software
field: web-development
product: dioxus
tags: [dioxus, escape-hatch, eval, document-eval, dangerous-inner-html, web-components, web-sys, getelementbyid, tauri]
level: advanced
status: docs-checked
description: "Drop out of declarative RSX in Dioxus: document::eval with dioxus.send/recv, dangerous_inner_html, custom attributes, web components, web-sys, getElementById and native widgets."
sources:
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/essentials/ui/escape.md
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/guides/platforms/web.md
  - https://github.com/DioxusLabs/docsite/blob/main/packages/docs-router/src/doc_examples/eval.rs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Escape hatches from RSX

Goal: reach the DOM or JavaScript when declarative RSX is not enough.

## Custom attributes and web components

Quote an attribute name to use one outside the predefined set: `div { "data-my-button-id": 123 }`. Any element name containing a dash is a web component, rendered without type checking, and every attribute must be quoted, so wrap it in a typed component:

```rust
#[component]
fn MyWebComponent(name: String, age: i32) -> Element {
    rsx! {
        my-web-component {
            "name": "hello, {name}",
            "age": age + 10
        }
    }
}
```

## dangerous_inner_html

Use it for pre-rendered HTML (the docs pre-render markdown for the Dioxus homepage). It overwrites other attributes and children, and untrusted data exposes users to XSS, so sanitize or use a text node.

```rust
let contents = "live <b>dangerously</b>";  // should come from a trusted source
rsx! { div { dangerous_inner_html: "{contents}" } }
```

## eval

`document::eval` runs JavaScript in the platform renderer (web-sys on web, the webview's eval otherwise). Use `dioxus.send()` / `await dioxus.recv()` in JS and `send` / `recv` on the returned handle in Rust:

```rust
let mut eval = document::eval(r#"
    dioxus.send("Hi from JS!");
    let msg = await dioxus.recv();
    console.log(msg);
"#);
eval.send("Hi from Rust!").unwrap();
let reply = eval.recv::<String>().await.unwrap();
```

To address a node, give it an id (`id: "div-{id}"`, id from `use_hook(|| Uuid::new_v4())`) and use `document.getElementById` in the eval source.

## Other mechanisms

- `web-sys` gives typed browser calls, but is not portable to Dioxus Desktop and Mobile. If you need it there, Dioxus-Web is supported as a Tauri frontend.
- `onmounted`, `onresize` and `onvisible` give element access.
- Child windows and overlays let webview content sit over a native texture; see the wgpu_child_window example.
- Native widgets need FFI (Objective-C, Kotlin); see the dioxus-desktop crate docs. The Dioxus Native renderer (Vello based) can paint GPU textures into canvas elements.

## Gotcha

Custom index template: an `index.html` for web must include a `div` with id `main`.

## Checked
Checked 2026-11-07 against the 0.7 Escaping RSX page, the Web platform page and the snippet files eval.rs, dangerous_inner_html.rs and building_uis_with_rsx.rs (all read). Confirmed: custom attributes, web components, dangerous_inner_html and XSS warning, eval send and recv, getElementById pattern, web-sys portability, onmounted/onresize/onvisible, child windows, native widgets, Dioxus Native on Vello, custom index.html needing a div with id main. Nothing removed.
Method: documentation only; no commands were run.
