---
id: computing-software.web-development.nuxt.nuxt-fetch-options-lazy-server-pick
name: nuxt-fetch-options-lazy-server-pick
category: computing-software
field: web-development
product: nuxt
tags: [nuxt, usefetch, lazy, pick, transform]
level: practitioner
status: docs-checked
description: "Tune useFetch and useAsyncData with lazy, server:false, pick and transform to control blocking and payload size."
sources:
  - https://github.com/nuxt/nuxt/blob/main/docs/1.getting-started/10.data-fetching.md
  - https://github.com/nuxt/nuxt/blob/main/docs/4.api/2.composables/use-lazy-fetch.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Shared options (last argument of both composables):

- `lazy: true` (or `useLazyFetch` / `useLazyAsyncData`, which have the same signature as `useFetch`): client-side navigation is not blocked; handle the loading state yourself with `status === 'pending'`. Awaiting `useLazyFetch` initializes the call but does not wait for the data. `useLazyFetch` is a reserved function name transformed by the compiler, so do not name your own function that.
- `server: false`: run only on the client. On initial load the data is not fetched before hydration is complete, so you handle a pending state; on subsequent client-side navigation the data is awaited before loading the page. Combined with `lazy` it suits data not needed on the first render (for example non-SEO data):

```ts
const articles = await useFetch('/api/article') // before hydration
const { status, data: comments } = useFetch('/api/comments', { lazy: true, server: false })
```

`useFetch` is meant to be invoked in setup or called at the top level of a function in lifecycle hooks; otherwise use `$fetch`.

- `pick: ['title', 'description']` selects only those fields to be returned, minimizing the payload stored in the HTML document.
- `transform` alters the result of the query, for example mapping a list to `{ title, description }` objects.

Both `pick` and `transform` do not prevent the unwanted data from being fetched initially; they prevent it from being added to the payload transferred from server to client.

- `immediate: false` stops the request starting when the composable is invoked; use `execute` to start it and `status` (`idle` before it starts) for the lifecycle.
- `watch: [id]` re-runs the fetch when those reactive values change, but watching does not change the URL: a URL built as a string with `id.value` is constructed when the function is invoked. For a changing URL use a getter (`() => `/api/users/${id.value}``) or a reactive value inside `query` (`query: { user_id: id }`). Reactive fetch options are watched automatically; opt out with `watch: false`.

## Checked

2026-11-04. Confirmed against the Nuxt data fetching page and the useLazyFetch page: lazy and the lazy composables, the await-useLazyFetch and reserved-name warnings, server:false behaviour and example, pick and transform plus the payload note, immediate:false with execute and status, watch limits, computed URL getter, reactive query, watch:false. Removed the claim that large server responses cost server time and the Verify step (neither in the pages).

Method: documentation only; no commands were run.
