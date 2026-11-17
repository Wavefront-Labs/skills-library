---
id: computing-software.web-development.svelte.await-expressions
name: await-expressions
category: computing-software
field: web-development
product: svelte
tags: [await-expressions, experimental-async, synchronized-updates, concurrency, settled]
level: advanced
status: docs-checked
description: "Svelte 5.36+ experimental await in script, $derived and markup: opt-in flag, synchronized UI updates, parallel work, loading states with pending, tick and settled."
sources:
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/03-template-syntax/19-await-expressions.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
From Svelte 5.36 you can use `await` at the top level of `<script>`, inside `$derived(...)` and in markup. It is experimental: opt in with `compilerOptions.experimental.async: true` in `svelte.config.js`. The flag is removed in Svelte 6.

Synchronized updates: while an `await` expression depends on state, UI changes wait until the async work completes, so the UI is never inconsistent. Updates can overlap; a fast one shows while an earlier slow one is ongoing.

```svelte
<p>{a} + {b} = {await add(a, b)}</p>
```

Concurrency: independent markup awaits run in parallel (`{await one(x)}` and `{await two(y)}`). Sequential awaits in script or async functions behave as normal JavaScript. Independent `$derived(await ...)` values are created sequentially but update independently, and Svelte warns with `await_waterfall`.

Loading states: wrap content in `<svelte:boundary>` with a `pending` snippet; it shows on first creation only. Afterwards detect async work with `$effect.pending()`. `settled()` from `svelte` returns a promise that resolves when the current update completes:

```js
updating = true;
await tick();     // so the change to `updating` is not grouped
color = 'octarine';
await settled();
updating = false;
```

Errors bubble to the nearest error boundary.

Breaking change under the flag: block effects like `{#if}` and `{#each}` run before `$effect.pre` or `beforeUpdate` in the same component.

## Checked

Method: docs-only read of cited pages, 2026-11-08
