---
id: computing-software.web-development.svelte.context-state-ssr
name: context-state-ssr
category: computing-software
field: web-development
product: svelte
tags: [context-with-state, ssr-global-state-leak, wrapper-component-context, mount-with-context, state-reassign-warning]
level: advanced
status: docs-checked
description: "Use Svelte context with $state, avoid breaking the link by reassigning, mount components with context in tests (5.49+), and why context beats module state on the server."
sources:
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/06-runtime/02-context.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Reactive state in context: put a `$state` object in context and let children read and update it.

```svelte
<script>
  import { setCounter } from './context.ts';
  let counter = $state({ count: 0 });
  setCounter(counter);
</script>
<button onclick={() => counter.count += 1}>increment</button>
```

Do not reassign: `counter = { count: 0 }` breaks the link between provider and consumers; mutate `counter.count = 0` instead. Svelte warns if you get it wrong. For primitives, pass functions (see `state-sharing-modules`).

Mounting with context (5.49+): wrap the component in a function that sets context first, e.g. for tests:

```js
function Wrapper(...args) {
  setUserContext({ name: 'Bob' });
  return MyComponent(...args);
}
const component = mount(Wrapper, { target: document.body });
// ...assertions
unmount(component);
```

This also works with `hydrate` and `render`. The context applies only to that mounted tree; each call creates a separate wrapper instance, so nothing leaks.

Replacing global state: module-level `$state` is often fine, but if it is mutated during server-side rendering (discouraged), data can be visible to the next user. Context avoids this because it is not shared between requests.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against the Svelte context page: state in context, the reassign warning, mounting with a wrapper (5.49+) also for hydrate and render, and the SSR cross-request argument. Nothing removed.
