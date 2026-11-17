---
id: computing-software.web-development.leptos.resources-loading-async-data
name: resources-loading-async-data
category: computing-software
field: web-development
product: leptos
tags: [leptos, rust, resource, local-resource, once-resource, async]
level: practitioner
status: docs-checked
description: "Load async data reactively in Leptos with Resource, LocalResource or OnceResource, understand source vs fetcher tracking, and read the Option result."
sources: [https://book.leptos.dev/async/, https://book.leptos.dev/async/10_resources.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: integrate a `Future` into the reactive system.

If none of the primitives fit, `spawn_local` (cross-platform) runs a `Future`; combine it with setting a signal.

## Choosing

- `Resource`: default under server-side rendering. Its value is serialised from server to client, and on first load the client deserialises it instead of re-running the task, so data loading starts on the server.
- `LocalResource`: client-side rendering with `!Send` APIs, or SSR with a task that can only run in the browser.
- `OnceResource`: runs once; takes a `Future` directly.

## LocalResource

One argument, a fetcher returning a `Future`. It behaves like a derived signal: signals read inside are tracked and a change creates a new `Future`.

```rust
let (count, set_count) = signal(0);
let async_data = LocalResource::new(move || load_data(count.get()));
```

## Resource

Two functions: a source (memoised input; when it changes, the fetcher runs) and a fetcher taking that value.

```rust
let async_data = Resource::new(
    move || count.get(),
    |count| load_data(count)
);
```

Signals in the source are tracked; signals in the fetcher are not. This lets the resource stay reactive without rerunning the fetcher during hydration.

```rust
let once = OnceResource::new(load_data(42));
```

## Accessing

Creating a resource calls the fetcher immediately. `.read()`, `.with()` and `.get()` return `Option<T>`: `None` while pending, `Some(value)` when done. You can also `.await` a resource. `refetch()` reloads manually (for example from a button click). A `LocalResource` that reads no signals loads only once.

```rust
let async_result = move || async_data.get()
    .map(|value| format!("Server returned {value:?}"))
    .unwrap_or_else(|| "Loading...".into());
```

Next: `computing-software.web-development.leptos.suspense-await-and-transition`.

## Checked

2026-11-07: Read in full: async/10_resources.md (Local Resources, Resources, OnceResource, refetch, Accessing Resources and the inline sandbox source) and async/README.md (the spawn_local advice). Confirmed Resource versus LocalResource guidance, source-tracked versus fetcher-untracked signals, serialisation from server to client, and that a LocalResource reading no signals loads once (sandbox comment 'a resource will only load once if it doesn't read any reactive data'). No claims were trimmed. The live sandbox was not opened.

Method: documentation only; no commands were run.
