---
id: computing-software.web-development.nuxt.nuxt-useasyncdata-keys-and-sharing
name: nuxt-useasyncdata-keys-and-sharing
category: computing-software
field: web-development
product: nuxt
tags: [nuxt, useasyncdata, keys, cache, shared-state]
level: advanced
status: docs-checked
description: "Use explicit keys with useAsyncData and useFetch, understand which options must stay consistent across shared keys, and use reactive keys."
sources:
  - https://github.com/nuxt/nuxt/blob/main/docs/1.getting-started/10.data-fetching.md
  - https://github.com/nuxt/nuxt/blob/main/docs/4.api/2.composables/use-async-data.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Keys prevent refetching. `useFetch` derives its key from URL, options and call location, so the same URL in two components has different keys. `useAsyncData` uses its first argument if it is a string; with only a handler it generates a key unique to the location of the call in your source code. Supply your own key when you want to share or look up the data.

```ts
const { id } = useRoute().params
const { data } = await useAsyncData(`user:${id}`, () => myGetFunction('users', { id }))
```

Retrieve cached data elsewhere with `useNuxtData(key)`, or see `clearNuxtData` and `refreshNuxtData` to invalidate or refetch cached data globally.

When components share a key they share the same `data`, `error` and `status` refs. These options MUST be identical across calls with that key: `handler`, `deep`, `transform`, `pick`, `getCachedData`, `default`. A mismatch triggers a development warning. These MAY differ: `server`, `lazy`, `immediate`, `dedupe`, `watch`. For independent instances use different keys (`users-1`, `users-2`).

Reactive keys are allowed (computed, ref, getter):

```ts
const userId = ref('123')
const { data } = useAsyncData(computed(() => `user-${userId.value}`), () => fetchUser(userId.value))
```

When the key changes, data refetches and old data is cleaned if unused elsewhere.

Multiple calls in one handler: `Promise.all` inside, passing `signal` from the second handler argument to `$fetch` so requests abort.

Do not use `useAsyncData` for side effects such as calling Pinia actions; that may repeat with nullish values. Use `callOnce` for those.

Verify: two components with the same key trigger only one network request.

## Checked

2026-11-08. Read the Keys, Shared State and Option Consistency, Reactive Keys and side-effect sections of the Nuxt data-fetching doc, and grepped the useAsyncData API doc for key, signal and callOnce text (that page was not read in full). Confirmed key generation rules, the must-match and may-differ option lists, reactive keys and Promise.all with signal. Removed the claim that generated keys are risky in wrapper composables and the claim that refreshNuxtData works by key.

Method: documentation only; no commands were run.
