---
id: computing-software.web-development.dioxus.dioxus-suspense-boundary-streaming
name: dioxus-suspense-boundary-streaming
category: computing-software
field: web-development
product: dioxus
tags: [dioxus, suspense, suspenseboundary, suspend, use-server-future, fullstack, streaming, with-loading-placeholder]
level: practitioner
status: docs-checked
description: "Group async loading in Dioxus with SuspenseBoundary and .suspend()?, switch to use_server_future in fullstack, and enable out-of-order streaming."
sources:
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/essentials/basics/suspense.md
  - https://github.com/DioxusLabs/docsite/blob/main/packages/docs-router/src/doc_examples/asynchronous.rs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# SuspenseBoundary and use_server_future

Goal: show one loading view while several child components load.

Wrap children in `SuspenseBoundary` with a `fallback` closure, and call `.suspend()?` on a resource inside a child to pause that component until the future finishes:

```rust
fn DogGrid() -> Element {
    rsx! {
        SuspenseBoundary {
            fallback: |_| rsx! { div { "Loading..." } },
            div {
                BreedGallery { breed: "hound" }
                BreedGallery { breed: "poodle" }
            }
        }
    }
}

#[component]
fn BreedGallery(breed: ReadSignal<String>) -> Element {
    let response = use_resource(move || async move {
        reqwest::Client::new()
            .get(format!("https://dog.ceo/api/breed/{breed}/images"))
            .send().await?
            .json::<BreedResponse>().await
    })
    .suspend()?;
    // happy path: match &*response.read() { Ok(urls) => ..., Err(err) => ... }
    rsx! {}
}
```

While any child is suspended the boundary renders the fallback, then the children once resolved. The fallback closure receives a `SuspenseContext` that describes the suspended component. A child can offer a different loading view through the `with_loading_placeholder` method.

## Fullstack

Fullstack waits for suspended futures during server-side rendering, so data loading starts sooner and search engines see the resolved page. For hydration compatibility, switch every suspended resource to `use_server_future`: it serializes the result on the server and deserializes it on the client, and suspends automatically, so do not call `.suspend()`; you still bubble the suspense with `?`. The returned value must implement `Serialize` and `Deserialize`, so map `reqwest` errors to strings (`.map_err(|err| err.to_string())?`).

Unlike `use_resource`, `use_server_future` is reactive only in the closure, not in the future. Read signals in the closure first:

```rust
use_server_future(move || {
    let cloned_id = id();
    async move { println!("{cloned_id}"); }
});
```

## Streaming

By default SSR waits for all suspended futures and sends the full page. Enabling out-of-order streaming sends finished HTML chunks as they resolve, so suspense fallbacks show while others load:

```rust
dioxus::LaunchBuilder::new()
    .with_context(server_only! {
        dioxus::server::ServeConfig::builder().enable_out_of_order_streaming()
    })
    .launch(DogGrid);
```

## Checked

2026-11-08. Confirmed against the Dioxus 0.7 suspense page (read in full) and its asynchronous.rs example file: SuspenseBoundary, .suspend()?, the fallback SuspenseContext, with_loading_placeholder, use_server_future in fullstack, closure-only reactivity, and out-of-order streaming via ServeConfig::builder().enable_out_of_order_streaming().

Method: documentation only; no commands were run.
