---
id: computing-software.web-development.nuxt.nuxt-hydration-mismatch-fixes
name: nuxt-hydration-mismatch-fixes
category: computing-software
field: web-development
product: nuxt
tags: [nuxt, hydration, ssr, usecookie, usestate]
level: practitioner
status: docs-checked
description: "Diagnose and fix hydration mismatches in Nuxt: browser-only APIs, random or time data, client-state conditions, with useCookie and useState."
sources:
  - https://github.com/nuxt/nuxt/blob/main/docs/3.guide/2.best-practices/hydration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The docs say not to ignore hydration warnings. Hydration errors force Vue to re-render the entire component tree, which increases time to interactive; users may see content flashing or layout shifts; event listeners may not attach, leaving buttons and forms non-functional; application state can get out of sync; and search engines may index different content than users see. Vue logs hydration mismatch warnings in the browser console during development.

Common causes and fixes from the docs:

1. Browser-only APIs during server-side rendering, such as `localStorage.getItem('theme')` in setup. Use `useCookie('theme', { default: () => 'light' })`, which works on both server and client.
2. Inconsistent data: `{{ Math.random() }}` differs between server and client. Use SSR-friendly state: `const state = useState('random', () => Math.random())`.
3. Conditional rendering on client state: `v-if="window?.innerWidth > 768"`. Use media queries (render both, for example `hidden md:block` and `md:hidden`) or handle it client-side.
4. Third-party libraries with side effects (common with tag managers): initialise them after hydration has completed, inside `onMounted(async () => { ... })`.
5. Time-dependent content such as a greeting from `new Date().getHours()`: use the `<NuxtTime>` component (`<NuxtTime :date="new Date()" format="HH:mm" />`), or set a default and update it in `onMounted`, optionally inside `<ClientOnly>` with a `#fallback`.
6. iOS Safari phone numbers: iOS detects phone numbers (and dates, addresses, email addresses) and wraps them in links before Vue hydrates, causing a mismatch on iOS only. Disable detection with a `format-detection` meta tag in `app.head.meta` (`content: 'telephone=no, date=no, email=no, address=no'`); to keep a phone number tappable wrap it in `<a href="tel:...">` so the link is in the server-rendered HTML.

Summary from the docs: use SSR-friendly composables (`useFetch`, `useAsyncData`, `useState`), wrap client-only code with `<ClientOnly>`, keep server and client data sources consistent, and avoid side effects in setup by moving browser-dependent code to `onMounted`.

## Checked

2026-11-04. Confirmed against the Nuxt and Hydration best-practices page: the impact list, console warnings, each common reason and its fix, the iOS Safari section, the in-summary list. Added the three reasons the draft omitted (libraries, time, iOS). Removed the invented debug-approach paragraph, the claim that .client.vue components are a hydration tool (not on the page) and the Verify step.

Method: documentation only; no commands were run.
