---
id: computing-software.web-development.dioxus.dioxus-breaking-out-dom-js
name: dioxus-breaking-out-dom-js
category: computing-software
field: web-development
product: dioxus
tags: [dioxus, document-eval, web-sys, onmounted, use-effect, as-web-event, set-focus, canvas]
level: advanced
status: docs-checked
description: "Reach the DOM and JavaScript from Dioxus: document::eval, web-sys, use_effect after render, onmounted element handles with set_focus, and as_web_event downcasts."
sources:
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/essentials/advanced/breaking_out.md
  - https://github.com/DioxusLabs/docsite/blob/main/packages/docs-router/src/doc_examples/breaking_out.rs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Breaking out of Dioxus: eval, web-sys, onmounted

Goal: use browser APIs Dioxus does not wrap.

## eval

Dioxus exposes a limited set of web APIs. For anything else run JavaScript:

```rust
onclick: move |_| async move {
    domain.set(document::eval("return document.domain").await.unwrap().to_string());
},
```

## web-sys (web only)

```rust
use ::web_sys::window;
use wasm_bindgen::JsCast;
// in a handler:
domain.set(
    window().unwrap().document().unwrap()
        .dyn_into::<::web_sys::HtmlDocument>().unwrap()
        .domain(),
);
```

## Touch the DOM in use_effect

`use_effect` runs after the component and all Dioxus UI have rendered, so read or modify the DOM there. Reads inside are reactive:

```rust
use_effect(move || {
    let count = count.read();
    document::eval(&format!(
        r#"var c = document.getElementById("dioxus-canvas");
var ctx = c.getContext("2d");
ctx.clearRect(0, 0, c.width, c.height);
ctx.font = "30px Arial";
ctx.fillText("{count}", 10, 50);"#
    ));
});
rsx! { button { onclick: move |_| count += 1, "Increment" } canvas { id: "dioxus-canvas" } }
```

## Element handles with onmounted

`onmounted` fires after the element is first mounted and gives a live reference:

```rust
let mut input_element = use_signal(|| None);
button { onmounted: move |element| input_element.set(Some(element.data())), "First button" }
button {
    onclick: move |_| async move {
        if let Some(header) = input_element() {
            let _ = header.set_focus(true).await;
        }
    },
    "Focus first button"
}
```

## Downcast events

On web, `event.as_web_event()` (after `use dioxus::web::WebEventExt;`) returns the underlying web-sys event, for example `event.as_web_event().movement_x()` in an `onmousemove` handler; the example guards it with `#[cfg(feature = "web")]`.

## Checked
Checked 2026-11-07 against the 0.7 Breaking Out page and the breaking_out.rs snippet file (both read in full). Confirmed: document::eval, web-sys (web only), use_effect after render and its reactivity, onmounted with set_focus, as_web_event with WebEventExt and the web feature gate. Nothing removed; snippet file added to sources.
Method: documentation only; no commands were run.
