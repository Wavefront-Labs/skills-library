---
id: computing-software.web-development.leptos.iterate-lists-with-for
name: iterate-lists-with-for
category: computing-software
field: web-development
product: leptos
tags: [leptos, rust, iteration, for, for-enumerate, keyed-list, collect-view, list]
level: practitioner
status: docs-checked
description: "Render lists in Leptos with a Vec of views for static lists and the keyed For or ForEnumerate component for lists that change."
sources: [https://book.leptos.dev/view/04_iteration.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Render lists: Vec<_>, For and ForEnumerate

Goal: choose the right iteration pattern and use a stable key.

## Static lists

Anything `Vec<T>` where `T: IntoView` is renderable. Map and collect:

```rust
let values = vec![0, 1, 2];
view! {
    <ul>
        {values.into_iter()
            .map(|n| view! { <li>{n}</li>})
            .collect_view()}
    </ul>
}
```

`.collect_view()` collects an iterator of `IntoView` into `Vec<View>`; `.collect::<Vec<_>>()` also works. Items in a static list can be reactive, e.g. `RwSignal::new(idx)` per row. `RwSignal` is a single read-write signal, handier than a tuple to pass around.

A reactive `Fn() -> Vec<_>` is an unkeyed update: DOM elements are reused by position. Fine for append/remove at the end; moving or inserting in the middle does extra browser work and can disturb input state and CSS animations.

## Dynamic lists with <For/>

Props:

- `each`: reactive function returning the items
- `key`: takes `&T`, returns a stable unique key
- `children`: renders each item

```rust
<For
    each=move || counters.get()
    key=|counter| counter.0
    children=move |(id, count)| {
        let count = RwSignal::from(count);
        view! { <li><button on:click=move |_| *count.write() += 1>{count}</button></li> }
    }
/>
```

Rows are only rerendered if their key changes. Do not use the index as key (indices change when items move); generate a unique id per row, e.g. an incrementing counter.

Use `ArcRwSignal` for per-row signals in a growing/shrinking list: it is reference-counted, so each signal is deallocated when its row is removed. Convert with `RwSignal::from(arc)` for a Copy-able handle.

## ForEnumerate

Same props as `<For/>`, but children also get a `ReadSignal<usize>` index:

```rust
<ForEnumerate
    each=move || counters.get()
    key=|counter| counter.id
    let(idx, counter)
>
    <button>{move || idx.get()} ". Value: " {move || counter.count.get()}</button>
</ForEnumerate>
```

## Related

- `computing-software.web-development.leptos.for-nested-data-reactivity`

## Checked

2026-11-07: every claim, snippet and step above was compared with the full text of the cited Leptos book pages (https://book.leptos.dev/view/04_iteration.html) and the book source on GitHub. Statements the pages do not state were removed or trimmed.

Method: documentation only; no commands were run.
