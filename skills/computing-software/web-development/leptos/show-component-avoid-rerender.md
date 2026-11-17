---
id: computing-software.web-development.leptos.show-component-avoid-rerender
name: show-component-avoid-rerender
category: computing-software
field: web-development
product: leptos
tags: [leptos, rust, show, control-flow, performance, rerender]
level: practitioner
status: docs-checked
description: "Use the Leptos Show component to render an expensive branch once instead of rebuilding it on every signal change."
sources: [https://book.leptos.dev/view/06_control_flow.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: stop a `move || if cond { <Big/> } else { <Small/> }` closure from recreating components each time its signal changes.

## Why

A closure like this reruns whenever `value` changes, so with `value.get() > 5` it rebuilds `<Small/>` for every increment up to 5 and then `<Big/>` for every increment after. If those components load resources, create signals or create DOM nodes, that is wasted work.

## Method

Use `<Show/>` with a `when` function, a `fallback`, and children for the true case:

```rust
let (value, set_value) = signal(0);

view! {
  <Show
    when=move || { value.get() > 5 }
    fallback=|| view! { <Small/> }
  >
    <Big/>
  </Show>
}
```

`<Show/>` memoizes the `when` condition. `<Small/>` is rendered once and kept until the condition flips; then `<Big/>` renders once and stays, until the value drops back and `<Small/>` renders again.

## Gotchas

- There is overhead. For a very simple node (updating one text node, a class or an attribute) a plain `move || if ...` is more efficient. Reach for `<Show/>` when rendering either branch is at all expensive.
- In the page's example `fallback` is a function (`|| view! { <Small/> }`) and the children are the nested content between the `<Show>` tags. See `computing-software.web-development.leptos.passing-children-and-render-props`.
- Related: `computing-software.web-development.leptos.conditional-rendering-with-rust-control-flow`.

## Gaps

The page gives no measured numbers for the overhead of `<Show/>`.

## Checked

2026-11-07: Read in full: view/06_control_flow.md (tips, if/Option/match, Preventing Over-Rendering with the Small/Big log, the Show component and its memoized when, the overhead caveat, type conversions, inline sandbox source). Confirmed Show's when/fallback/children behaviour and that it 'memoizes the when condition'. One correction: removed the unsourced claim that children go to a `children` prop and that fallback is a 'render prop'; the text now describes only what the page's example shows. Live sandbox not opened.

Method: documentation only; no commands were run.
