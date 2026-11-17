---
id: computing-software.web-development.dioxus.dioxus-spawn-tasks-use-action
name: dioxus-spawn-tasks-use-action
category: computing-software
field: web-development
product: dioxus
tags: [dioxus, spawn, spawn-forever, use-action, task, cancel, async, cancel-safe]
level: practitioner
status: docs-checked
description: "Run async work in Dioxus with spawn, async handlers, use_action, spawn_forever and Task cancel; keep futures cancel safe, no locks across await."
sources:
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/essentials/basics/async.md
  - https://github.com/DioxusLabs/docsite/blob/main/packages/docs-router/src/doc_examples/asynchronous.rs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Spawning futures and actions in Dioxus

Goal: do async work without blocking the UI thread.

Futures are lazy: nothing runs until awaited or spawned. In Dioxus all futures run on the main thread (concurrent, not parallel), so never run blocking work in them.

```rust
let mut response = use_signal(|| "Click to start a request".to_string());
rsx! {
    button {
        // an async closure returned from a handler is spawned automatically
        onclick: move |_| async move {
            response.set("...".into());
            let resp = reqwest::Client::new().get("https://dioxuslabs.com").send().await;
            if resp.is_ok() { response.set("dioxuslabs.com responded!".into()); }
            else { response.set("failed to fetch response!".into()); }
        },
        "{response}"
    }
}
```

Or call `spawn(async move { ... })`, which returns a `Task`.

## use_action

`use_action` combines a signal and a task; pass a callback returning a `Result<T>`:

```rust
let mut breed = use_action(move |breed| async move { /* reqwest::get(...).await ... */ });
// start: breed.call(cur_breed.clone());
match breed.value() {
    Some(Ok(res)) => rsx! { img { src: "{res.read().message}" } },
    Some(Err(_e)) => rsx! { div { "Failed to fetch a dog, please try again." } },
    None => rsx! { div { "Click the button to fetch a dog!" } },
}
```

Calling `.call()` while an action is pending cancels the current task and replaces it.

## Cancellation

- Spawned futures are cancelled when the component unmounts; use `spawn_forever` (attached to the root component) to keep running. Signals used inside must then live for the whole app, or using them after drop panics.
- Cancel manually with `task.cancel()` on the `Task` from `spawn` or `spawn_forever`.
- Futures can also be cancelled when a resource restarts, so they must be cancel safe: restore global state with a `Drop` guard rather than after the await.

## Heavy work and locks

Run expensive work with `std::thread::spawn` on desktop/mobile or a web worker on web. Never hold `read`/`write` locks across `.await`.

## Gotcha

A spawned task is not cancelled when the handler runs again; the docs use use_action for rapid input, because calling it while pending cancels the current task.

## Checked

2026-11-08. Confirmed against the Dioxus 0.7 async page (read in full) and its asynchronous.rs example file: lazy futures, main-thread execution, spawn and automatic spawning of returned futures, use_action with call and value, cancellation on unmount, spawn_forever, Task cancel, cancel safety, std::thread::spawn or web workers, and locks across await. Reworded the final gotcha to what the page states.

Method: documentation only; no commands were run.
