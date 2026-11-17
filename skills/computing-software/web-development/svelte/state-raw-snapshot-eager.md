---
id: computing-software.web-development.svelte.state-raw-snapshot-eager
name: state-raw-snapshot-eager
category: computing-software
field: web-development
product: svelte
tags: [state-raw, state-snapshot, state-eager, structured-clone, non-proxied-state]
level: practitioner
status: docs-checked
description: "Svelte's $state.raw for reassign-only state, $state.snapshot for plain copies of proxies, and $state.eager for immediate UI feedback while await expressions are pending."
sources:
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/02-runes/02-%24state.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`$state.raw`: no deep reactivity. Raw state cannot be mutated, only reassigned:

```js
let person = $state.raw({ name: 'Heraclitus', age: 49 });
person.age += 1;            // no effect
person = { name: 'Heraclitus', age: 50 }; // works
```

This avoids the proxy cost for large arrays and objects you never mutate. Raw state can contain reactive state. Class fields can use `$state.raw` too.

`$state.snapshot(value)`: returns a static copy of a deeply reactive proxy, e.g. before passing it to `structuredClone` or an external API that does not expect a Proxy. If a value has `toJSON`, the snapshot clones what `toJSON` returns.

```js
console.log($state.snapshot(counter)); // { count: ... }, not Proxy
```

`$state.eager(value)`: when state is used by an `await` expression, UI updates are synchronized and wait for the async work. `$state.eager` updates immediately, e.g. `aria-current={$state.eager(pathname) === '/' ? 'page' : null}` in a nav bar for instant feedback. Use it sparingly, only as feedback to user action.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against the $state page: $state.raw reassign-only behaviour, $state.snapshot including toJSON, and $state.eager with the nav example and sparing-use advice. Nothing removed.
