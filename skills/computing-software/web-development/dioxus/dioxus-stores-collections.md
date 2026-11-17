---
id: computing-software.web-development.dioxus.dioxus-stores-collections
name: dioxus-stores-collections
category: computing-software
field: web-development
product: dioxus
tags: [dioxus, store, use-store, derive-store, lens, readstore, hashmap, transpose]
level: advanced
status: docs-checked
description: "Use Dioxus reactive Stores: derive Store, use_store, field lenses, nested stores, Option and Result lenses, per-entry HashMap reactivity."
sources:
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/essentials/basics/collections.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Reactive Stores and collections in Dioxus

Goal: make reactivity precise for struct fields and collection entries.

```rust
#[derive(Store)]
struct HeaderState {
    title: String,
    subtitle: String
}

let header = use_store(|| HeaderState {
    title: "Hello, ".to_string(),
    subtitle: "world!".to_string(),
});
let title = header.title();   // a lens "zoomed in" on one field
```

The derive generates a method per field. The lens is zero-cost but its type cannot be named, so functions take it as a generic:

```rust
fn get_title(state: Store<HeaderState, impl Readable<Target = HeaderState>>) -> String {
    state.title().cloned()
}
fn clear_title(state: Store<HeaderState, impl Writable<Target = HeaderState>>) {
    state.title().take();
}
```

At a component boundary stores convert automatically: a lens becomes `ReadSignal<String>` or `ReadStore<String>` props. Stores support `.read()`, `.write()`, `.set()`, `Display` and are `Copy`.

## Nested and enum fields

Nesting only works when the nested type also derives `Store` (`header.other().title2()`); foreign types without it cannot be lensed. For `Option` or `Result` fields, lenses have `.unwrap()`. Use `.transpose()` (Store<Option<T>> to Option<Store<T>>) to keep zooming, or `.as_ref()` which calls `.read()` internally and loses precise zoom:

```rust
let len = match header.subtitle().transpose() {
    Some(subtitle) => subtitle.read().len(),
    None => 0,
};
```

## Collections

A `Signal<HashMap<..>>` read with `users.read().iter()` cannot pass borrowed items to a child component (lifetime is not `'static`). Switch to a store:

```rust
let mut users = use_store(|| HashMap::<UserId, UserData>::new());
rsx! { for (id, user) in users.iter() { ListItem { key: "{id}", user } } }

#[component]
fn ListItem(user: ReadSignal<UserData>) -> Element { rsx! { li { "{user.read().name}" } } }
```

`Store<HashMap<K, V>>` is reactive per entry: insert or remove queues one re-render; editing one entry re-renders only its `ListItem`. Derive `Store` on `UserData` and accept `ReadStore<UserData>` to lens into fields (`user.name()`).

## Methods with #[store]

`#[store] impl<Lens> Store<UserData, Lens> { ... }` creates an extension trait: `&self` methods bound `Lens` by `Readable`, `&mut self` by `Writable`, and by-value `self` adds no bound.

## Gotcha

The docs say signals and structs are usually enough; stores pay off with foreign data types and huge collections.

## Checked

2026-11-08. Confirmed against the Dioxus 0.7 stores and collections page (read in full): derive Store, use_store, field lenses, Readable/Writable lens bounds, ReadSignal/ReadStore props, nested stores, Option/Result unwrap, transpose versus as_ref, per-entry HashMap reactivity, ReadStore<UserData>, and the #[store] attribute bounds.

Method: documentation only; no commands were run.
