---
id: computing-software.web-development.leptos.clone-props-into-nested-children
name: clone-props-into-nested-children
category: computing-software
field: web-development
product: leptos
tags: [leptos, rust, children, clone, view-macro, ownership]
level: practitioner
status: docs-checked
description: "Fix cannot-move-out-of-captured-variable errors for owned props passed through several ChildrenFn components using the clone: view macro helper."
sources: [https://book.leptos.dev/interlude_projecting_children.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: pass an owned value (such as a `String`) down through components whose `children` are `ChildrenFn` and so run more than once.

## The problem
```rust
#[component]
pub fn App() -> impl IntoView {
    let name = "Alice".to_string();
    view! {
        <Outer>
            <Inner>
                <Inmost name=name.clone()/>
            </Inner>
        </Outer>
    }
}
```
where `Outer` and `Inner` take `children: ChildrenFn` and just call `children()`, and `Inmost(name: String)` renders it. Even with `name=name.clone()` this fails with `cannot move out of name, a captured variable in an Fn closure`. `name` is captured through several levels of children closures that may each run repeatedly, and there is no obvious place to clone it into them.

## Method
Use the `clone:` directive on the intermediate component. `clone:name` clones `name` before moving it into that component's children:

```rust
view! {
    <Outer>
        <Inner clone:name>
            <Inmost name=name.clone()/>
        </Inner>
    </Outer>
}
```

The page's example keeps `name=name.clone()` at the point of use.

## Gotchas
- For references to children and fallbacks themselves (not owned data), `StoredValue` is the alternative: see `computing-software.web-development.leptos.project-children-with-storedvalue`.

## Checked

2026-11-07: every claim, snippet and step above was compared with the full text of the cited Leptos book pages (https://book.leptos.dev/interlude_projecting_children.html) and the book source on GitHub. Statements the pages do not state were removed or trimmed.

Method: documentation only; no commands were run.
