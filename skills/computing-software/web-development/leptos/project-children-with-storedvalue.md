---
id: computing-software.web-development.leptos.project-children-with-storedvalue
name: project-children-with-storedvalue
category: computing-software
field: web-development
product: leptos
tags: [leptos, rust, children, stored-value, show, ownership]
level: practitioner
status: docs-checked
description: "Pass ChildrenFn children and a fallback through nested Show components by moving them into StoredValue so the closures stay Fn."
sources: [https://book.leptos.dev/interlude_projecting_children.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: forward a component's `children` (and a `fallback`) through several layers of `<Show/>` or `<Suspense/>` without the `FnOnce` closure error.

## The problem
A component like `NestedShow` that wraps `children()` inside two `<Show/>` components fails with `expected a closure that implements the Fn trait, but this closure only implements FnOnce` (E0525). Each `<Show/>` takes `ChildrenFn`, so its children closure may be built many times. The first build moves `fallback` and `children` into the inner `<Show/>`, leaving nothing for later builds. Components own their props, so a captured reference is not enough.

## Method
Both `<Show/>` and `<Suspense/>` only need an immutable reference to children, so hand ownership to the reactive system with `StoredValue` (Copy and 'static, like a signal), then read it back inside the closures:

```rust
pub fn NestedShow<F, IV>(fallback: F, children: ChildrenFn) -> impl IntoView
where
    F: Fn() -> IV + Send + Sync + 'static,
    IV: IntoView + 'static,
{
    let fallback = StoredValue::new(fallback);
    let children = StoredValue::new(children);

    view! {
        <Show when=|| todo!() fallback=|| ()>
            <Show
                when=move || todo!()
                fallback=move || fallback.read_value()()
            >
                {children.read_value()()}
            </Show>
        </Show>
    }
}
```

1. Wrap `fallback` and `children` in `StoredValue::new` at the top of the component.
2. Inside nested closures, call `.read_value()` and invoke the result.

## Gotchas
- This works only because `<Show/>` needs `&` access to children, which `read_value` provides. If you must pass owned props through `ChildrenFn` layers, see `computing-software.web-development.leptos.clone-props-into-nested-children`.
- The `view!` macro hides the generated closures, so these errors are hard to read; the page says they can always be solved.

## Gaps
The page leaves the `when` conditions as `todo!()`.

## Checked

2026-11-07: Read in full: interlude_projecting_children.md (the E0525 FnOnce error with a children closure used in a For, the StoredValue fix, read_value, and the pointer to the clone: helper). Every claim in the skill traces to those sections. No claims were trimmed. Linked docs.rs pages were not opened.

Method: documentation only; no commands were run.
