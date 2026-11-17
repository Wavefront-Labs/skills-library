---
id: computing-software.web-development.dioxus.dioxus-rsx-attributes-and-listeners
name: dioxus-rsx-attributes-and-listeners
category: computing-software
field: web-development
product: dioxus
tags: [dioxus, rsx, attributes, event-listeners, oninput, spread-attributes, onresize, onvisible, style-attributes]
level: practitioner
status: docs-checked
description: "Set Dioxus RSX attributes: value types, conditional and repeated class, style properties, event listeners, spreading and custom quoted attributes."
sources:
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/essentials/ui/attributes.md
  - https://github.com/DioxusLabs/docsite/blob/main/packages/docs-router/src/doc_examples/building_uis_with_rsx.rs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# RSX attributes and event listeners

Goal: configure elements with attributes, including the RSX-specific forms.

## Basics

Write `name: value` in the element body. Values can be formatted text, so a signal can drive an input:

```rust
rsx! { input { type: "number" } }
let mut value = use_signal(|| "Hello world".to_string());
rsx! { input { oninput: move |event| value.set(event.value()), value: "{value}" } }
```

Attribute value kinds: `Text`, `Float`, `Int`, `Bool`, `Listener`, `Any` (type-erased `Rc<dyn Any>`, mostly for third-party renderers) and `None` (removes the attribute). Use `Some("scope")` / `None` for HTML boolean attributes: `div { itemscope: Some("scope") }`. Dioxus converts `false` to `None` for some attributes automatically.

## Special forms

- Conditional attribute: an unterminated `if` sets it only when true: `input { type: if number_type() { "number" } }`.
- Style: either one `style: "..."` string or each property as its own attribute, e.g. `background_color: "red"`, `margin: "10px"`.
- Class: `class` may appear several times and each is added to the class list:

```rust
span {
    class: if red { "bg-red-500" },
    class: if blue_border { "border border-blue-500" },
    class: "w-4 h-4 block",
}
```

- Spread a list of `Attribute` values with `button { ..attributes, "button" }`; later entries in the list win over earlier ones.
- Custom attributes: wrap the name in quotes, e.g. `div { "style": "width: 20px;" }`. This also works for events: `"onclick": "navigator.clipboard.writeText(window.document.title);"`.
- Event listeners always start with `on` and take a closure.
- `onresize` and `onvisible` are Dioxus-only attributes (not in the HTML spec), built on a cross-platform `IntersectionObserver`: `onresize: move |data| info!("{:#?}", data.get_border_box_size().unwrap())` and `onvisible: move |data| info!("visibility changed")`.

## Gotcha

- `dangerous_inner_html` overwrites the element's other attributes and children and is unsafe for untrusted data (XSS); sanitize first or render untrusted input as a text node.

## Checked

2026-11-08. Confirmed against the Dioxus 0.7 attributes page (read in full) and its building_uis_with_rsx.rs example file: value kinds, Some/None boolean attributes, conditional attributes, style attributes, repeated class, spreading, onresize and onvisible, custom quoted attributes, and dangerous_inner_html with its XSS warning.

Method: documentation only; no commands were run.
