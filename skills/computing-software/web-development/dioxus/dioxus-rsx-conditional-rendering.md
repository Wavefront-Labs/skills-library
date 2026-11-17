---
id: computing-software.web-development.dioxus.dioxus-rsx-conditional-rendering
name: dioxus-rsx-conditional-rendering
category: computing-software
field: web-development
product: dioxus
tags: [dioxus, rsx, conditional-rendering, intodynnode, inline-if, match, expressions]
level: practitioner
status: docs-checked
description: "Render conditionally in Dioxus RSX with brace expressions, match, if/else, IntoDynNode, and inline if blocks that give a placeholder without else."
sources:
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/essentials/ui/conditional.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Conditional rendering in RSX

Goal: choose what to render with plain Rust.

## Expressions

Wrap any expression that evaluates to an `Element` (or anything implementing `IntoDynNode`) in `{}`:

```rust
let header = match current_timezone() {
    TimeZone::PST => rsx! { h1 { "Welcome home" } },
    _ if app.snoozed() => rsx! { h1 { "snoozed..." } },
    _ => rsx! { h1 { "Bon voyage!" } },
}

rsx! { div { {header} } }
```

Use `if/else` where JavaScript would use a ternary:

```rust
let screen = if authenticated { render_app() } else { render_login() };
rsx! { div { {screen} } }
```

## What IntoDynNode accepts

An expression converts to one of four `DynamicNode` variants: Component, Text (Rust `String`), Placeholder (an optimised `None`) and List (a Vec of Elements). Valid expressions include empty braces, other `Element` values, `str`/`String`/`Arguments` (e.g. `{format_args!("lazy fmt -> {}", arg())}`), an `Option` whose inner type qualifies, and any iterator:

```rust
let cards = (0..10).map(|i| rsx! { li { "Card: {i}" } });
rsx! { ol { {cards} } }
```

## Inline if

RSX has syntax sugar for inline `if`. The body is RSX, not a Rust expression:

```rust
rsx! {
    div {
        if logged_in() { LoggedInScreen {} } else { LoggedOutScreen {} }
    }
}
```

Unlike Rust, an inline `if` still yields an `Element` without an `else`; RSX substitutes a placeholder:

```rust
rsx! { div { if logged_out() { span { "You should log in!" } } } }
```

## Gotcha

The docs state there are no plans to add further syntax sugar beyond inline `if` and `for`.

## Checked

2026-11-08. Confirmed against the Dioxus 0.7 conditional rendering page (read in full): brace expressions, match guards, if/else, the four DynamicNode variants, valid IntoDynNode expressions, inline if with a placeholder when there is no else, and the statement that no further syntax sugar is planned.

Method: documentation only; no commands were run.
