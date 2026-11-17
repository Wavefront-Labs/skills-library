---
id: computing-software.web-development.dioxus.dioxus-custom-hooks
name: dioxus-custom-hooks
category: computing-software
field: web-development
product: dioxus
tags: [dioxus, custom-hooks, use-hook, needs-update, use-on-destroy, consume-context, use-signal]
level: advanced
status: docs-checked
description: "Write Dioxus custom hooks: wrap existing hooks, build on use_hook, trigger re-renders with needs_update, and clean up with use_on_destroy."
sources:
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/essentials/advanced/custom_hooks.md
  - https://github.com/DioxusLabs/docsite/blob/main/packages/docs-router/src/doc_examples/hooks_composed.rs
  - https://github.com/DioxusLabs/docsite/blob/main/packages/docs-router/src/doc_examples/hooks_custom_logic.rs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Writing custom hooks in Dioxus

Goal: encapsulate reusable logic in a function whose name starts with `use_`.

## Compose existing hooks

A shortcut for a context value:

```rust
fn use_settings() -> Signal<AppSettings> {
    consume_context()
}
```

A persistent-storage hook can be built on `use_signal`: the docs' `use_persistent<T>(key, init)` creates `use_signal(move || { ... LocalStorage::get(key.as_str()).ok().unwrap_or_else(init) ... })`, wraps the signal in a `Copy` struct `UsePersistent<T>`, and its `set` writes to `LocalStorage` as well as to the signal (it uses the `gloo_storage` crate).

## Build on use_hook

`use_hook` takes one closure, run only the first time the component renders. Its return value is stored for as long as the component lives, and on every render (not just the first) you get a reference to it. All standard hooks are built on it. Use `use_on_destroy` to clean up resources when the component is destroyed.

The docs' simplified `use_signal` and `use_context` implementations:

```rust
pub fn use_context<T: 'static + Clone>() -> T {
    use_hook(|| consume_context())
}

pub fn use_context_provider<T: 'static + Clone>(f: impl FnOnce() -> T) -> T {
    use_hook(|| {
        let val = f();
        provide_context(val.clone());
        val
    })
}
```

A signal-like hook stores `Rc<RefCell<T>>` plus a set of subscribers in `use_hook`; `get` subscribes `ReactiveContext::current()` and `set` marks subscribers dirty.

## Reactive hooks with needs_update

`use_hook` only stores a value. To queue a re-render call `dioxus::core::needs_update()`:

```rust
button {
    onclick: move |_| dioxus::core::needs_update(),
    "Queue for re-rendering"
}
```

Combine `needs_update`, `use_hook` and interior mutability (for example a `ReactiveString` holding `Rc<RefCell<String>>` whose `set` calls `needs_update()`). The docs note you should never need to build state-management primitives yourself; use the built-in ones.

## Checked
Checked 2026-11-07 against the 0.7 Custom Hooks page and its snippet files hooks_composed.rs and hooks_custom_logic.rs (all read in full). Confirmed: use_settings wrapper, use_persistent with gloo_storage LocalStorage, use_hook semantics and use_on_destroy, simplified signal and context hooks, needs_update and the ReactiveString example. Nothing removed.
Method: documentation only; no commands were run.
