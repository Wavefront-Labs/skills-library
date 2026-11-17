---
id: computing-software.web-development.angular.control-flow-for
name: control-flow-for
category: computing-software
field: web-development
product: angular
tags: [angular, templates, control-flow, for-block, track, empty-block, ngfor]
level: intro
status: docs-checked
description: "Angular @for loops: choosing the track expression, contextual variables like $index and $even with let aliases, and the @empty fallback block."
sources:
  - https://angular.dev/guide/templates/control-flow
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`@for` repeats a block over any JavaScript iterable (Angular adds optimizations for `Array`). Pass a `track` expression (see below).

```html
@for (item of items; track item.id) {
  {{ item.name }}
}
```

There are no `continue` or `break` statements.

Why `track` matters: it lets Angular keep the relationship between data and DOM nodes, so it performs the minimum DOM operations when data changes. Choose:
- A property that uniquely identifies each item, commonly `id` or `uuid`. If your model lacks one, strongly consider adding it.
- `$index` for static collections that never change.
- The item itself (`track item`) only as a last resort. It tracks by reference identity with `===`, can cause significantly slower updates, and gives Angular no way to map data items to DOM nodes.

Unlike `*ngFor`, `@for` prioritizes view reuse: if a tracked property changes but the object reference stays the same, Angular updates the view's bindings (including component inputs) instead of destroying and recreating the element.

Contextual variables always available inside the block: `$count`, `$index`, `$first`, `$last`, `$even`, `$odd`. Alias them with `let`, which helps in nested loops:

```html
@for (item of items; track item.id; let idx = $index, e = $even) {
  <p>Item #{{ idx }}: {{ item.name }}</p>
}
```

`@empty` immediately after the loop content renders when there are no items:

```html
@for (item of items; track item.name) {
  <li>{{ item.name }}</li>
} @empty {
  <li>There are no items.</li>
}
```

For conditional blocks see `computing-software.web-development.angular.control-flow-if-switch`.

## Checked

Date: 2026-11-07

Read in full: https://angular.dev/guide/templates/control-flow (source Markdown from the angular/angular repository, adev/src/content/guide, plus the live page text where the fetch returned content). Inline code snippets were read; no separate example files were opened.
Removed "`track` is required" (the page does not say so).

Method: documentation only; no commands were run.
