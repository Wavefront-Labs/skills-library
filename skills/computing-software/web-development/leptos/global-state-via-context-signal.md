---
id: computing-software.web-development.leptos.global-state-via-context-signal
name: global-state-via-context-signal
category: computing-software
field: web-development
product: leptos
tags: [leptos, rust, context, signals, global-state]
level: practitioner
status: docs-checked
description: "Share app-wide state in Leptos by calling provide_context with a signal at the root and reading it with use_context in descendants, keeping fine-grained updates."
sources: [https://book.leptos.dev/15_global_state.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: make one signal readable (and optionally writable) from components anywhere under a root without prop drilling.

## When to use
The page says most apps do not need global state; compose local state per component. Valid cases include theming, saved user settings, and sharing data between distant parts of the UI. The three recommended options are URL state via the router, signals through context (this skill), and a store (see `computing-software.web-development.leptos.global-state-with-stores`).

## Method
Create the signal at the root and `provide_context` it:

```rust
#[component]
fn App() -> impl IntoView {
    let (count, set_count) = signal(0);
    // provide the read half to the whole app
    provide_context(count);

    view! {
        <SetterButton set_count/>   // may modify the count
        <FancyMath/>                // read-only consumers
        <ListItems/>
    }
}
```

Consume it anywhere beneath with `use_context`:

```rust
let count = use_context::<ReadSignal<u32>>()
    .expect("there to be a `count` signal provided");
let is_even = move || count.get() & 1 == 0;
```

Pass `set_count` as a prop (as to `SetterButton`) to grant write access to specific components only.

## Gotchas
- `use_context::<T>()` returns an `Option`; the page calls `.expect` because the parent just provided the signal.
- A signal provided via context only triggers updates where it is read, not in components in between, so fine-grained reactivity is preserved at a distance.

## Checked

2026-11-07: every claim, snippet and step above was compared with the full text of the cited Leptos book pages (https://book.leptos.dev/15_global_state.html) and the book source on GitHub. Statements the pages do not state were removed or trimmed.

Method: documentation only; no commands were run.
