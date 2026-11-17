---
id: computing-software.web-development.leptos.component-props
name: component-props
category: computing-software
field: web-development
product: leptos
tags: [leptos, rust, props, component, optional, default, documentation, signal]
level: practitioner
status: docs-checked
description: "Define Leptos component props: pass signals for changing values, use #[prop(optional)], #[prop(default = ...)] and doc comments."
sources: [https://book.leptos.dev/view/03_components.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Define component props

Goal: split UI into reusable components that take arguments.

Props are extra arguments on the component function; you pass them like HTML attributes. Components are PascalCase.

```rust
#[component]
fn ProgressBar(
    progress: ReadSignal<i32>
) -> impl IntoView {
    view! { <progress max="50" value=progress /> }
}

// use it:
<ProgressBar progress=count/>
```

## Reactive vs static props

Props have no special meaning: a component is a function that runs once to set up the UI. If a prop changes over time, pass a signal type (like `ReadSignal<i32>`), not a plain `i32`.

## optional

`#[prop(optional)]` lets callers omit the prop; the value is `Default::default()` (for `u16`, `0`, rarely useful for a progress max).

```rust
#[prop(optional)] max: u16,
```

## default

`#[prop(default = 100)] max: u16` supplies a specific default. Call as `<ProgressBar max=50 progress=count/>` or omit `max`.

## Documenting components

Doc comments work on the component and on each prop (unlike plain Rust function args):

```rust
/// Shows progress toward a goal.
#[component]
fn ProgressBar(
    /// The maximum value of the progress bar.
    #[prop(default = 100)]
    max: u16,
    /// How much progress should be displayed.
    #[prop(into)]
    progress: Signal<i32>,
) -> impl IntoView { /* ... */ }
```

This generates docs for the component, its `Props` type and each setter field, visible on hover with rust-analyzer.

## Gotchas

- Passing a closure such as `double_count` to a `ReadSignal<i32>` prop does not compile: its type is a closure, not `ReadSignal<i32>`. See the generic and into skill.

## Related

- `computing-software.web-development.leptos.generic-and-into-props`

## Checked

2026-11-07: every claim, snippet and step above was compared with the full text of the cited Leptos book pages (https://book.leptos.dev/view/03_components.html) and the book source on GitHub. Statements the pages do not state were removed or trimmed.

Method: documentation only; no commands were run.
