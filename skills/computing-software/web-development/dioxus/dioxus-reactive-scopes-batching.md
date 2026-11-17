---
id: computing-software.web-development.dioxus.dioxus-reactive-scopes-batching
name: dioxus-reactive-scopes-batching
category: computing-software
field: web-development
product: dioxus
tags: [dioxus, reactivity, reactive-scope, signal, batching, use-memo, derived-state, one-way-data-flow]
level: practitioner
status: docs-checked
description: "How Dioxus reactivity works: three pillars, reactive scopes that subscribe on read, automatic batching of writes, immediate memo re-evaluation, and deriving values."
sources:
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/essentials/basics/reactivity.md
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/essentials/basics/signals.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Dioxus reactivity model: scopes and batching

Goal: predict what re-renders when a signal changes.

## Three pillars

- Data flows down: parents pass values and functions to children as props; a child cannot directly modify a parent's state.
- Data is tracked: `.set()` and `.write()` on a reactive value are observed and queue effects.
- Data is derived: compute from sources while rendering or in a memo, never by writing state during render.

```rust
let names = use_signal(|| vec!["Jane", "Jack", "Jill"]);
let num_names = names.read().len();   // derived from names
```

The docs mark storing the count in a second signal and setting it during render as the wrong form: modifying state while rendering queues re-renders and can loop forever.

## Reactive scopes

A reactive scope observes reads and writes. A component is the simplest one: calling `.read()` during render (explicit, or implicit through `Display` and other `Readable` extensions) subscribes it, and a write queues a re-render. If a component never reads a signal during render, it does not subscribe, so writing that signal causes no re-render:

```rust
let mut loading = use_signal(|| false);
rsx! { button { onclick: move |_| async move {
    if loading() { return; }
    loading.set(true);
    // .. do async work
    loading.set(false);
} } }
```

`use_effect`, `use_memo` and `use_resource` use reactive scopes that live outside the rendering lifecycle.

## Batching

All built-in hooks batch: `.write()` queues an effect before the next step instead of running it immediately, and side effects are de-duplicated. An `await` is a barrier between steps; after a step that modified state, Dioxus prefers to paint the new UI before polling more futures.

Consistency beats batching: reading a memo directly after writing a signal it depends on re-evaluates the memo immediately.

```rust
let mut count = use_signal(|| 0);
let double = use_memo(move || count() * 2);
// in an async handler: count += 1; println!("double is now: {}", double());
```

## Checked
Checked 2026-11-07 against the 0.7 Intro to Reactivity page and the ReadSignal, Reactive Scopes and Automatic Batching sections of the Signals page (read in full). Confirmed: three pillars, derived-data example and infinite loop warning, subscribe-on-read, unread signal causing no re-render, hooks using out-of-render scopes, batching and de-duplication, await barriers, immediate memo re-evaluation. Nothing removed.
Method: documentation only; no commands were run.
