---
id: computing-software.web-development.dioxus.dioxus-use-resource-use-loader
name: dioxus-use-resource-use-loader
category: computing-software
field: web-development
product: dioxus
tags: [dioxus, use-resource, use-loader, data-fetching, reqwest, waterfall, cancel-safe, resource]
level: practitioner
status: docs-checked
description: "Fetch data in Dioxus with reqwest, use_resource and use_loader, and avoid request waterfalls by starting every resource before any early return."
sources:
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/essentials/basics/resources.md
  - https://github.com/DioxusLabs/docsite/blob/main/packages/docs-router/src/doc_examples/asynchronous.rs
  - https://github.com/DioxusLabs/docsite/blob/main/packages/docs-router/src/doc_examples/data_fetching.rs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Data fetching with use_resource and use_loader

Goal: load async data reactively and in parallel.

Dioxus has no built-in HTTP client. Add reqwest and serde:

```sh
cargo add reqwest --features json
cargo add serde --features derive
```

## use_resource

`use_resource` derives async state. It tracks `.read()` calls of signals inside the future and restarts immediately when one is written:

```rust
let mut breed = use_signal(|| "hound".to_string());
let dogs = use_resource(move || async move {
    reqwest::Client::new()
        .get(format!("https://dog.ceo/api/breed/{breed}/images"))
        .send().await?
        .json::<BreedResponse>().await
});
// dogs.read() is None while running; Some(Ok(..)) / Some(Err(..)) afterwards
```

Unlike `use_memo`, the output is not compared with `PartialEq`: readers rerun whenever the future reruns, even if the value is identical. The future must be cancel safe (see the async skills): a task that inserts into global state and removes it after the await leaks the entry if the resource restarts, so use a guard with a `Drop` impl.

## use_loader

`use_loader` is for reactive futures returning `Result<T, E>`. It returns `Result<Loader<T>, Loading>`, which integrates with error boundaries and suspense, so `?` early-returns while pending or errored:

```rust
let breed_list = use_loader(move || async move {
    reqwest::get("https://dog.ceo/api/breeds/list/all").await?.json::<ListBreeds>().await
})?;
```

The docs recommend `use_resource` for client-side fetching and `use_loader` for hybrid client/server fetching.

## Avoid waterfalls

If you `return` early from the component while the first resource is loading, later `use_resource` calls never start, so requests run one after another. Create all resources first, then do the early returns:

```rust
let poodle_img = use_resource(|| fetch_dog_image("poodle"));
let golden_retriever_img = use_resource(|| fetch_dog_image("golden retriever"));
let pug_img = use_resource(|| fetch_dog_image("pug"));
// now match each one and return the loading placeholder if not Some(Ok(..))
```

## Gotchas

- Without `use_resource`, a handler that fetches can fire many requests on rapid clicks; guard with a `loading` signal.
- Limit data fetching to a few centralized sources; load related data (name and id) in one request where possible.

## Checked

2026-11-08. Confirmed against the Dioxus 0.7 data fetching page (read in full) and its asynchronous.rs and data_fetching.rs example files: reqwest and serde setup, use_resource tracking and restarting, no PartialEq memoization, cancel safety, use_loader returning Result<Loader<T>, Loading>, the recommendation for each, and the early-return waterfall.

Method: documentation only; no commands were run.
