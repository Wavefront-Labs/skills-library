---
id: computing-software.web-development.leptos.global-state-with-stores
name: global-state-with-stores
category: computing-software
field: web-development
product: leptos
tags: [leptos, rust, stores, reactive-stores, context, global-state]
level: practitioner
status: docs-checked
description: "Model app-wide state as a struct with #[derive(Store)] from reactive_stores so each field updates independently, provided through context."
sources: [https://book.leptos.dev/15_global_state.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: keep a global struct whose fields are read and written reactively without notifying readers of other fields.

## Method
Stores are available from Leptos 0.7 through the separately shipped `reactive_stores` crate. Derive `Store` on the struct (`use reactive_stores::Store;`):

```rust
#[derive(Clone, Debug, Default, Store)]
struct GlobalState {
    count: i32,
    name: String,
}
```

This generates a trait `GlobalStateStoreFields` adding a method per field (`count`, `name`) to `Store<GlobalState>`; each returns a reactive field. Provide the store at the root and fetch it with `expect_context`:

```rust
#[component]
fn App() -> impl IntoView {
    provide_context(Store::new(GlobalState::default()));
    // ...
}

#[component]
fn GlobalStateCounter() -> impl IntoView {
    let state = expect_context::<Store<GlobalState>>();
    // reactive access to the `count` field only
    let count = state.count();

    view! {
        <button on:click=move |_| { *count.write() += 1; }>
            "Increment Global Count"
        </button>
        <span>"Count is: " {move || count.get()}</span>
    }
}
```

## Gotchas
- Clicking the button updates only `state.count`; anything reading `state.name` is not notified. This combines top-down data flow with fine-grained updates.
- The page points to the repo `stores` example for a fuller demonstration.
- Simpler alternative for a single value: `computing-software.web-development.leptos.global-state-via-context-signal`.

## Checked

2026-11-07: every claim, snippet and step above was compared with the full text of the cited Leptos book pages (https://book.leptos.dev/15_global_state.html) and the book source on GitHub. Statements the pages do not state were removed or trimmed.

Method: documentation only; no commands were run.
