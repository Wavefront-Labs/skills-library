---
id: computing-software.web-development.dioxus.dioxus-ssr-hydration-rules
name: dioxus-ssr-hydration-rules
category: computing-software
field: web-development
product: dioxus
tags: [dioxus, ssr, hydration, use-server-cached, use-server-future, use-loader, use-effect, fullstack]
level: advanced
status: docs-checked
description: "Avoid Dioxus hydration errors: use_server_cached and use_server_future for non-deterministic data, use_effect for client-only data, use_loader."
sources:
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/essentials/fullstack/ssr.md
  - https://github.com/DioxusLabs/docsite/blob/main/packages/docs-router/src/doc_examples/hydration.rs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Avoid hydration errors in Dioxus SSR

Goal: make a component render exactly the same thing on the server and the client.

The server runs the component, waits for server futures, serializes non-deterministic data (such as a future's result), then renders HTML. The client hydrates by re-running each component with the deserialized data, adding event listeners and running effects (`use_effect`, `use_future`). If the two renders differ you may see errors such as `Cannot set properties of undefined (setting 'textContent')` or a deserialization error saying a type serialized on the server (e.g. f64) failed to deserialize on the client (e.g. i32).

## Rules

Non-deterministic values must go in `use_server_future`, `use_server_cached` or `use_effect`.

```rust
// bad: different value on client and server
let random: u8 = use_hook(|| rand::random());
// good: serialized on the server, deserialized on the client
let random: u8 = use_server_cached(|| rand::random());
```

```rust
// bad: may be finished on the server but pending on the client
let r: u8 = use_resource(|| random_server_function()).suspend()?().unwrap_or_default();
// good
let r: u8 = use_server_future(|| random_server_function())?().unwrap().unwrap_or_default();
```

Client-only data (such as localStorage) must be read inside `use_effect`, which runs after hydration. Start the signal as `None` and `set` it in the effect.

`use_server_cached` and `use_server_future` closures always run on the server but the client may skip them when the result was serialized, so they must not have side effects. Return the value instead of setting a signal inside:

```rust
// bad: signal state is not serialized
use_server_future(move || async move { storage.set(Some(server_future().await)); })?;
// good
let storage = use_server_future(|| async move { server_future().await })?;
```

## use_loader (new in 0.7)

`use_loader` is for isomorphic data loading. Unlike `use_server_future` it does not re-suspend the page when the future re-runs, and it re-throws loading errors to the nearest suspense boundary. Its callback returns a `Result<T, E>`; use `?` on the hook:

```rust
let breed_list = use_loader(move || async move {
    reqwest::get("https://dog.ceo/api/breeds/list/all").await?.json::<ListBreeds>().await
})?;
```

## Checked

2026-11-08. Confirmed against the Dioxus 0.7 server-side rendering page (read in full) and its hydration.rs example file: server and client hydration steps, both error messages, use_server_cached, use_server_future, use_effect for client-only data, no side effects in server hooks, and use_loader behaviour.

Method: documentation only; no commands were run.
