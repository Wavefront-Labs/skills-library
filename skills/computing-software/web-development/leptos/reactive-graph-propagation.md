---
id: computing-software.web-development.leptos.reactive-graph-propagation
name: reactive-graph-propagation
category: computing-software
field: web-development
product: leptos
tags: [leptos, rust, reactive-graph, signals, memo, effects, performance]
level: practitioner
status: docs-checked
description: "Understand how Leptos propagates changes through its Clean/Check/Dirty reactive graph, solves the diamond problem, and when to choose memos over derived signals."
sources: [https://book.leptos.dev/appendix_reactive_graph.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# How the Leptos reactive graph runs effects

Goal: reason about when effects and memos re-run, and choose between memos and derived signals.

## Model

Primitives: signals (`ReadSignal`/`WriteSignal`, `RwSignal`, `Resource`, `Trigger`) are root nodes; memos (`Memo`) derive values; effects are leaf nodes. Each node has a value, sources and subscribers. Derived signals (plain closures) are not nodes. The primary goal is to run effects as rarely as possible, since effects (DOM, network) cost far more than updating Rust data. The algorithm is based on the Reactively library.

## Memos only notify on change

```rust
let (name, set_name) = signal("Alice");
let name_upper = Memo::new(move |_| name.with(|n| n.to_uppercase()));
let name_len = Memo::new(move |_| name.len());
Effect::new(move |_| log!("len = {}", name_len()));
Effect::new(move |_| log!("name = {}", name_upper()));
set_name("Bob");   // logs len = 3 and name = BOB
set_name("Tim");   // logs only name = TIM; length is still 3
```

## Diamond problem

When one effect depends on two memos that share a signal, a naive push system would run it twice (once with a stale value). Leptos marks nodes `Clean`, `Check` (maybe changed) or `Dirty` (definitely changed). Setting a signal marks it Dirty and descendants Check, queuing effects. A queued effect checks parents: a Check parent checks its own sources, re-runs if one is Dirty, and reports whether its value changed; the effect re-runs only if some parent changed, and runs once. This is "push-pull" and favors not over-notifying over raw propagation speed.

## Memos vs signals vs derived signals

- Signals always notify subscribers when set, even to an equal value (avoids requiring `PartialEq`).
- Memos compare to the previous value and notify only on change; if the computation is very expensive, memoize its inputs too.
- Memos cost a `PartialEq` check, extra memory for a node, and graph traversal. Most real graphs are shallow and wide, so prefer derived signals for cheap computations:

```rust
let b = move || a() + 2;
let c = move || b() % 2 == 0;
let d = move || if c() { "even" } else { "odd" };
```

At most memoize the final node before an expensive side effect:

```rust
let text = Memo::new(move |_| d());
Effect::new(move |_| engrave_text_into_bar_of_gold(&text()));
```

Related: computing-software.web-development.leptos.signal-ownership-lifecycle.

## Checked

2026-11-07: Read in full: appendix_reactive_graph.md (three primitive sets, node value/sources/subscribers, the three worked examples with the len = 3 log sequence, Solving the Diamond Problem with Clean/Check/Dirty, Memos vs Signals, Memos vs Derived Signals and the bar-of-gold example). Every statement in the skill traces to those sections, including 'signals always notify, even to an equal value' and the memo overhead list. No claims were trimmed. The linked Reactively library and Milo's article were not opened.

Method: documentation only; no commands were run.
