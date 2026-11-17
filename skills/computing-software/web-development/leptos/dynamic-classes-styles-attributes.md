---
id: computing-software.web-development.leptos.dynamic-classes-styles-attributes
name: dynamic-classes-styles-attributes
category: computing-software
field: web-development
product: leptos
tags: [leptos, rust, class, style, attributes, derived-signal, inner-html, view-macro, reactivity]
level: practitioner
status: docs-checked
description: "Update CSS classes, inline styles and attributes reactively in Leptos with class:, style: and signal-valued attributes, plus derived signals."
sources: [https://book.leptos.dev/view/02_dynamic_attributes.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dynamic classes, styles, attributes and derived signals

Goal: change an element's class, style or attributes in response to a signal.

## Classes

`class:name=value` takes a class name and a `bool` or a function returning `bool`. True adds the class; false removes it.

```rust
<button
    on:click=move |_| { *set_count.write() += 1; }
    class:red=move || count.get() % 2 == 1
>
    "Click me"
</button>
```

Add the CSS yourself, e.g. in `index.html`: `<style>.red { color: red; }</style>`.

If the class name does not parse in the macro (dashes mixed with numbers etc.), use tuple syntax, and use an array to apply several classes under one condition:

```rust
class=("button-20", move || count.get() % 2 == 1)
class=(["button-20", "rounded"], move || count.get() % 2 == 1)
```

## Styles

```rust
style="position: absolute"
style:left=move || format!("{}px", count.get() + 100)
style:background-color=move || format!("rgb({}, {}, 100)", count.get(), 100)
style:max-width="400px"
// CSS variable
style=("--columns", move || count.get().to_string())
```

## Attributes

A plain string or primitive is static; a function (including a signal) is reactive. Signals are functions, so `value=count` and `value=move || count.get()` are interchangeable:

```rust
<progress max="50" value=count />
```

## Derived signals

A derived signal is a closure that reads a signal. Define once, use in many places:

```rust
let double_count = move || count.get() * 2;
// <progress max="50" value=double_count />
// <p>"Double Count: " {double_count}</p>
```

The calculation reruns once per signal change per place used; fine for cheap work. For expensive work the book points to memos (a later chapter).

## inner_html (advanced)

`<div inner_html=html/>` sets the HTML contents of an element, replacing any children. It does not escape input, so only use trusted content or escape entities to avoid XSS.

## Gotchas

- Self-closing tags such as `<br>` need an explicit slash: `<br/>`.

## Related

- `computing-software.web-development.leptos.reactive-vs-static-view-values`

## Checked

2026-11-07: every claim, snippet and step above was compared with the full text of the cited Leptos book pages (https://book.leptos.dev/view/02_dynamic_attributes.html) and the book source on GitHub. Statements the pages do not state were removed or trimmed.

Method: documentation only; no commands were run.
