---
id: computing-software.web-development.svelte.await-ssr-fork
name: await-ssr-fork
category: computing-software
field: web-development
product: svelte
tags: [async-ssr, server-render, fork-api, preloading, pending-snippet-ssr]
level: sme
status: docs-checked
description: "Async server-side rendering with await render(App) and the fork() API (5.42+) to start expected await work early, then commit or discard it."
sources:
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/03-template-syntax/19-await-expressions.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Prerequisite: `await` in components (5.36+) is experimental and needs `compilerOptions.experimental.async: true` in the Svelte config; the flag goes away in Svelte 6.

Server-side rendering: Svelte supports asynchronous SSR through the `render(...)` API from `svelte/server`; await the result:

```js
import { render } from 'svelte/server';
import App from './App.svelte';

const { head, body } = await render(App);
```

Frameworks like SvelteKit do this for you. If a `<svelte:boundary>` with a `pending` snippet is met during SSR, that snippet renders and the rest of its content is ignored. All `await` expressions outside such boundaries resolve and render before `await render(...)` returns. A streaming implementation is planned.

Forking: `fork(...)`, added in 5.42, runs `await` expressions you expect to happen soon. It is mainly for frameworks to implement preloading when users signal intent to navigate.

```svelte
<script>
  import { fork } from 'svelte';
  let open = $state(false);
  let pending = null;

  function preload() { pending ??= fork(() => { open = true; }); }
  function discard() { pending?.discard(); pending = null; }
</script>

<button
  onpointerenter={preload}
  onpointerleave={discard}
  onclick={() => { pending?.commit(); pending = null; open = true; }}
>open menu</button>
```

Async work inside the revealed component starts as soon as the fork is created. As an experimental feature, details may change outside a semver major release.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against the await expressions page: async SSR with await render(), pending-snippet behaviour, fork() added in 5.42 with the preload example, experimental caveat. Added the missing prerequisite (experimental.async flag, await in components from 5.36). Nothing else removed.
