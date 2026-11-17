---
id: computing-software.web-development.leptos.reactive-vs-static-view-values
name: reactive-vs-static-view-values
category: computing-software
field: web-development
product: leptos
tags: [leptos, rust, reactivity, signal, closure, view-macro, pitfall]
level: practitioner
status: docs-checked
description: "Tell reactive from one-shot values in a Leptos view: signals and closures update, while count.get() renders once."
sources: [https://book.leptos.dev/view/01_basic_component.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reactive versus static values in view!

Goal: avoid the most common Leptos mistake, writing a value where you needed a signal or function.

Only signals and functions are treated as reactive values in the view. Passing a function tells the framework that the value might change.

## Rules

| In the view | Behaviour |
| --- | --- |
| `{count}` | passes the signal; text updates whenever `count` changes |
| `{move || count.get()}` | closure; reactive |
| `{count.get()}` | reads the value once and renders an unreactive `i32` |
| `{move || count.get() * 2}` | reactive |
| `{count.get() * 2}` | evaluated once; will not update |

When `set_count` fires, a closure that depends on `count` reruns and the framework makes a targeted update to that specific text node, touching nothing else.

## Example from the book

```rust
view! {
    <p><strong>"Reactive: "</strong>{move || count.get()}</p>
    <p><strong>"Reactive shorthand: "</strong>{count}</p>
    // NOTE: if you just write {count.get()}, this will not be reactive
    <p><strong>"Not reactive: "</strong>{count.get()}</p>
}
```

## Why

The page says the component body is a set-up function that runs once, not a render function that reruns multiple times, so reactivity is expressed by handing the view a signal or closure.

## Related

- `computing-software.web-development.leptos.first-component-and-view`
- `computing-software.web-development.leptos.dynamic-classes-styles-attributes`

## Checked

2026-11-07: Read in full: view/01_basic_component.md including the inline sandbox source (the Reactive, Reactive shorthand and Not reactive paragraphs; the {count} versus {count.get()} and move-closure versus plain-expression paragraphs). The table rows match the page text. One correction: the 'Why' paragraph said nothing re-renders the whole component; it now states what the page says (the component body is a set-up function that runs once, not a render function that reruns). Live sandbox not opened.

Method: documentation only; no commands were run.
