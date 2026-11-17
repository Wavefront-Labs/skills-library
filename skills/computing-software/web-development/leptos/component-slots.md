---
id: computing-software.web-development.leptos.component-slots
name: component-slots
category: computing-software
field: web-development
product: leptos
tags: [leptos, rust, slots, slot-macro, children, components]
level: practitioner
status: docs-checked
description: "Define Leptos slots with the #[slot] macro so a component can take several differently typed child pieces like Then, ElseIf and Else."
sources: [https://book.leptos.dev/view/09_component_children.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: build a component that accepts multiple typed children, for example an `If` with `Then`, optional `ElseIf`s and an optional `Else`.

```rust
view! {
    <If condition=a_is_true>
        <Then>"Show content when a is true"</Then>
        <ElseIf condition=b_is_true>"b is true"</ElseIf>
        <Else>"None of the above are true"</Else>
    </If>
}
```

## Method

1. Annotate a plain struct with `#[slot]`:

```rust
#[slot]
struct Then {
    children: ChildrenFn,
}
```

2. Use the struct as a prop type:

```rust
#[component]
fn If(condition: Signal<bool>, then_slot: Then) -> impl IntoView {
    move || {
        if condition.get() {
            (then_slot.children)().into_any()
        } else {
            ().into_any()
        }
    }
}
```

3. At the call site, mark the slot element with `slot:<prop_name>`:

```rust
<If condition=a_is_true>
    <Then slot:then_slot>"Show content when a is true"</Then>
</If>
```

Writing `slot` with no name defaults to the snake-case struct name, so `<Then slot>` equals `<Then slot:then>`.

## Gotchas

- Event handlers cannot be placed directly on a slot (`<SlotWithChildren slot:slot on:click=...>` is not allowed). Wrap the slot content in a regular element and attach the handler there:

```rust
<SlotWithChildren slot:slot>
    <div on:click=move |_| {}><h1>"Hello, World!"</h1></div>
</SlotWithChildren>
```

- The page points to the slots examples in the Leptos repository for a complete example.
- Single-children case: `computing-software.web-development.leptos.passing-children-and-render-props`.

## Checked

2026-11-07: every claim, snippet and step above was compared with the full text of the cited Leptos book pages (https://book.leptos.dev/view/09_component_children.html) and the book source on GitHub. Statements the pages do not state were removed or trimmed.

Method: documentation only; no commands were run.
