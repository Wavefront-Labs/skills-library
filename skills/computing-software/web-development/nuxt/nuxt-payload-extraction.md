---
id: computing-software.web-development.nuxt.nuxt-payload-extraction
name: nuxt-payload-extraction
category: computing-software
field: web-development
product: nuxt
tags: [nuxt, payload, payload-extraction, devalue, prerender]
level: advanced
status: docs-checked
description: "How Nuxt serialises useAsyncData, useFetch and useState results into payloads, the experimental.payloadExtraction modes, and their staleness and serialisation caveats."
sources:
  - https://github.com/nuxt/nuxt/blob/main/docs/1.getting-started/15.prerendering.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
When Nuxt renders a page on the server, it serializes the results of data fetching (`useAsyncData`, `useFetch`) and app state (`useState`) into a payload so the client can hydrate without re-fetching. With payload extraction enabled, Nuxt also writes the payload to a `_payload.json` file alongside the route's HTML. Prerendered routes generate it at build time; routes using ISR or SWR caching generate it when the route is first rendered, even on a hybrid (non-static) site. During client-side navigation Nuxt fetches the destination route's `_payload.json` and reuses the extracted data instead of running the data fetching again in the browser.

Control with `experimental.payloadExtraction`:
- `'client'`: the payload is inlined in the HTML for the initial render and extracted to `_payload.json` files for client-side navigation. No extra network request on first load.
- `true`: the payload is extracted to a separate `_payload.json` for both the initial render and client-side navigation. The HTML is smaller and the payload file can be cached by a CDN, at the cost of one extra request on first load.
- `false`: extraction disabled; the payload is always inlined and no `_payload.json` files are generated.

The default is `'client'`. It is forced to `false` when `ssr: false` is set.

```ts
export default defineNuxtConfig({ experimental: { payloadExtraction: 'client' } })
```

Consequences from the docs:
- On a fully static site, client-side navigation reuses the data captured at build time, so data can be stale until the next rebuild.
- For ISR/SWR routes, CDNs can cache payload files alongside the HTML, improving client-side navigation for cached routes. Dynamic routes like `pages/[...slug].vue` can opt in with glob patterns such as `'/**': { isr: true }`.
- Payloads are serialized with devalue, so custom types (such as class instances) need payload plugins with custom reducers and revivers to survive the round trip.

## Checked

2026-11-04. Confirmed against the Nuxt prerendering page, section "Payload Extraction": payload contents, when _payload.json is generated, the three payloadExtraction values, default and ssr:false rule, and the three consequences. Removed the DevTools/useNuxtApp inspection sentence (not on this page) and the Verify step.

Method: documentation only; no commands were run.
