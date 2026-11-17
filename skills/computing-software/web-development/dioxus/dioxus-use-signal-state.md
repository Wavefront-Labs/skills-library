---
id: computing-software.web-development.dioxus.dioxus-use-signal-state
name: dioxus-use-signal-state
category: computing-software
field: web-development
product: dioxus
tags: [dioxus, use-signal, signal, read, write, set, toggle, readable, writable]
level: intro
status: docs-checked
description: "Create and update Dioxus mutable state with use_signal: read, call, set and write, plus the Display, toggle, math and iter conveniences."
sources:
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/essentials/basics/signals.md
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/essentials/basics/index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Dioxus signals as component state

Goal: hold mutable state in a component and update the UI by reading and writing a `Signal`.

```rust
let mut signal = use_signal(|| 0);

let inner = signal.read();          // a reference to the inner value
let name = use_signal(|| "Bob".to_string());
let a = name();                     // call like a function: a Clone of the value
let b = name.cloned();              // same thing
signal.set(1);                      // replace the value
let mut value = signal.write();     // mutable reference
*value += 1;
```

Reads and writes are explicit: Dioxus has no Proxy equivalent, so reactivity is traced through `.read()` and `.write()`. Assign through a write guard with the dereference operator, e.g. `onclick: move |_| *count.write() = current + 1`.

## Ergonomic extensions

Mutable signals implement `Readable` and `Writable`, which add:

- `Signal<T>` implements `Display` when `T` does, so `rsx! { "Count is: {count}" }` works (and reads the signal).
- `Signal<bool>` has `toggle()`: `button { onclick: move |_| enabled.toggle(), ... }`.
- Numeric signals support operators: `button { onclick: move |_| count += 1, "Up high!" }` and `count -= 1`.
- Signals over `IntoIterator` types have `.iter()`: `for name in names.iter() { li { "hello {name}" } }`.

Use these unless the inner type does not implement the required traits.

## Gotchas stated by the docs

- State may be kept in a struct wrapped in one signal: `let mut state = use_signal(EditorState::new);` and then `state.write().handle_input(event)` in a handler.
- Calling `.read()` on a signal while rendering subscribes the component; calling `.write()` or `.set()` queues work for the subscribers.

## Checked

2026-11-08. Confirmed against the Dioxus 0.7 signals page and the state basics page (both read in full): use_signal, read, call syntax, cloned, set, write, explicit reads and writes, Display, toggle, math operators and iter extensions, single-struct state with write(), and subscription on read.

Method: documentation only; no commands were run.
