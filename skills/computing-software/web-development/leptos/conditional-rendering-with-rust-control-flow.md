---
id: computing-software.web-development.leptos.conditional-rendering-with-rust-control-flow
name: conditional-rendering-with-rust-control-flow
category: computing-software
field: web-development
product: leptos
tags: [leptos, rust, control-flow, conditional-rendering, option, match]
level: practitioner
status: docs-checked
description: "Render different views in Leptos using plain if, match, Option and bool::then inside reactive closures, with no special components."
sources: [https://book.leptos.dev/view/06_control_flow.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: decide what to render from a signal using ordinary Rust expressions.

## Method

Rust control flow returns values, and any `T: IntoView` also works as `Option<T>` and `Result<T, impl Error>`. A function returning those types is reactive. To be reactive, the expression must be wrapped in a closure (`move ||`) that reads a signal.

```rust
let (value, set_value) = signal(0);
let is_odd = move || value.get() % 2 != 0;
```

`if` / `else` inside a closure:

```rust
view! { <p>{move || if is_odd() { "Odd" } else { "Even" }}</p> }
```

Render something or nothing with `Option`, or the shorter `bool::then`:

```rust
let message = move || is_odd().then(|| "Ding ding ding!");
view! { <p>{message}</p> }
```

`match` works the same way and supports guards:

```rust
let message = move || match value.get() {
    0 => "Zero",
    1 => "One",
    n if is_odd() => "Odd",
    _ => "Even",
};
```

Helpers such as `Option::map`, `Option::and_then`, `Option::ok_or`, `Result::map`, `Result::ok` and `bool::then` convert between renderable types declaratively. Pulling the closure out of `view!` can give better `cargo fmt` and rust-analyzer support.

## Gotchas

- Each of these closures is a derived signal and reruns every time its signal changes, even when the output branch is unchanged. For cheap output (a text node) that is fine; for expensive branches use `computing-software.web-development.leptos.show-component-avoid-rerender`.
- Branches that return different view types do not compile; see `computing-software.web-development.leptos.conditional-branch-type-unification`.
- Toggling a class (`class:hidden=is_odd`, from the page's live example) keeps the element alive between states instead of destroying it.

## Checked

2026-11-07: every claim, snippet and step above was compared with the full text of the cited Leptos book pages (https://book.leptos.dev/view/06_control_flow.html) and the book source on GitHub. Statements the pages do not state were removed or trimmed.

Method: documentation only; no commands were run.
