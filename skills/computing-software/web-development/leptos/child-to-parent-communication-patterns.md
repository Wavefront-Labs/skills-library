---
id: computing-software.web-development.leptos.child-to-parent-communication-patterns
name: child-to-parent-communication-patterns
category: computing-software
field: web-development
product: leptos
tags: [leptos, rust, parent-child, callbacks, props, events]
level: practitioner
status: docs-checked
description: "Choose how a Leptos child component notifies its parent: pass a WriteSignal, pass a callback prop, or add an on: listener on the component."
sources: [https://book.leptos.dev/view/08_parent_child.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: pick between three prop-level patterns for child-to-parent communication (context is the fourth; see `computing-software.web-development.leptos.context-instead-of-prop-drilling`).

Parent-to-child is easy: pass a `ReadSignal` or `Signal` as a prop.

## 1. Pass a WriteSignal

```rust
<ButtonA setter=set_toggled/>

#[component]
pub fn ButtonA(setter: WriteSignal<bool>) -> impl IntoView {
    view! { <button on:click=move |_| setter.update(|v| *v = !*v)>"Toggle"</button> }
}
```

Simple, but the parent hands off mutation rights and it is unclear when or how the value changes. Used widely, it invites spaghetti code.

## 2. Pass a callback

```rust
<ButtonB on_click=move |_| set_toggled.update(|v| *v = !*v)/>

#[component]
pub fn ButtonB(on_click: impl FnMut(MouseEvent) + 'static) -> impl IntoView {
    view! { <button on:click=on_click>"Toggle"</button> }
}
```

The child only fires an event; the mutation logic stays in the parent. This keeps local state local, at the cost of the logic living up in the parent. The page calls these real trade-offs, not right-or-wrong.

## 3. Event listener on the component

When the callback maps directly to a native DOM event, skip the prop:

```rust
<ButtonC on:click=move |_| set_toggled.update(|v| *v = !*v)/>

#[component]
pub fn ButtonC() -> impl IntoView { view! { <button>"Toggle"</button> } }
```

The listener is added to each top-level element the component returns (here the one `<button>`), and the event is correctly typed.

## Gotchas

- Option 3 only works for real DOM events passed straight to rendered elements. For logic that does not map to an element (the page's example is `<ValidatedForm/>` with an `on_valid_form_submit` callback) use option 2.
- `MouseEvent` comes from `leptos::ev::MouseEvent`.

## Checked

2026-11-07: every claim, snippet and step above was compared with the full text of the cited Leptos book pages (https://book.leptos.dev/view/08_parent_child.html) and the book source on GitHub. Statements the pages do not state were removed or trimmed.

Method: documentation only; no commands were run.
