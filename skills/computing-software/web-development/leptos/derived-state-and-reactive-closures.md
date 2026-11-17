---
id: computing-software.web-development.leptos.derived-state-and-reactive-closures
name: derived-state-and-reactive-closures
category: computing-software
field: web-development
product: leptos
tags: [leptos, rust, derived-signal, memo, closures, reactivity]
level: practitioner
status: docs-checked
description: "Model dependent state in Leptos with derived closures or Memo instead of effects, and remember components run once so only closures are reactive."
sources: [https://book.leptos.dev/reactivity/working_with_signals.html, https://book.leptos.dev/reactivity/interlude_functions.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: make one value depend on another the idiomatic way, and understand why Leptos code is full of closures.

## Mental model

Your component function is a setup function and runs once, not a render function. Values in the view are reactive only if they are signals or closures that read signals. The framework reruns the smallest unit (a closure) when a dependency changes; it hands `increment` to the browser as an event listener and updates a single text node.

```rust
let (count, set_count) = signal(0);
let double_count = move || count.get() * 2;       // derived signal
let count_is_odd = move || count.get() & 1 == 1;
let text = move || if count_is_odd() { "odd" } else { "even" };
Effect::new(move |_| { logging::log!("text = {}", text()); });
view! { <p>{move || text().to_uppercase()}</p> }
```

## Making signals depend on each other

1. B is a function of A: signal for A plus a derived signal or `Memo`.

```rust
let (count, set_count) = signal(1);
let derived_signal_double_count = move || count.get() * 2;
let memoized_double_count = Memo::new(move |_| count.get() * 2);
```

2. C is a function of A and B: two signals and one derived signal.

```rust
let full_name = move || format!("{} {}", &*first_name.read(), &*last_name.read());
```

3. A and B independent but sometimes updated together: just call both setters in the handler.
4. Discouraged: an effect that writes B when A changes. It costs two full passes through the reactive system and risks loops and over-running effects. Prefer clear top-down flow.

For derived signal versus memo, the page defers to the `Memo` API docs.

## Gotchas

- On nightly, signals are callable functions, so `impl Fn() -> T` accepts signals, memos and derived signals uniformly; on stable you call `.get()`.
- Related: `computing-software.web-development.leptos.effects-and-effect-watch`, `computing-software.web-development.leptos.signal-read-write-access-methods`.

## Checked

2026-11-07: every claim, snippet and step above was compared with the full text of the cited Leptos book pages (https://book.leptos.dev/reactivity/working_with_signals.html, https://book.leptos.dev/reactivity/interlude_functions.html) and the book source on GitHub. Statements the pages do not state were removed or trimmed.

Method: documentation only; no commands were run.
