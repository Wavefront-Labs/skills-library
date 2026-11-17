---
id: computing-software.web-development.dioxus.dioxus-component-lifecycle
name: dioxus-component-lifecycle
category: computing-software
field: web-development
product: dioxus
tags: [dioxus, lifecycle, use-hook, use-drop, use-effect, rerender, component, use-memo]
level: intro
status: docs-checked
description: "Dioxus component lifecycle: use_hook runs once, tracked values trigger re-renders, never mutate state in the component body, use_effect after render, use_drop for cleanup."
sources:
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/essentials/advanced/lifecycle.md
  - https://github.com/DioxusLabs/docsite/blob/main/packages/docs-router/src/doc_examples/component_lifecycle.rs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Component lifecycle in Dioxus

Goal: run code at the right point in a component's life.

## Initialize once: use_hook

The closure passed to `use_hook` runs the first time the component renders; the created value is reused on re-renders.

```rust
let random_number = use_hook(|| {
    let new_random_number = random_number();
    log!("{new_random_number}");
    new_random_number
});
```

## Rerender on tracked values

Reading a tracked value during render re-renders the component when it changes, and a prop change re-renders the child:

```rust
let mut count = use_signal(|| 0);
log!("Rerendering parent component with {}", *count.peek());
rsx! {
    button { onclick: move |_| count += 1, "Increment" }
    Count { current_count: count() }
}
```

## Do not mutate state in the body

```rust
// Don't: reads and writes state during render, easily an infinite loop
let mut count = use_signal(|| 0);
count += 1;
```

Instead derive state with `use_memo` or `use_resource`, or mutate it in an effect.

## Effects after render

```rust
use_effect(|| {
    log!("Effect ran");
    document::eval("document.getElementById('effect-output').innerText = 'Effect ran'");
});
```

Effects run after the component is rendered, so they can read or modify the rendered component.

## Cleanup

Before a component is dropped it drops all its hooks. If you only need the drop effect, use `use_drop`:

```rust
fn Child() -> Element {
    dioxus::core::use_drop(|| {
        log!("Child dropped");
    });
    rsx! { div { "Child" } }
}
```

In the example, a parent toggles `Child` with `if show() { Child {} }`; hiding it unmounts the child and runs the drop closure.

## Checked
Checked 2026-11-07 against the 0.7 Component Lifecycle page and the component_lifecycle.rs snippet file (both read in full). Confirmed: use_hook once, rerender on tracked values, no state mutation in the body, use_effect after render, use_drop cleanup. Removed: the opening mount, diff and drop sentence, which the page does not state.
Method: documentation only; no commands were run.
