---
id: computing-software.web-development.svelte.state-sharing-modules
name: state-sharing-modules
category: computing-software
field: web-development
product: svelte
tags: [shared-state, svelte-js-modules, export-state, pass-state-to-functions, reactive-getter]
level: practitioner
status: docs-checked
description: "Share Svelte $state across functions and modules: pass getters not values, why exporting a reassigned $state fails in .svelte.js, and the two safe patterns."
sources:
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/02-runes/02-%24state.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Functions: JavaScript passes values, so `add(a, b)` receives the current numbers, not the variables. To keep reading current state, pass functions (`add(() => a, () => b)`) or an object whose property is read later (a `get value()` getter over a `$state` object).

Modules: you can declare state in `.svelte.js` and `.svelte.ts` files, but you cannot export state that is directly reassigned:

```js
export let count = $state(0);   // not allowed
export function increment() { count += 1; }
```

The compiler wraps each reference in `$.get`/`$.set` per file; an importing file does not know to, so `typeof count` would be `'object'`.

Two options:

1. Export an object and mutate its properties, not the binding:
```js
export const counter = $state({ count: 0 });
export function increment() { counter.count += 1; }
```
2. Keep the variable private and export accessors:
```js
let count = $state(0);
export function getCount() { return count; }
export function increment() { count += 1; }
```

Check: the playground's JS Output tab shows the generated `$.state`/`$.get`/`$.set` code.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against the $state page: pass-by-value explanation, getters, the export restriction for reassigned state with compiler explanation, and the two safe patterns. Nothing removed.
