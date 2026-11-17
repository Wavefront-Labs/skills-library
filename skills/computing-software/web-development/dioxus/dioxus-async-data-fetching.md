---
id: computing-software.web-development.dioxus.dioxus-async-data-fetching
name: dioxus-async-data-fetching
category: computing-software
field: web-development
product: dioxus
tags: [dioxus, use-resource, spawn, reqwest, serde, async, resource-restart, race-condition]
level: practitioner
status: docs-checked
description: "Fetch data in Dioxus with reqwest and serde: async onclick handlers, dioxus::spawn, and use_resource with restart() to avoid parallel-request race conditions."
sources:
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/tutorial/data_fetching.md
  - https://github.com/DioxusLabs/docsite/blob/main/packages/docs-router/src/doc_examples/guide_data_fetching.rs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Fetching data (reqwest, spawn, use_resource)

Goal: call an HTTP API from a Dioxus component. Dioxus has no built-in data-fetching utilities (crates such as dioxus-query exist), so the tutorial uses reqwest and serde.

```bash
cargo add reqwest --features json
cargo add serde --features derive
```

## Response type
The dog.ceo API returns `{"message": "...jpg", "status": "success"}`; deserialize the field you need:
```rust
#[derive(serde::Deserialize)]
struct DogApi {
    message: String,
}
```

## Async event handler
```rust
let mut img_src = use_signal(|| "".to_string());
let save = move |_| async move {
    let response = reqwest::get("https://dog.ceo/api/breeds/image/random")
        .await.unwrap()
        .json::<DogApi>()
        .await.unwrap();
    img_src.set(response.message);
};
// button { onclick: save, id: "save", "save!" }
```
Dioxus automatically calls `dioxus::spawn` on asynchronous closures. For async work without an async closure, call `spawn` on an async block:
```rust
button { onclick: move |_| { spawn(async move { /* do some async work... */ }); } }
```
Spawned futures run on the current async executor and are dropped automatically. They cannot borrow from outside the async block: `Copy` data can be captured, everything else must be moved (usually `.clone()`).

## use_resource
Bare async calls can race: clicking fetch twice quickly starts two parallel requests, and the wrong one may finish first. A `Resource` is state that depends on async work, with methods to start, stop, pause and modify it.
```rust
let mut img_src = use_resource(|| async move {
    reqwest::get("https://dog.ceo/api/breeds/image/random")
        .await.unwrap()
        .json::<DogApi>()
        .await.unwrap()
        .message
});

rsx! {
    img { src: img_src.cloned().unwrap_or_default() }
    button { onclick: move |_| img_src.restart(), id: "skip", "skip" }
}
```
Resources integrate with Suspense, Streaming HTML and reactivity; see the use_resource API docs for details.

## Checked
Checked 2026-11-07 against the 0.7 Fetching Data tutorial page and the guide_data_fetching.rs snippet file (both read in full). Confirmed: reqwest and serde dependencies, DogApi struct, async onclick, dioxus::spawn rules, use_resource with restart(). Removed: a pointer to use_server_future that the page does not mention.
Method: documentation only; no commands were run.
