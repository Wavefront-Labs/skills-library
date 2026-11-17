---
id: computing-software.web-development.nuxt.nuxt-data-fetching-overview
name: nuxt-data-fetching-overview
category: computing-software
field: web-development
product: nuxt
tags: [nuxt, data-fetching, usefetch, useasyncdata, fetch]
level: intro
status: docs-checked
description: "Choose between $fetch, useFetch and useAsyncData, understand the SSR payload, Suspense blocking and when await matters."
sources:
  - https://github.com/nuxt/nuxt/blob/main/docs/1.getting-started/10.data-fetching.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Nuxt has three data tools: `$fetch` (the ofetch library, auto-imported; the simplest way to make a request), `useFetch` (a wrapper around `$fetch` that fetches data only once in universal rendering) and `useAsyncData` (similar to `useFetch` with more fine-grained control, for example when a CMS or third party provides its own query layer). `useFetch(url)` is nearly equivalent to `useAsyncData(url, () => event.$fetch(url))`.

Why not plain `$fetch` in setup: it can fetch the data twice, once on the server (to render the HTML) and again on the client during hydration, which can cause hydration issues, slower time to interactivity and unpredictable behavior. `useFetch` and `useAsyncData` forward data fetched on the server to the client in the payload (`useNuxtApp().payload`, visible in the Payload tab of Nuxt DevTools), so the client does not refetch it. `$fetch` alone gives no network call de-duplication or navigation prevention: use it for client-side, event-based interactions (for example a form submit) or combined with `useAsyncData` for initial component data.

Suspense: Nuxt uses Vue's `<Suspense>` under the hood to prevent navigation before every async data is available. Add `<NuxtLoadingIndicator>` for a progress bar between navigations.

About `await`: it does not change the server-rendered HTML (Nuxt waits for the request during server rendering either way). It changes whether code after the call can rely on `data` being populated, and client-side navigation: with `await` (the default) navigation blocks until the data resolves; without it navigation happens immediately, `data` starts as its default value and you handle loading and error through `status` and `error`. `await` and `lazy` are independent: if you `await` a lazy call it still blocks server rendering, but on client-side navigation the `await` resolves immediately without waiting for the request. To make navigation wait, drop `lazy`.

Return values of both composables: `data`, `refresh`/`execute`, `clear` (sets `data` to `undefined` or the value of `options.default()`, `error` to `undefined`, `status` to `idle`, and marks pending requests as cancelled), `error`, `status` (`"idle"`, `"pending"`, `"success"`, `"error"`). `data`, `error` and `status` are Vue refs. By default Nuxt waits until a `refresh` is finished before it can be executed again. If data was not fetched on the server (for example `server: false`), it is not fetched until hydration completes, so `data` stays undefined in `<script setup>` even after an `await` on the client.

## Checked

2026-11-04. Confirmed against the Nuxt data fetching page: the three tools and their relationship, the double-fetch problem and payload, Suspense, the await section including the await-plus-lazy warning, return values, refresh behaviour and server:false note. Removed the Verify step.

Method: documentation only; no commands were run.
