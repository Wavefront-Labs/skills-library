---
id: computing-software.web-development.dioxus.dioxus-antipatterns
name: dioxus-antipatterns
category: computing-software
field: web-development
product: dioxus
tags: [dioxus, antipatterns, keys, use-memo, use-effect, use-hook, partialeq, interior-mutability]
level: practitioner
status: docs-checked
description: "Avoid Dioxus pitfalls: missing or index keys, Mutex/RefCell props, state updates during render, one huge state signal, random values in the body, permissive PartialEq."
sources:
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/guides/tips/antipatterns.md
  - https://github.com/DioxusLabs/docsite/blob/main/packages/docs-router/src/doc_examples/anti_patterns.rs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Dioxus antipatterns and fixes

Goal: recognise common mistakes and use the documented replacement.

## Keys
Do not omit keys unless the list never changes, and do not key by index. Key by a unique id: `li { key: "{key}", "List item: {value}" }`.

## Interior mutability in props
`Rc<RefCell<..>>`, `Mutex` or `RwLock` props are hard to use: writing to them does not rerun any components, so the UI goes stale. Pass a reactive value instead:

```rust
#[component]
fn Comp(map: Signal<HashMap<u32, String>>) -> Element {
    rsx! {
        button { onclick: move |_| { map.write().insert(0, "Hello".to_string()); }, "Mutate map" }
        "{map.read().get(&0).unwrap()}"
    }
}
```

## Updating state during render
It is inefficient, and an unconditional update loops forever. Use an effect, or better a memo for derived state:

```rust
use_effect(move || {
    if first_signal() + 1 != second_signal() {
        second_signal.set(first_signal() + 1);
    }
});
let second_signal = use_memo(move || first_signal() + 1);
```

## Large groups of state
One big struct signal makes accidental read-and-write loops easy, is hard to reason about, and rerenders many components. Use several signals, and `use_memo` in children to derive just the part they need (for example `users.read().first().unwrap().clone()`).

## Non-deterministic code in the body
`rand::random::<u64>()` in the body runs on every rerender, so the id changes each time. Store it with `use_hook(|| rand::random::<u64>())` or run it in an effect.

## Overly permissive PartialEq
A `PartialEq` that always returns `true` stops the component from ever rerendering when the parent does. Derive `PartialEq`; if you must write it by hand, return `false` whenever props may have changed. Returning `false` when unsure is better than `true`, e.g. compare an `Rc` with `Rc::ptr_eq`.

## Checked
Checked 2026-11-07 against the 0.7 antipatterns page and its included snippet file anti_patterns.rs (both read in full). Confirmed: keys by unique id, interior mutability in props with the Signal fix, updating state during render with use_effect and use_memo, large state with use_memo in children, non-deterministic code with use_hook, permissive PartialEq with Rc::ptr_eq. Nothing removed; snippet file added to sources.
Method: documentation only; no commands were run.
