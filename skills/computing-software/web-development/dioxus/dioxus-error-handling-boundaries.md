---
id: computing-software.web-development.dioxus.dioxus-error-handling-boundaries
name: dioxus-error-handling-boundaries
category: computing-software
field: web-development
product: dioxus
tags: [dioxus, errorboundary, handle-error, render-error, captured-error, anyhow, context, error-context]
level: practitioner
status: docs-checked
description: "Handle errors in Dioxus: return Result from components and handlers with ?, catch them in ErrorBoundary handle_error, add anyhow context, and use CapturedError or dioxus::Ok."
sources:
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/essentials/basics/error_handling.md
  - https://github.com/DioxusLabs/docsite/blob/main/packages/docs-router/src/doc_examples/error_handling.rs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Error handling and ErrorBoundary in Dioxus

Goal: bubble rendering and handler errors to a boundary that renders a fallback.

`Element` is a type alias for `Result<VNode, RenderError>`, so `?` works in components. `RenderError` is an enum of `Error(CapturedError)` or `Suspended(SuspendedFuture)`, and converts from `anyhow::Error`:

```rust
#[component]
fn ThrowsError() -> Element {
    let number: i32 = use_hook(|| "1.234").parse()?;
    todo!()
}
```

## Catch with ErrorBoundary

```rust
rsx! {
    ErrorBoundary {
        handle_error: |_| {
            rsx! { "Oops, we encountered an error. Please report this to the developer of this application" }
        },
        ThrowsError {}
    }
}
```

An error returned from a component is thrown to the nearest boundary. Event handlers can also return errors and they bubble the same way:

```rust
onclick: move |_| {
    let number: i32 = "1...234".parse()?;
    tracing::info!("Parsed number: {number}");
    Ok(())
},
```

## Context and downcasting

anyhow's `Context` trait adds information: `.parse().context("Failed to parse name")?`. To show specific UI, wrap the error in a custom type and downcast when caught (`.downcast_ref::<T>()` on the anyhow error). Boundaries get an `ErrorContext`; call `error.error()` to inspect it and return `Err(...)` to let a different boundary handle it instead of catching.

## Error types

- `anyhow::Error` is the core error type in callbacks, actions and loaders; `.context()`, `anyhow!()` and `bail!()` work. A server function can return `anyhow::Result<i32>`.
- `CapturedError` is `pub struct CapturedError(pub Arc<anyhow::Error>)`, a `Clone` wrapper. `use_resource` requires `Clone` output, which plain `anyhow::Error` is not; `dioxus::Ok(res)` returns `Result<T, CapturedError>`.

## Local handling

For field-level errors such as validation, keep the result in a memo and render it: `let parsed = use_memo(move || phone_number().parse::<PhoneNumber>());` then `match parsed() { Ok(..) => ..., Err(error) => rsx! { "Phone number is invalid: {error}" } }`.

## Gotcha

Wrapping errors in `Result` for resources: use `dioxus::Ok` or `CapturedError` where `Clone` is needed.

## Checked
Checked 2026-11-07 against the 0.7 Error handling page and the error_handling.rs snippet file (both read in full). Confirmed: Element and RenderError definitions, ErrorBoundary handle_error, event handler errors, anyhow context and downcast_ref, ErrorContext error(), CapturedError and dioxus::Ok, memo-based local validation. Nothing removed.
Method: documentation only; no commands were run.
