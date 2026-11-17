---
id: computing-software.web-development.leptos.signal-read-write-access-methods
name: signal-read-write-access-methods
category: computing-software
field: web-development
product: leptos
tags: [leptos, rust, signals, read, write, local-signals]
level: practitioner
status: docs-checked
description: "Pick between .get, .read, .with, .set, .write and .update on Leptos signals, and use the _local variants for non-Send browser types."
sources: [https://book.leptos.dev/reactivity/working_with_signals.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: access and mutate signals without needless clones, and store `!Send` values correctly.

## Getting

- `.get()` clones the value and tracks it. Most common.
- `.read()` returns a guard dereferencing to the value, tracked; good for methods taking `&self` (`my_vec_signal.read().len()`). You cannot update the signal until the guard drops, or it is a runtime error.
- `.with(|v| ...)` gives `&T` and tracks; use when you need more than one call but want to bound the lock.

## Setting

- `.set(v)` replaces the value and notifies subscribers.
- `.write()` returns a mutable guard and notifies; you cannot read until it drops (runtime error otherwise).
- `.update(|v| ...)` gives `&mut T`. It does not return the closure's value; use `.try_update()` for that (for example, to get back an item removed from a `Vec`).

`count.get()` equals `count.read().clone()`; `count.set(1)` equals `*count.write() = 1`.

## Avoid hidden clones

```rust
// clones the whole Vec, then discards it, then replaces it
let (names, set_names) = signal(Vec::new());
if names.get().is_empty() { set_names(vec!["Alice".to_string()]); }

// borrow and mutate in place
if names.read().is_empty() { set_names.write().push("Alice".to_string()); }
```

## Thread safety

Values in signals must be `Send + Sync` because the reactive graph supports multi-threading (for SSR on multi-threaded runtimes). `wasm-bindgen` and `web-sys` types are `!Send`, so use the local variants only for such data:

- `signal` -> `signal_local`
- `RwSignal::new` -> `RwSignal::new_local`
- `Resource` -> `LocalResource`
- `Action::new` -> `Action::new_local` or `Action::new_unsync`

## Gotchas

- These traits come from blanket implementations (`Read` from `Track` + `ReadUntracked`, `With` from `Read`, `Get` from `With` + `Clone`; similarly for writing), so docs may list only the base traits.
- With the `nightly` feature, `count()` is sugar for `.get()` and `set_count(1)` for `.set(1)`.

## Checked

2026-11-07: Read in full: reactivity/working_with_signals.md (Getting and Setting, the blanket-implementation note, the Vec<String> clone example, Thread Safety and the local-variant table, Nightly Syntax, making signals depend on each other). Every bullet matches; the get/set equivalences are the page's own. No claims were trimmed. Not opened: the docs.rs method pages and the Interlude on functions.

Method: documentation only; no commands were run.
