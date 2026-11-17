---
id: computing-software.web-development.svelte.svelte-boundary
name: svelte-boundary
category: computing-software
field: web-development
product: svelte
tags: [svelte-boundary, error-boundary, pending-snippet, failed-snippet, onerror-handler]
level: practitioner
status: docs-checked
description: "svelte:boundary (5.3+) walls off app parts: pending snippet for first await, failed snippet with reset, onerror reporting, and what errors boundaries do not catch."
sources:
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/05-special-elements/01-svelte-boundary.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`<svelte:boundary onerror={handler}>...</svelte:boundary>` (added in 5.3.0) lets you show UI while `await` expressions first resolve and handle errors thrown during rendering or effects. When a boundary handles an error (via `failed` or `onerror`), its existing content is removed. Errors outside rendering (event handlers, `setTimeout`, async work) are not caught.

`pending` snippet: shown at creation until all `await` expressions inside resolve; not shown for later updates (use `$effect.pending()`).

```svelte
<svelte:boundary>
  <p>{await delayed('hello!')}</p>
  {#snippet pending()}<p>loading...</p>{/snippet}
</svelte:boundary>
```

`failed` snippet: rendered on error, with `error` and a `reset` function that recreates the contents. It can be declared inside or passed as `{failed}`.

```svelte
<svelte:boundary>
  <FlakyComponent />
  {#snippet failed(error, reset)}
    <button onclick={reset}>oops! try again</button>
  {/snippet}
</svelte:boundary>
```

`onerror(error, reset)`: for reporting (`onerror={(e) => report(e)}`) or to use `error` and `reset` outside the boundary. Errors thrown or rethrown there go to a parent boundary.

Server: errors fail the whole render by default. Since 5.51, pass `transformError` to `render(...)` (also accepted by `mount` and `hydrate`) returning a JSON-stringifiable object used to render `failed`. Redact sensitive messages and stacks.

## Checked

2026-11-08: Read the svelte:boundary page end to end (5.3.0, pending, failed, onerror, uncaught error kinds, 5.51 transformError, mount and hydrate option). Every claim was located; nothing removed.

Method: docs-only read of cited pages, 2026-11-08
