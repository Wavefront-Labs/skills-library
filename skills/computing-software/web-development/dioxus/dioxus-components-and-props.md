---
id: computing-software.web-development.dioxus.dioxus-components-and-props
name: dioxus-components-and-props
category: computing-software
field: web-development
product: dioxus
tags: [dioxus, component, props, partialeq, readsignal, children, spread-props, props-default, props-into]
level: practitioner
status: docs-checked
description: "Define Dioxus components with #[component], extract props into a Props struct, and use #[props(default, into, extends)], ReadSignal, children and spread props."
sources:
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/essentials/ui/components.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Components and properties

Goal: write reusable components and control their props.

## Defining

A component is a function returning `Element`. To use it from another component, annotate it with `#[component]`; it must start with a capital letter or contain an underscore, take arguments implementing `PartialEq` and `Clone`, and return an `Element`. Arguments become the properties.

```rust
#[component]
pub fn MyComponent(name: String) -> Element {
    rsx! { div { h3 { "Hello, {name}!" } } }
}

rsx! { MyComponent { name: "World" } }
```

Do not call components like regular functions; RSX creates an instance with its own state and lifecycle.

## Props struct

```rust
#[derive(PartialEq, Clone, Props)]
struct CardProps { title: String, content: String }

#[component]
fn Card(props: CardProps) -> Element {
    rsx! { h1 { "{props.title}" } span { "{props.content}" } }
}
```

- `PartialEq` decides whether to rerender; you may hand-write it (for example compare a large dataset by id only).
- `Clone` is required because props are cloned each render; wrap expensive fields in `ReadSignal<T>` (no change for callers) or use `Arc`/`Rc`.
- `Props` derives a typed builder: `CardProps::builder().content("body".to_string()).build()`.

## #[props(...)] modifiers

- `#[props(default)]` makes a field optional with its default value.
- `#[props(!optional)]` makes an `Option<T>` field required.
- `#[props(into)]` converts via `Into`.
- `#[props(extends = GlobalAttributes)]` adds an element's attributes.

`Option<T>` fields default to `None`; `String` fields accept formatted strings; `ReadOnlySignal<T>` converts a passed `T`; a `children: Element` prop accepts child elements; `EventHandler<T>` enforces closures. Doc comments on fields show up as inline docs.

## Spread and children

`Card { title: "Chapter 1", ..props }` overrides fields of a prebuilt props value. A wrapper takes `children: Element` and renders it with `{children}`:

```rust
#[component]
fn RedDiv(children: Element) -> Element {
    rsx! { div { background_color: "red", {children} } }
}
```

## Checked
Checked 2026-11-07 against the 0.7 Components and Properties page (read in full). Confirmed: #[component] rules, Props struct and required traits, builder, ReadSignal, #[props] modifiers, Option, String, ReadOnlySignal, children and EventHandler behaviours, spread props, children example. Nothing removed.
Method: documentation only; no commands were run.
