---
id: computing-software.web-development.leptos.actions-for-async-mutations
name: actions-for-async-mutations
category: computing-software
field: web-development
product: leptos
tags: [leptos, rust, action, dispatch, pending, mutations]
level: practitioner
status: docs-checked
description: "Run an async function on demand in Leptos with Action, dispatch input, and read input, pending and value signals for loading or optimistic UI."
sources: [https://book.leptos.dev/async/13_actions.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: track an async operation triggered by an event (like submitting a form), as opposed to loading data, which is a resource.

Resource: load data when something changes. Action: occasionally run an async function in response to something like a click.

## Method

`Action::new` takes an async function with a reference to a single input. For several arguments use a tuple or struct; for none use `()`. The future must be `'static`, so clone the input into it.

```rust
let add_todo_action = Action::new(|input: &String| {
    let input = input.to_owned();
    async move { add_todo_request(&input).await }
});
```

Start it with `.dispatch(...)`, which is not async and can be called from event listeners, timeouts or anywhere:

```rust
add_todo_action.dispatch("Some value".to_string());
```

Signals synchronised with the action:

```rust
let submitted = add_todo_action.input();  // RwSignal<Option<String>>
let pending = add_todo_action.pending();  // ReadSignal<bool>
let todo_id = add_todo_action.value();    // RwSignal<Option<Uuid>>
```

Use them for loading indicators or optimistic UI. A form:

```rust
let input_ref = NodeRef::<Input>::new();
view! {
    <form on:submit=move |ev| {
        ev.prevent_default(); // don't reload the page
        let input = input_ref.get().expect("input to exist");
        add_todo_action.dispatch(input.value());
    }>
        <input type="text" node_ref=input_ref/>
        <button type="submit">"Add Todo"</button>
    </form>
    <p>{move || pending.get().then_some("Loading...")}</p>
}
```

## Notes

- Alternatively `spawn_local` plus your own signals, but an `Action` tracks pending state for you.
- The page says real apps usually pair actions with server functions, `ServerAction` and `<ActionForm/>`, and points to the `todo_app_sqlite` example. Those are not covered here.
- The page's sandbox wraps a `!Send` browser timer in `send_wrapper::SendWrapper` inside the action.

## Checked

2026-11-07: every claim, snippet and step above was compared with the full text of the cited Leptos book pages (https://book.leptos.dev/async/13_actions.html) and the book source on GitHub. Statements the pages do not state were removed or trimmed.

Method: documentation only; no commands were run.
