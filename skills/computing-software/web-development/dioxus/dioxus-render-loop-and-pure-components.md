---
id: computing-software.web-development.dioxus.dioxus-render-loop-and-pure-components
name: dioxus-render-loop-and-pure-components
category: computing-software
field: web-development
product: dioxus
tags: [dioxus, rendering, rerender, reconciliation, diffing, pure-functions, use-signal, side-effects]
level: practitioner
status: docs-checked
description: "How Dioxus components render and rerender (props PartialEq, signal writes), diffing, and why the component body must be pure with mutations in handlers or effects."
sources:
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/essentials/ui/render.md
  - https://github.com/DioxusLabs/docsite/blob/main/packages/docs-router/src/doc_examples/components.rs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# How components render and rerender

Goal: predict when a component function runs again and keep its body pure.

## The loop

`dioxus::launch` sets up the runtime and calls your initial component to get an `Element`. The virtual tree is not real DOM; a platform renderer converts it into real elements and draw calls. Components are not normal functions: they need an active Dioxus runtime.

A component reruns when state it depends on changes, in two cases:

- its properties change (judged by `PartialEq`), or
- internal state it read changes (for example `signal.write()`) and an update is scheduled.

Mutation happens in event handlers. After a rerun Dioxus diffs the old and new `Element`, working out the fewest draw calls to match the new UI. Only dynamic parts of the RSX are compared; static elements are skipped. The cycle Render, Display, Listen, Mutate is called reconciliation.

```rust
#[component]
fn MyStatefulComponent() -> Element {
    let mut count = use_signal(|| 0);
    rsx! {
        div {
            h3 { "Count: {count}" }
            button { onclick: move |_| count += 1, "Increment" }
        }
    }
}
```

A component is a function of state, `fn(State) -> Element`, reading props, hooks and context. Your RSX declares the desired UI, not how to update to it.

## Purity

The body must be pure: same inputs, same output, no side effects. Hooks and context count as external state, so do not modify them while rendering.

```rust
// Impure: writes a signal during render, may loop or behave unexpectedly
count += 1;
```

Put mutations in event handlers (`onclick: move |_| count += 1`), in effects that run after render, or in long-running async tasks reacting to background work.

## Gotcha

If a component body is not pure, the docs say you are likely misusing the reactive paradigm.

## Checked
Checked 2026-11-07 against the 0.7 Reconciliation page and the components.rs snippet file (both read in full). Confirmed: launch and virtual tree, rerun conditions via PartialEq and signal writes, diffing of dynamic parts, reconciliation loop, fn(State) -> Element, purity rule and the impure count += 1 example, mutation in handlers, effects or async tasks. Nothing removed.
Method: documentation only; no commands were run.
