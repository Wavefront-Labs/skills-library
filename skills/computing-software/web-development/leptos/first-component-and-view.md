---
id: computing-software.web-development.leptos.first-component-and-view
name: first-component-and-view
category: computing-software
field: web-development
product: leptos
tags: [leptos, rust, component, view-macro, signal, mount, prelude, on-click]
level: practitioner
status: docs-checked
description: "Write a first Leptos component with #[component], a signal, an on:click handler and the view! macro, and mount it with mount_to_body."
sources: [https://book.leptos.dev/view/01_basic_component.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Write your first Leptos component

Goal: render an `<App/>` component with a counter button, understanding the pieces.

## Mount

```rust
use leptos::mount::mount_to_body;

fn main() {
    mount_to_body(App);
}
```

## Component

```rust
use leptos::prelude::*;

#[component]
fn App() -> impl IntoView {
    let (count, set_count) = signal(0);

    view! {
        <button on:click=move |_| set_count.set(3)>
            "Click me: "
            {count}
        </button>
        <p>
            "Double count: "
            {move || count.get() * 2}
        </p>
    }
}
```

## Key points

- `use leptos::prelude::*;` brings in commonly used traits and functions; individual imports also work and the compiler will recommend them.
- `#[component]` marks a function as a component. Components are `PascalCase`, take zero or more arguments (gathered into a props struct built by `view!`), and return `impl IntoView`.
- The body is a set-up function that runs once, not a render function that reruns. Use it to create signals, side effects and describe the UI.
- `signal(0)` returns a `(getter, setter)` tuple. Read with `count.get()`, write with `set_count.set(...)` (on nightly with the `nightly` feature, `count()` and `set_count(...)` shorthands exist). `.get()` clones; `.with()` and `.update()` can be more efficient.
- Events use `on:{eventname}`, e.g. `on:click`. Text nodes are quoted strings; Rust expressions go in `{}`. All HTML elements work, including custom elements like `<my-custom-element>`.
- To increment in place use `*set_count.write() += 1;`, which gives a mutable reference.
- Unquoted text is partly supported but can cause spacing issues around punctuation and does not handle all Unicode; quoting always works.

## Related

- `computing-software.web-development.leptos.reactive-vs-static-view-values`
- `computing-software.web-development.leptos.csr-trunk-setup`

## Checked

2026-11-07: every claim, snippet and step above was compared with the full text of the cited Leptos book pages (https://book.leptos.dev/view/01_basic_component.html) and the book source on GitHub. Statements the pages do not state were removed or trimmed.

Method: documentation only; no commands were run.
