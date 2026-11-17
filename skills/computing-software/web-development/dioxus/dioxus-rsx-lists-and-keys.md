---
id: computing-software.web-development.dioxus.dioxus-rsx-lists-and-keys
name: dioxus-rsx-lists-and-keys
category: computing-software
field: web-development
product: dioxus
tags: [dioxus, rsx, for-loop, iterators, key, fragment, store, readsignal]
level: practitioner
status: docs-checked
description: "Render lists in Dioxus RSX with inline for or iterators, choose stable keys, use Fragment to key multi-root items, and pass collection items to child components."
sources:
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/essentials/ui/iteration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Rendering lists and keys

Goal: render collections without losing component state.

## Iterate

Any iterator yielding `Element` works inside RSX, or use the inline `for` sugar (its body is RSX):

```rust
rsx! {
    {(0..10).map(|idx| rsx! { "item {idx}" })}

    for user in users.iter() {
        User { id: user.id }
    }
}
```

For temporary variables inside a loop, use an inline expression block that returns `rsx!`. With a `Signal<T>` wrapper, call `.iter()` first: `for item in items.iter() { li { "{item}" } }`.

## Keys

Each list item should carry a unique key that is stable across renders, so Dioxus can track items as they move:

```rust
rsx! {
    for user in users {
        div { key: "{user.id}", "{user.name}" }
    }
}
```

Names and timestamps can collide and may be missing; when no field is reliably unique, mint an id from a generation counter:

```rust
let mut generation = use_signal(|| 0);
let mut items = use_signal(|| vec![]);
let mut add_item = move |name| {
    let id = generation();
    generation.set(id + 1);
    items.write().push(Item { id, name })
};
```

The worst key is the item index (`key: "{idx}"`): it changes as the list mutates and causes performance problems or lost component state.

## Fragment

If the iterator body has several root elements, RSX uses the first element's key. When none is available, wrap in `Fragment { key: "{item.id}", ... }`.

## Passing items to children

Forwarding references was disabled (it relied on unsound Rust semantics). Instead: clone owned data if cheap, pass the collection and the index, or iterate a `Store` (`use_store(|| vec![])`), which hands out reactive items without cloning; the child takes `count: ReadSignal<i32>`. For complex apps the page recommends building around global context or a Store.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against the Dioxus 0.7 "Rendering Lists" docsite page (iterators, inline `for`, keys, Fragment, borrowed state). Nothing removed.
