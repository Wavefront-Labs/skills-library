---
id: computing-software.web-development.dioxus.dioxus-rsx-elements-and-text
name: dioxus-rsx-elements-and-text
category: computing-software
field: web-development
product: dioxus
tags: [dioxus, rsx, element, text-node, format-strings, element-type, renderers]
level: intro
status: docs-checked
description: "Write Dioxus UI with rsx!: elements, text nodes with format-string interpolation, the Element type, and returning an error from a component."
sources:
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/essentials/ui/rsx.md
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/essentials/ui/elements.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# RSX elements and text

Goal: build a UI tree with `rsx!`, the proc macro that is the primary Dioxus syntax (it gets hot-reload, code folding and highlighting).

## Elements and text

An element is a name followed by curly braces; quoted text is a text node and follows `format!` rules (Display and Debug), but inside `{}` you may put full Rust expressions.

```rust
let author = "Dioxus Labs";
let content = "Build cool things";

rsx! {
    h1 { "Welcome to Dioxus!" }
    h3 { "Brought to you by {author}" }
    p { class: "main-content", {content} }
}
```

```rust
let user = use_signal(|| User { name: "Dioxus".to_string() });
rsx! { "Hello {user.read().name}" }
```

Attributes go inline like struct fields: `input { placeholder: "type something cool!" }`. Available elements include p, h1, span, div, a, pre, form, input, textarea, select, button, img, video, audio, canvas, svg, iframe, table and its parts, details, summary, dialog, progress, meter and time.

## The Element type

`rsx!` returns an `Element`, which can be assigned to variables, cheaply cloned and stored in state, and returned from plain functions:

```rust
fn create_description(content: &str) -> Element {
    if content.is_empty() {
        return Err("Missing description".into());
    }
    rsx! { span { class: "description", "{content}" } }
}
```

`Element` is an alias for `Result<VNode>`, so you can match on it or return an error while rendering. The error type is based on `anyhow` and composes with Error Boundaries and Server Functions.

## Renderers

Dioxus renders HTML and CSS everywhere. The first-party renderers are Dioxus-Web (DOM nodes), Dioxus-Webview (desktop and mobile system webview) and Dioxus-Native (native elements, still being improved). Web and Webview are the most mature.

## Checked

2026-11-09. Confirmed against the Dioxus 0.7 docsite pages rsx.md and elements.md and the building_uis_with_rsx.rs examples they include: RSX as the primary syntax with hot-reload, code folding and highlighting; format! rules (Display and Debug) with full expressions in braces; inline attributes; the element list; Element as an alias for Result<VNode> built on anyhow; the three first-party renderers and their maturity. Nothing removed.

Method: documentation only; no commands were run.
