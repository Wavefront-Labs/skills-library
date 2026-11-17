---
id: computing-software.web-development.leptos.effects-and-effect-watch
name: effects-and-effect-watch
category: computing-software
field: web-development
product: leptos
tags: [leptos, rust, effects, effect-new, effect-watch, auto-tracking]
level: practitioner
status: docs-checked
description: "Use Effect::new and Effect::watch in Leptos to sync signals with the outside world, with automatic dependency tracking and SSR behaviour."
sources: [https://book.leptos.dev/reactivity/14_create_effect.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: run side effects (logging, DOM, web APIs) when signals change.

## Effect::new

```rust
let (a, set_a) = signal(0);
Effect::new(move |_| {
  // runs once now, subscribes to `a`
  logging::log!("Value: {}", a.get());
});
```

- Runs on the next tick of the reactive system (in a component, just after it renders).
- The closure receives the value it returned last time (`None` on the first run).
- Effects do not run on the server by default, so browser-only APIs are safe. Use `Effect::new_isomorphic` to also run on the server.
- No dependency array: tracking is automatic (any signal read) and dynamic (the list is rebuilt each run, so only signals in the branch actually taken count). With `if use_last.get() { first + last } else { first }`, changes to `last` are ignored while `use_last` is false.

## When not to use one

Effects synchronise the reactive system with the non-reactive world. Copying one signal into another is always sub-optimal:

```rust
// not great
Effect::new(move |_| { set_b.set(a.get() * 2); });
// better
let b = move || a.get() * 2;
```

Use a derived signal or `Memo`. Writing a signal in an effect is fine when syncing with external things (web API, console, filesystem, DOM). The page points to `leptos-use` for ready-made reactive wrappers.

## Explicit tracking: Effect::watch

`Effect::watch(dependency_fn, handler, immediate)` tracks only `dependency_fn`; the handler is untracked. With `immediate` false the handler runs only after the first change. It returns an `Effect` with `.stop()`.

```rust
let effect = Effect::watch(
    move || num.get(),
    move |num, prev_num, _| { leptos::logging::log!("Number: {}; Prev: {:?}", num, prev_num); },
    false,
);
set_num.set(1); // logs "Number: 1; Prev: Some(0)"
effect.stop();
set_num.set(2); // nothing
```

## Note

The renderer itself uses effects: `<p>{count}</p>` is an effect that updates the text node.

Related: `computing-software.web-development.leptos.derived-state-and-reactive-closures`.

## Checked

2026-11-07: every claim, snippet and step above was compared with the full text of the cited Leptos book pages (https://book.leptos.dev/reactivity/14_create_effect.html) and the book source on GitHub. Statements the pages do not state were removed or trimmed.

Method: documentation only; no commands were run.
