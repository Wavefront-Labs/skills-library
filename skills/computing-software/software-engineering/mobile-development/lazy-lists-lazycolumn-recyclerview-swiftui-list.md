---
id: computing-software.software-engineering.mobile-development.lazy-lists-lazycolumn-recyclerview-swiftui-list
name: lazy-lists-lazycolumn-recyclerview-swiftui-list
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, lazycolumn, recyclerview, swiftui-list, diffutil, paging, jetpack-compose, swiftui, lists]
level: practitioner
status: docs-checked
description: "Build fast scrolling Android lists: Compose LazyColumn keys and contentType, nesting rules, RecyclerView adapter basics, and Paging 3."
sources: ["https://developer.android.com/develop/ui/compose/lists", "https://developer.android.com/develop/ui/views/layout/recyclerview", "https://developer.android.com/topic/libraries/architecture/paging/v3-overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lazy lists (LazyColumn / RecyclerView / Paging)

**Goal:** lists of thousands of items that scroll smoothly, keep scroll position and animate
updates correctly.

## Compose LazyColumn
```kotlin
LazyColumn(state = listState, contentPadding = PaddingValues(16.dp)) {
    stickyHeader { SectionHeader("Today") }
    items(items = messages, key = { it.id }, contentType = { it.type }) { msg ->
        MessageRow(msg, modifier = Modifier.animateItem())
    }
}
```
- **Stable `key`s**: by default item state is keyed by position, so items that move lose remembered state (for example
  a LazyRow inside a LazyColumn loses its scroll position). A stable, unique key lets Compose move state with the
  item and handle reorderings. `animateItem()` animates additions, removals and moves, and needs keys to work.
- `contentType` (Compose 1.2 and later) lets Compose reuse compositions only between items of the same type.
- Never nest a `LazyColumn` without a fixed height inside a vertically scrollable `Column(Modifier.verticalScroll)`:
  it throws `IllegalStateException`. Use one LazyColumn with multiple `item`/`items` blocks. Nesting in a different
  direction, or giving the nested list a fixed size, is allowed.
- Avoid 0-pixel items (for example async images with no default size): the layout composes all items on the first
  measurement. Give items a default size.
- Putting several elements in one `item {}` composes them together as one entity and interferes with
  `scrollToItem()`/`animateScrollToItem()`; fine for small things such as dividers.
- `rememberLazyListState()` with `derivedStateOf { listState.firstVisibleItemIndex > 0 }` drives a "scroll to top"
  button without recomposing on every scroll change.

## RecyclerView
RecyclerView needs a `ViewHolder` (extend `RecyclerView.ViewHolder`; a wrapper around the item View) and an `Adapter`
that creates holders in `onCreateViewHolder()` (does not fill in data) and binds data in `onBindViewHolder()`.

## Paging large or remote data
- Paging 3: `Pager` builds `PagingData` streams from a `PagingSource` and a `PagingConfig`; `RemoteMediator` pages
  from a layered source such as network plus a local database cache.
- In Compose add `androidx.paging:paging-compose` and use `collectAsLazyPagingItems()` on a `Flow<PagingData>`, passing
  the `LazyPagingItems` to `items()` in a LazyColumn, with no adapters or diffing logic needed. Provide a key with
  `lazyPagingItems.itemKey { it.id }`.
- With a `RemoteMediator`, use realistically sized placeholders: small or missing placeholders can leave the screen
  never filled so many pages are fetched.

## Verify
- [ ] Every list has stable keys.
- [ ] Insert/remove/reorder animate correctly and keep per-item state.

## Checked
2026-11-08. Confirmed against the Android Developers pages Lists and grids (Compose), Create dynamic lists with RecyclerView and Paging overview: keys, `animateItem`, `contentType`, nesting rules, 0-pixel and multi-element items, `derivedStateOf` scroll example, adapter and ViewHolder roles, Pager/RemoteMediator/`collectAsLazyPagingItems`. Removed: the SwiftUI section and Apple List source (page not readable; name and tags are kept for the id), `ListAdapter`/`DiffUtil`/`AsyncListDiffer`/`setHasFixedSize`/`RecycledViewPool`/`ConcatAdapter` advice and `cachedIn`, `pageSize = 30` (not on the pages read), the R8/baseline-profile measurement note, and iOS paging notes.
Method: documentation only; no commands were run.
