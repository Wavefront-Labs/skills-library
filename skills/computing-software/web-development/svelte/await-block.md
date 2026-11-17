---
id: computing-software.web-development.svelte.await-block
name: await-block
category: computing-software
field: web-development
product: svelte
tags: [await-block, promise-states, lazy-component-import, pending-then-catch, ssr-pending]
level: practitioner
status: docs-checked
description: "Branch on promise state in Svelte templates with {#await}: pending, then and catch, shorthand forms, SSR behaviour, and lazy-loading components with import()."
sources:
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/03-template-syntax/05-await.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```svelte
{#await promise}
  <p>waiting for the promise to resolve...</p>
{:then value}
  <p>The value is {value}</p>
{:catch error}
  <p>Something went wrong: {error.message}</p>
{/await}
```

The `:then` branch also renders when the expression is not a Promise. The `catch` block may be omitted.

Shorthand forms:
- No pending state: `{#await promise then value}...{/await}`
- Error only: `{#await promise catch error}...{/await}`

SSR: during server-side rendering only the pending branch renders. If the expression is not a Promise, only the `:then` branch renders, including on the server.

Lazy components:

```svelte
{#await import('./Component.svelte') then { default: Component }}
  <Component />
{/await}
```

Compare with `await` expressions in markup (see `await-expressions`).

## Checked

2026-11-08. Read the {#await} page in full. All claims matched; no claims changed.

Method: documentation only (raw page from the sveltejs/svelte repo); no commands were run.
