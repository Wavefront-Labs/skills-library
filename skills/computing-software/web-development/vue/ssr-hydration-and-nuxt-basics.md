---
id: computing-software.web-development.vue.ssr-hydration-and-nuxt-basics
name: ssr-hydration-and-nuxt-basics
category: computing-software
field: web-development
product: vue
tags: [vue, ssr, hydration, nuxt, hydration-mismatch, universal-rendering, onmounted, web-development]
level: advanced
status: gated
description: "Vue SSR hydration mismatches (window/Date/Math.random in render), Nuxt's data-fetching composables, and client-only escape hatches."
sources:
  - https://vuejs.org/guide/scaling-up/ssr.html
  - https://nuxt.com/docs/getting-started/data-fetching
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Vue SSR, hydration mismatches, and Nuxt basics

**Goal:** server-render for fast first paint and SEO without the client's
hydration pass producing a different DOM than the server sent — which is the
single most common SSR bug class.

## 1. What hydration actually is
SSR renders HTML on the server and sends it to the browser immediately
(fast first paint, crawlable). The client then runs Vue again over that same
markup, "hydrating" it — attaching event listeners and reactive bindings to the
existing DOM nodes instead of re-rendering from scratch. Hydration **assumes**
the client's render output matches the server's exactly; if it doesn't, Vue
either warns and patches the mismatch (slow, and may flash) or, in some cases,
silently leaves the DOM wrong.

## 2. The classic causes of a mismatch
- **Browser-only globals** (`window`, `document`, `localStorage`) referenced
  during render (the Vue SSR guide lists invalid HTML nesting, random values and time zones as mismatch causes; that `typeof window` branches always mismatch is unconfirmed (gated: unconfirmed, source is paywalled or blocked)) — don't exist on the server, throw there, or get guarded in a
  way that produces different output server vs client.
- **Non-deterministic values** computed during render: random values, time-zone-dependent output (Vue SSR guide), and by the same logic `Date.now()` — the server computes one value
  at request time, the client computes a different one at hydration time
  moments later, producing a mismatch on every single page load.
- **Conditional rendering based on `typeof window !== 'undefined'`** directly in
  a template/render function — this guarantees the server and client branches
  differ by construction; this pattern is the bug, not a fix for it.
Fix: move browser-only/non-deterministic logic into `onMounted()` (client-only,
runs after hydration) and render a stable placeholder for both server and
initial client pass, then update it post-mount if needed.

## 3. `<ClientOnly>` (Nuxt) / manual client-only wrapping
(Nuxt `<ClientOnly>` and its `#fallback` slot: unconfirmed (gated: unconfirmed, source is paywalled or blocked))
```vue
<ClientOnly>
  <WeatherWidget />      <!-- needs navigator.geolocation; server can't render it -->
  <template #fallback><div class="skeleton" /></template>
</ClientOnly>
```
For a component that is fundamentally impossible to render server-side (reads
`window.innerWidth`, a charting lib that needs a real canvas), skip SSR for just
that component rather than disabling SSR for the whole page — the fallback slot
renders on the server and during the brief gap before client mount.

## 4. Nuxt's data-fetching composables
`useFetch`/`useAsyncData` run on the server during SSR and **do not re-fetch on
the client during hydration** — the fetched data is serialized into the page
payload and reused client-side, avoiding a duplicate request. Calling a raw
`fetch()` directly inside `setup()` instead loses this dedup and fetches twice
(once server, once client) unless wrapped in one of these composables.
```js
const { data, error, pending } = await useFetch('/api/products');
```
Nuxt docs: `useFetch` generates a key from the URL, options and call location (calls sharing a key share `data`, `error` and `status`), and is meant for `setup` or the top level of lifecycle hooks; elsewhere use `$fetch`.

## 5. State that must cross server-to-client
Anything set during SSR that the client needs on hydration (a CSRF token, a
feature flag resolved server-side) goes through `useState()` (Nuxt's SSR-safe
shared state, serialized into the payload) — not a plain module-level variable,
because server modules are initialised once and reused across requests, so module-level state is shared between users (Vue SSR guide, "Cross-Request State Pollution"). That `useState` is the recommended Nuxt replacement is unconfirmed (gated: unconfirmed, source is paywalled or blocked).

## Verify
- [ ] No render-path code reads `window`/`document`/`localStorage` without an `onMounted`/`ClientOnly` guard.
- [ ] No `Date.now()`/`Math.random()`/locale-dependent formatting runs during the initial render that must match server output.
- [ ] Data fetching uses `useFetch`/`useAsyncData`, not a raw `fetch` call that double-fetches client-side.
- [ ] Per-request server state uses `useState()` or request-scoped storage, never a shared module-level variable.
- [ ] No hydration mismatch warnings appear in the browser console on a cold load of any page.
