---
id: computing-software.web-development.svelte.store-factories
name: store-factories
category: computing-software
field: web-development
product: svelte
tags: [writable-store, readable-store, derived-store, readonly-store, store-get]
level: practitioner
status: docs-checked
description: "svelte/store helpers: writable set/update and start-stop callbacks, readable, derived with sync and async callbacks, arrays of stores, readonly, and get."
sources:
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/06-runtime/01-stores.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`writable(initial, start?)`: store with `set(value)` (no-op if equal) and `update(fn)`. If a second argument function is given, it is called when subscribers go from zero to one, receives `set` and `update`, and must return a `stop` function called when subscribers drop to zero. A writable's value is lost when destroyed (e.g. page refresh); sync to `localStorage` yourself if needed.

```js
const count = writable(0, () => {
  console.log('got a subscriber');
  return () => console.log('no more subscribers');
});
```

`readable(initial, start)`: value cannot be set from outside; `start` receives `set` and `update`:

```ts
const time = readable(new Date(), (set) => {
  const interval = setInterval(() => set(new Date()), 1000);
  return () => clearInterval(interval);
});
```

`derived(storeOrArray, fn, initial?)`: the callback runs when the first subscriber subscribes, then whenever dependencies change. `derived(a, ($a) => $a * 2)`; with an array, `derived([a, b], ([$a, $b]) => $a + $b)`. Accept `set` (and optional `update`) as extra arguments to set asynchronously; then the third argument is the initial value, otherwise `undefined`. Returning a function from the callback runs it when the callback reruns or the last subscriber leaves.

`readonly(store)`: wraps a store so it can be subscribed but not set.

`get(store)`: reads the current value by subscribing, reading and unsubscribing, so avoid it in hot code paths.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against the Svelte stores page: writable set/update and start-stop function, readable, derived (sync, async, array, cleanup return, initial value), readonly and get. Nothing removed.
