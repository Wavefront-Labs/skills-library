---
id: computing-software.web-development.dioxus.dioxus-use-server-future
name: dioxus-use-server-future
category: computing-software
field: web-development
product: dioxus
tags: [dioxus, fullstack, use-server-future, suspense, serialization, hydration, ssr, reactivity]
level: practitioner
status: docs-checked
description: "Use use_server_future in Dioxus for SSR hydration: it auto-suspends and is reactive only in its closure, so read signals before the async block."
sources:
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/essentials/basics/suspense.md
  - https://github.com/DioxusLabs/docsite/blob/main/packages/docs-router/src/doc_examples/asynchronous.rs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Use use_server_future for suspense in fullstack Dioxus

Goal: make suspended data load during server-side rendering and hydrate on the client.

Dioxus fullstack waits for suspended futures during SSR, so data loading starts sooner and search engines see the resolved page. For hydration compatibility, switch every suspended resource to `use_server_future`. It serializes the future's result on the server and deserializes it on the client, and it suspends automatically, so you do not call `.suspend()`.

```rust
#[component]
fn BreedGallery(breed: ReadOnlySignal<String>) -> Element {
    // the value returned from the future must implement Serialize and Deserialize
    let response = use_server_future(move || async move {
        reqwest::Client::new()
            .get(format!("https://dog.ceo/api/breed/{breed}/images"))
            .send()
            .await
            // reqwest::Result is not Serialize, so map errors to a String
            .map_err(|err| err.to_string())?
            .json::<BreedResponse>()
            .await
            .map_err(|err| err.to_string())
    })?; // bubble up the suspense variant with ?

    // if it were still pending, the ? above returned; unwrap the None case
    let response_read = response.read();
    let response = response_read.as_ref().unwrap();
    rsx! { /* match response { Ok(..) .. Err(..) .. } */ }
}
```

## Reactivity rule

Unlike `use_resource`, `use_server_future` is reactive only in the closure, not in the future. To subscribe to a signal, read it in the closure and move the value into the async block:

```rust
use_server_future(move || {
    let cloned_id = id();       // reactive: read in the closure
    async move { println!("{cloned_id}"); }
});
```

Reading `id` inside the async block is not reactive.

## Streaming

By default SSR waits for all suspended futures and sends the fully resolved page. Enabling out of order streaming (`enable_out_of_order_streaming` on the serve config) sends finished HTML chunks one at a time, so suspense boundaries can show loading views while other futures resolve. See the HTML streaming skill.

## Checked

2026-11-08. Confirmed against the Dioxus 0.7 suspense page (read in full) and its asynchronous.rs example file: use_server_future serialization, automatic suspend, Serialize/Deserialize requirement, map_err to String, reactive only in the closure, and enable_out_of_order_streaming.

Method: documentation only; no commands were run.
