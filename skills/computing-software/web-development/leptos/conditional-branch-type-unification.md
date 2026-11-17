---
id: computing-software.web-development.leptos.conditional-branch-type-unification
name: conditional-branch-type-unification
category: computing-software
field: web-development
product: leptos
tags: [leptos, rust, into-any, either, view-types, control-flow]
level: practitioner
status: docs-checked
description: "Fix Leptos compile errors when if or match branches return different view types by using Either enums or .into_any()."
sources: [https://book.leptos.dev/view/06_control_flow.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: make a conditional with branches of different element types compile.

## Problem

Leptos uses a statically typed view tree. `view! { <pre>..</pre> }` returns a different type from `view! { <p>..</p> }` or `<textarea>`, and Rust cannot return different types from different branches, so a `match` mixing them will not compile.

## Method

Two options, per the page:

1. Use the `Either` enum (and `EitherOf3`, `EitherOf4`, and so on) to make the branches one type.
2. Call `.into_any()` on each branch to convert to a single type-erased `AnyView`.

```rust
view! {
    <main>
        {move || match is_odd() {
            true if value.get() == 1 => {
                view! { <pre>"One"</pre> }.into_any()
            },
            false if value.get() == 2 => {
                view! { <p>"Two"</p> }.into_any()
            }
            _ => view! { <textarea>{value.get()}</textarea> }.into_any()
        }}
    </main>
}
```

## Gotchas

- The strong typing exists to enable compile-time optimisations; type erasure with `.into_any()` trades some of that away for convenience. The page does not quantify the cost.
- The page shows only `.into_any()` in code; for the `Either` family it gives the names but no example, so check the API docs for the exact variant constructors.
- Related: `computing-software.web-development.leptos.conditional-rendering-with-rust-control-flow`.

## Checked

2026-11-07: every claim, snippet and step above was compared with the full text of the cited Leptos book pages (https://book.leptos.dev/view/06_control_flow.html) and the book source on GitHub. Statements the pages do not state were removed or trimmed.

Method: documentation only; no commands were run.
