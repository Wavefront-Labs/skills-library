---
id: computing-software.web-development.dioxus.dioxus-hoisting-readsignal-callbacks
name: dioxus-hoisting-readsignal-callbacks
category: computing-software
field: web-development
product: dioxus
tags: [dioxus, readsignal, writesignal, eventhandler, callback, hoisting, props, component]
level: practitioner
status: docs-checked
description: "Hoist shared state in Dioxus and design props: accept ReadSignal so signals, memos and plain values work, and pass EventHandler or Callback instead of mutable Signal props."
sources:
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/essentials/basics/hoisting.md
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/essentials/basics/signals.md
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/essentials/basics/event_handlers.md
  - https://github.com/DioxusLabs/docsite/blob/main/packages/docs-router/src/doc_examples/event_handler_prop.rs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Hoisting state, ReadSignal props and callbacks in Dioxus

Goal: share state between sibling components while keeping one-way data flow.

Hoist state to the nearest common ancestor. Split the UI first, then the state, and pass derived values down:

```rust
#[component]
fn EmailAndName() -> Element {
    let mut name = use_signal(|| "name".to_string());
    let mut email = use_signal(|| "email".to_string());
    let is_valid = use_memo(move || validate_name_and_email(name, email));
    rsx! {
        Validator { is_valid }
        div { class: if !is_valid() { "border-red" },
            input { oninput: move |e| name.set(e.value()) }
            input { oninput: move |e| email.set(e.value()) }
        }
    }
}
```

## Accept ReadSignal

A plain `bool` prop is not reactive, so an effect that logs it will not fire on change. Declare reactive props as `ReadSignal`; every `Readable` type (Signal, Memo, Resource) converts into it, and untracked values passed as properties convert too (`Validator { is_valid: true }`):

```rust
#[component]
fn Validator(is_valid: ReadSignal<bool>) -> Element {
    use_effect(move || log!("validity change: {is_valid}"));
    rsx! { if !is_valid { "Invalid name or email" } }
}
```

`ReadSignal` is read-only; `WriteSignal` is read-write and equivalent to `Signal`. Prefer these in interfaces over concrete reactive types, and the docs recommend wrapping every readable component property in `ReadSignal`.

## Callbacks instead of mutable props

Taking `mut sig: Signal<i32>` compiles (with warnings) but is discouraged. Expose a handler and let the parent update state:

```rust
#[component]
fn Incrementer(onclick: EventHandler<MouseEvent>) -> Element {
    rsx! { button { onclick, "Increment!" } }   // shorthand for onclick: onclick
}
// parent: Incrementer { onclick: move |_| count += 1 }
```

Call a handler with `.call(value)`. `EventHandler<T>` is a subset of `Callback<Args, Ret>`; use `Callback<MouseEvent, String>` (or `Callback<u32, u32>`) when the closure must return a value: `current.set(onclick.call(e))`.

## Gotcha

`EventHandler` and `Callback` carry a handle to the Dioxus runtime, so they can be passed to APIs such as file-system watchers where plain closures that touch app state outside the app might panic.

## Checked
Checked 2026-11-07 against the 0.7 Hoisting State page, the ReadSignal and WriteSignal section of the Signals page, the Event Handlers page (Custom Data, Returning a Value, Callbacks Carry the Runtime) and the event_handler_prop.rs snippet file. Confirmed: hoisting examples, ReadSignal decay and automatic conversion, WriteSignal equivalence to Signal, wrap every readable prop advice, mutable Signal props discouraged, EventHandler as a subset of Callback, Callback<MouseEvent, String> and Callback<u32, u32>, runtime handle gotcha. Nothing removed.
Method: documentation only; no commands were run.
