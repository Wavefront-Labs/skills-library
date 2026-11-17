---
id: computing-software.web-development.svelte.stores-basics
name: stores-basics
category: computing-software
field: web-development
product: svelte
tags: [svelte-stores, store-auto-subscription, dollar-store-prefix, runes-vs-stores, shared-state-module]
level: intro
status: docs-checked
description: "Svelte stores and the $ prefix for auto-subscription at the component top level, and when runes in .svelte.js modules replace stores versus when stores still fit."
sources:
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/06-runtime/01-stores.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A store is an object giving reactive access to a value via the store contract. Prefix a store reference with `$` inside a component and Svelte declares the variable, subscribes at initialisation and unsubscribes when appropriate. Assigning to `$count` requires a writable store and calls its `.set`.

Rules: the store must be declared at the top level of the component (not inside an `if` block or function). Local variables that are not stores must not start with `$`.

```svelte
<script>
  import { writable } from 'svelte/store';
  const count = writable(0);
  console.log($count); // 0
  count.set(1);
  $count = 2;
</script>
```

When to use stores: before Svelte 5 they were the default for shared state or extracted logic. With runes this has greatly diminished. Extract logic using runes in `.svelte.js`/`.svelte.ts` files, and share state with a `$state` object:

```ts
// state.svelte.js
export const userState = $state({ name: 'name' });
```

Components import it and read `userState.name`, or assign `userState.name = 'new name'`.

Stores remain a good fit for complex asynchronous data streams, or when you need more manual control over updating values or listening to changes. If you know RxJS, the `$` syntax feels familiar.

See `store-factories` and `store-contract`.

## Checked

2026-11-08: Read the Stores page (dollar prefix rules, top-level requirement, when to use stores versus runes, state.svelte.js example, store contract pointer). Every claim was located; nothing removed.

Method: docs-only read of cited pages, 2026-11-08
