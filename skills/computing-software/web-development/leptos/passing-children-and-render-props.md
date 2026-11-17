---
id: computing-software.web-development.leptos.passing-children-and-render-props
name: passing-children-and-render-props
category: computing-software
field: web-development
product: leptos
tags: [leptos, rust, children, render-props, fragment, components]
level: practitioner
status: docs-checked
description: "Accept children and render-prop functions in a Leptos component, choose the right Children type, and map over child nodes with ChildrenFragment."
sources: [https://book.leptos.dev/view/09_component_children.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: write a component that wraps content passed between its tags (like `<FancyForm>`).

There are two mechanisms: render props (props that are functions returning a view, like `<Show fallback=...>`) and the special `children` prop (anything placed between the component tags).

## Method

```rust
#[component]
pub fn TakesChildren<F, IV>(
    render_prop: F,
    children: Children,
) -> impl IntoView
where
    F: Fn() -> IV,
    IV: IntoView,
{
    view! { {render_prop()} <hr/> {children()} }
}
```

Use it:

```rust
view! {
    <TakesChildren render_prop=|| view! { <p>"Hi, there!"</p> }>
        "Some text"
        <span>"A span"</span>
    </TakesChildren>
}
```

`Children` is an alias for `Box<dyn FnOnce() -> AnyView>`; the `AnyView` is opaque and cannot be inspected. If you need to call `children` more than once use `ChildrenFn` or `ChildrenMut` (for `Fn` / `FnMut`).

## Manipulating children

`ChildrenFragment` returns a `Fragment` (a wrapper around `Vec<AnyView>`) whose `nodes` you can iterate:

```rust
#[component]
pub fn WrapsChildren(children: ChildrenFragment) -> impl IntoView {
    let children = children()
        .nodes
        .into_iter()
        .map(|child| view! { <li>{child}</li> })
        .collect::<Vec<_>>();
    view! { <ul>{children}</ul> }
}
```

`<WrapsChildren>"A" "B" "C"</WrapsChildren>` renders a three-item list.

## Gotchas

- For component props (not HTML attributes) `render_prop=render_prop` can be shortened to `render_prop`.
- For several differently typed children use slots: `computing-software.web-development.leptos.component-slots`.

## Checked

2026-11-07: every claim, snippet and step above was compared with the full text of the cited Leptos book pages (https://book.leptos.dev/view/09_component_children.html) and the book source on GitHub. Statements the pages do not state were removed or trimmed.

Method: documentation only; no commands were run.
