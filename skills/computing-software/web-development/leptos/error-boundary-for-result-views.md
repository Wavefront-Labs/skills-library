---
id: computing-software.web-development.leptos.error-boundary-for-result-views
name: error-boundary-for-result-views
category: computing-software
field: web-development
product: leptos
tags: [leptos, rust, error-boundary, error-handling, result, fallback]
level: practitioner
status: docs-checked
description: "Catch Err values rendered in a Leptos view with ErrorBoundary and show a fallback listing the current errors."
sources: [https://book.leptos.dev/view/07_errors.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: show a useful message when a `Result` rendered in the view is `Err`, and restore the content when it becomes `Ok` again.

## How Result renders

`Result<T, E>` implements `IntoView` like `Option`: `Ok(T)` renders the `T`, `Err(_)` renders nothing. A signal holding a `Result` therefore silently shows nothing on bad input.

## Method

Wrap the part of the view that may render an `Err` in `<ErrorBoundary/>` and give it a `fallback`. The fallback receives a signal of the current errors.

```rust
let (value, set_value) = signal(Ok(0));

view! {
    <input type="number" on:input:target=move |ev| {
        set_value.set(ev.target().value().parse::<i32>())
    }/>
    <ErrorBoundary
        fallback=|errors| view! {
            <div class="error">
                <p>"Not a number! Errors: "</p>
                <ul>
                    {move || errors.get()
                        .into_iter()
                        .map(|(_, e)| view! { <li>{e.to_string()}</li>})
                        .collect::<Vec<_>>()
                    }
                </ul>
            </div>
        }
    >
        <p>"You entered " <strong>{value}</strong></p>
    </ErrorBoundary>
}
```

Typing `42` shows the children; typing `foo` shows the fallback (the page's example message is "cannot parse integer from empty string"); fixing the input brings the children back.

## Gotchas

- Parse the input yourself. The page notes `<input type="number">` does not guarantee an `i32`: browsers differ, and users can enter floats, values larger than 32 bits, or the letter `e`.
- `<ErrorBoundary/>` behaves like `<Show/>`: children when everything is `Ok`, fallback when an `Err` is rendered among them.
- Related: `computing-software.web-development.leptos.conditional-rendering-with-rust-control-flow`.

## Checked

2026-11-07: every claim, snippet and step above was compared with the full text of the cited Leptos book pages (https://book.leptos.dev/view/07_errors.html) and the book source on GitHub. Statements the pages do not state were removed or trimmed.

Method: documentation only; no commands were run.
