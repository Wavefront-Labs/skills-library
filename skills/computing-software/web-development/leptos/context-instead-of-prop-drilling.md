---
id: computing-software.web-development.leptos.context-instead-of-prop-drilling
name: context-instead-of-prop-drilling
category: computing-software
field: web-development
product: leptos
tags: [leptos, rust, context, provide-context, use-context, prop-drilling]
level: practitioner
status: docs-checked
description: "Share a signal setter with deeply nested Leptos components via provide_context and use_context instead of threading props through every layer."
sources: [https://book.leptos.dev/view/08_parent_child.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: let a deep descendant (`<ButtonD/>`) update state owned by `<App/>` without adding a prop to every intermediate component.

## Problem

With `App > Layout > Content > ButtonD`, passing `set_toggled: WriteSignal<bool>` through `Layout` and `Content` is "prop drilling": they only forward it, and changing its type (say to an `enum`) means editing three places.

## Method

Provide at the top with `provide_context`, consume below with `use_context`. Contexts are identified by their type and live in a top-down tree that follows the UI tree.

```rust
#[component]
pub fn App() -> impl IntoView {
    let (toggled, set_toggled) = signal(false);
    provide_context(set_toggled);   // share with all children
    view! { <p>"Toggled? " {toggled}</p> <Layout/> }
}

#[component]
pub fn ButtonD() -> impl IntoView {
    let setter = use_context::<WriteSignal<bool>>().expect("to have found the setter provided");
    view! { <button on:click=move |_| setter.update(|v| *v = !*v)>"Toggle"</button> }
}
```

`Layout` and `Content` drop their `set_toggled` parameter.

The page's full example wraps the setter in a newtype to avoid clashing with other possible `WriteSignal<bool>` contexts:

```rust
#[derive(Copy, Clone)]
struct SmallcapsContext(WriteSignal<bool>);
provide_context(SmallcapsContext(set_smallcaps));
let setter = use_context::<SmallcapsContext>().unwrap().0;
```

## Gotchas

- You lose compile-time type safety between provider and consumer: finding the context is a runtime check (`use_context(...).expect(...)`), and the compiler will not guide a refactor.
- The same caution as passing a `WriteSignal` applies: state can be mutated from arbitrary places. Provide state at the highest level that needs it.
- No performance penalty: intermediate components do nothing when the signal updates, since signals are fine-grained.

Related: `computing-software.web-development.leptos.child-to-parent-communication-patterns`.

## Checked

2026-11-07: every claim, snippet and step above was compared with the full text of the cited Leptos book pages (https://book.leptos.dev/view/08_parent_child.html) and the book source on GitHub. Statements the pages do not state were removed or trimmed.

Method: documentation only; no commands were run.
