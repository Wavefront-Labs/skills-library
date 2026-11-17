---
id: computing-software.web-development.leptos.for-nested-data-reactivity
name: for-nested-data-reactivity
category: computing-software
field: web-development
product: leptos
tags: [leptos, rust, for, iteration, store, memo, nested-signals, reactive-stores, pitfall]
level: practitioner
status: docs-checked
description: "Fix a Leptos For loop that does not update row values: change the key, nest signals, use per-row Memos with ForEnumerate, or use Stores."
sources: [https://book.leptos.dev/view/04b_iteration.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Make rows of structured data update inside <For/>

Goal: a `<For/>` over structs where mutating a field must refresh the UI.

## The problem

Rows are rerendered only when their key changes. With `struct DatabaseEntry { key: String, value: i32 }` and `key=|state| state.key.clone()`, doubling `value` via `set_data.update(...)` logs the new data but the `{child.value}` text does not change; wrapping in `move ||` does not help either, because `child.value` is a plain `i32`.

`let(child)` on `<For/>` is shorthand for `children=|child| view! { ... }`; you can destructure: `let(DatabaseEntry { key, value })`.

## Four fixes

1. Change the key: `key=|state| (state.key.clone(), state.value)`. Easiest, but least efficient; the whole row is thrown away and rebuilt, and the key clones the data.
2. Nested signals: `value: RwSignal<i32>`, then `row.value.update(|v| *v *= 2)` and `{child.value}`. Most efficient, fits the model, but awkward for API data you do not control. Reading `data.read()` suffices because only inner signals change.
3. Memoized slices with `ForEnumerate`:

```rust
<ForEnumerate
    each=move || data.get()
    key=|state| state.key.clone()
    children=move |index, _| {
        let value = Memo::new(move |_| {
            data.with(|data| data.get(index.get()).map(|d| d.value).unwrap_or(0))
        });
        view! { <p>{value}</p> }
    }
/>
```

   Use `data.get(index.get())`, not indexing: the memo may rerun once after the row is removed. Do not use plain `For` with `.enumerate()`; the memo keeps its initial index, so reordering causes duplicate entries.
4. Stores (needs the `reactive_stores` dependency; newest API, described by the book as possibly having edge cases, written December 2024):

```rust
#[derive(Store, Debug, Clone)]
pub struct Data {
    #[store(key: String = |row| row.key.clone())]
    rows: Vec<DatabaseEntry>,
}
#[derive(Store, Debug, Clone)]
struct DatabaseEntry { key: String, value: i32 }

// each=move || data.rows()
// key=|row| row.read().key.clone()
// children=|child| { let value = child.value(); view! { <p>{move || value.get()}</p> } }
// update: for row in data.rows().iter_unkeyed() { *row.value().write() *= 2; }
```

The store top level must be a struct; `use reactive_stores::StoreFieldIterator;` is needed for `iter_unkeyed`. Mutating `value` does not notify `key`.

## Related

- `computing-software.web-development.leptos.iterate-lists-with-for`

## Checked

2026-11-07: every claim, snippet and step above was compared with the full text of the cited Leptos book pages (https://book.leptos.dev/view/04b_iteration.html) and the book source on GitHub. Statements the pages do not state were removed or trimmed.

Method: documentation only; no commands were run.
