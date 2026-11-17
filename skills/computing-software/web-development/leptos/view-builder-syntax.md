---
id: computing-software.web-development.leptos.view-builder-syntax
name: view-builder-syntax
category: computing-software
field: web-development
product: leptos
tags: [leptos, rust, builder-syntax, no-macros, view-macro, html-elements]
level: practitioner
status: docs-checked
description: "Build Leptos views without the view! macro using element functions, .child(), .attr(), .on() and component props builders."
sources: [https://book.leptos.dev/view/builder.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: write Leptos UI as plain Rust function calls when you prefer not to use `view!`. The builder syntax is always available but never required.

## Method

- A component can be a plain function; `#[component]` is optional: `pub fn counter(initial_value: i32, step: u32) -> impl IntoView { }`
- Elements are functions named after the tag: `p()`. Custom elements: `custom("my-custom-element")`.
- Children: `.child(...)` takes one child, a tuple, or an array of `IntoView` types: `p().child((em().child("Big, "), strong().child("bold "), "text"))`
- Attributes: `.attr("id", "foo")`, or built-in attribute methods like `.id("foo")`; reactive values are closures: `.attr("data-count", move || count.get().to_string())`
- `class:`, `prop:`, `style:` map to `.class()`, `.prop()`, `.style()`.
- Events: `.on(ev::click, move |_| ...)`; typed events from `leptos::ev` prevent typos and give correct callback types.

```rust
pub fn counter(initial_value: i32, step: i32) -> impl IntoView {
    let (count, set_count) = signal(initial_value);
    div().child((
        button().on(ev::click, move |_| set_count.set(0)).child("Clear"),
        button().on(ev::click, move |_| *set_count.write() -= step).child("-1"),
        span().child(("Value: ", move || count.get(), "!")),
        button().on(ev::click, move |_| *set_count.write() += step).child("+1"),
    ))
}
```

## Using built-in components

Each component is a function of one props argument, and props have a builder:

```rust
Show(
    ShowProps::builder()
        .when(move || value.get() > 5)
        .fallback(|| p().child("5 or lower"))
        .children(ToChildren::to_children(|| p().child("above 5")))
        .build(),
)
```

Or build the struct directly (`ShowProps { when: ..., fallback: (|| ...).into(), children: ToChildren::to_children(...) }`). The builder applies modifiers such as `#[prop(into)]`; with the struct form you call `.into()` yourself.

## Translating from view!

Use rust-analyzer "expand macro recursively" or `cargo-expand` to see what `view!` generates. `leptosfmt` is mentioned as a formatter for the macro syntax.

## Checked

2026-11-07: Read in full: view/builder.md (the no-macro builder always available, .child, .attr, .class, .prop, .style, .on(ev::click), custom(), Show builder versus struct form, rust-analyzer expand and cargo-expand, leptosfmt mention). Every statement matches. No claims were trimmed. Linked docs.rs pages were not opened.

Method: documentation only; no commands were run.
