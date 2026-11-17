---
id: computing-software.web-development.dioxus.dioxus-use-memo-use-effect
name: dioxus-use-memo-use-effect
category: computing-software
field: web-development
product: dioxus
tags: [dioxus, use-memo, use-effect, peek, use-reactive, readsignal, untracked-state, partialeq]
level: practitioner
status: docs-checked
description: "Use Dioxus use_memo for derived state and use_effect for side effects; opt out with peek; keep props reactive with ReadSignal or use_reactive."
sources:
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/essentials/basics/effects.md
  - https://github.com/DioxusLabs/docsite/blob/main/packages/docs-router/src/doc_examples/untested_06/reactivity.rs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Memos, effects, peek and untracked props in Dioxus

Goal: derive state and run side effects without extra component re-renders.

## use_memo

`use_memo` takes a closure and returns a tracked value that reruns when a dependency changes. The memo's value only updates (and notifies readers) when the new value differs by `PartialEq` from the old. Memos implement `Readable` but not `Writable`.

```rust
let mut count = use_signal(|| 0);
let half_count = use_memo(move || count() / 2);
```

Doing the computation inside a memo means the component only re-renders when the computed value changes, not when each input changes. Memos can even hold `Element`s: `let loading_ui = use_memo(move || { let n = loading_text.read().chars().count(); rsx! { "there are {n} characters!" } });` rendered with `{loading_ui}`.

## use_effect

Anything read in the closure becomes a dependency; the effect reruns when it changes:

```rust
use_effect(move || {
    let current_count = count();
    log!("{current_count}");
});
```

Effects run after the UI has been painted. The docs say to prefer plain actions in handlers over effects when the component cannot be unmounted in between (for example setting the document title in `oninput`), since effects are frequently misused.

## peek: read without subscribing

`*toggle.peek()` reads a signal without making it a dependency of the current reactive context, which avoids an effect that sets a signal it also reads looping forever.

## Untracked values and props

A plain value (such as an `i32` prop) read inside a memo does not subscribe. Two fixes from the page:

```rust
// 1. wrap the prop in ReadSignal (T is converted automatically at the call site)
#[component]
fn Count(count: ReadSignal<i32>) -> Element {
    let double_count = use_memo(move || count() * 2);
    rsx! { div { "Double count: {double_count}" } }
}

// 2. track a raw value with use_reactive!
let double_count = use_memo(use_reactive!(|(count,)| count * 2));
```

## Gotcha

The reactivity.rs example file spells the prop type `ReadOnlySignal`; the page prose uses `ReadSignal`.

## Checked

2026-11-08. Confirmed against the Dioxus 0.7 effects and memos page (read in full) and its reactivity.rs example file: use_memo with PartialEq, Readable but not Writable, memoized Elements, use_effect dependencies, running after paint, preferring actions over effects, peek, use_reactive!, and ReadSignal props.

Method: documentation only; no commands were run.
