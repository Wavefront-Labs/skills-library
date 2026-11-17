---
id: computing-software.web-development.dioxus.dioxus-suspense-fallback-placeholder
name: dioxus-suspense-fallback-placeholder
category: computing-software
field: web-development
product: dioxus
tags: [dioxus, suspense, suspenseboundary, use-resource, suspend, fallback, with-loading-placeholder]
level: practitioner
status: docs-checked
description: "Show one loading view for several async resources in Dioxus with SuspenseBoundary, a fallback closure, .suspend()? and with_loading_placeholder."
sources:
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/essentials/basics/suspense.md
  - https://github.com/DioxusLabs/docsite/blob/main/packages/docs-router/src/doc_examples/asynchronous.rs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Show one loading view for many async resources with SuspenseBoundary

Goal: avoid handling the loading state of each `use_resource` separately by wrapping children in a `SuspenseBoundary`.

## Steps

1. Wrap the children that load data in `SuspenseBoundary` and give it a `fallback` closure that returns the loading view. The closure may receive a `SuspenseContext`.
2. In each child component, call `.suspend()?` on the `use_resource` result. This pauses rendering of that component until the future finishes and returns early while it runs.
3. The boundary shows the fallback while any child is suspended, then shows the children again once suspense resolves.

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
            .send()
            .await?
            .json::<BreedResponse>()
            .await
    })
    // suspend the component and return early while the future is running
    .suspend()?;
    // then handle only the resolved (happy-path) value
    rsx! { /* use response.read() */ }
}
```

## Custom loading view from a child

To change the loading view while one specific task loads, a child can provide a different loading view with the `with_loading_placeholder` method. The placeholder it returns is passed to the boundary, which may render it instead of the default loading view.

## Notes

- The page's code uses `ReadSignal<String>` for the `breed` prop, so the resource re-runs reactively when it changes.
- In a fullstack (SSR) app, use `use_server_future` instead; see the use-server-future skill.

## Checked

2026-11-08. Confirmed against the Dioxus 0.7 suspense page (read in full) and its asynchronous.rs example file: SuspenseBoundary with a fallback closure (optionally taking a SuspenseContext), .suspend()? on use_resource, with_loading_placeholder, and ReadSignal<String> for the breed prop.

Method: documentation only; no commands were run.
