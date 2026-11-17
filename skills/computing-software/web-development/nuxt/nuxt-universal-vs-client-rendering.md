---
id: computing-software.web-development.nuxt.nuxt-universal-vs-client-rendering
name: nuxt-universal-vs-client-rendering
category: computing-software
field: web-development
product: nuxt
tags: [nuxt, rendering, ssr, universal-rendering, spa]
level: intro
status: docs-checked
description: "Compare Nuxt universal (SSR plus hydration) and client-side rendering, what runs where, and how to turn SSR off with ssr false."
sources:
  - https://github.com/nuxt/nuxt/blob/main/docs/3.guide/1.concepts/1.rendering.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Nuxt uses universal rendering by default: the server runs the Vue code and returns a fully rendered HTML page (or a cached one if generated in advance), then in the browser the same JavaScript runs again in the background to bind listeners to the HTML (hydration), enabling interactivity. Benefits: users get the initial content immediately, and crawlers can index the HTML without overhead. Downsides: server and browser do not provide the same APIs, so code that runs on both sides can be tricky; and a server must run to render pages on the fly, which adds cost (reduced by the browser taking over client-side navigation, and possibly by edge-side rendering).

What runs where: in `const counter = ref(0)` the ref is initialised on the server and again during hydration; the body of a click handler runs only in the browser. Middleware and pages run on the server and on the client during hydration; plugins can run on the server, client or both; components can be forced client-only; composables and utilities depend on the context of use. When importing a library that relies on browser APIs and has side effects, make sure the importing component is only called client-side, because bundlers do not treeshake imports of modules with side effects.

Client-side rendering: the browser downloads and runs the JavaScript, which generates the HTML. Benefits: no server-compatibility worry (for example using `window`), cheaper (any static server works), and it can keep working offline. Downsides: users wait for download, parse and execution, and indexing and updating content in search results takes longer. The page suggests it for heavily interactive web applications (SaaS, back-office apps, online games). Enable with:

```ts
export default defineNuxtConfig({ ssr: false })
```

With `ssr: false`, also place an HTML file at `app/spa-loading-template.html` with markup for a loading screen until the app is ready.

The page calls universal rendering especially appropriate for content-oriented sites: blogs, marketing websites, portfolios, e-commerce sites and marketplaces.

## Checked

2026-11-08. Read in full from the nuxt/nuxt docs repository: docs/3.guide/1.concepts/1.rendering.md (Universal and Client-Side Rendering sections). Confirmed: benefits, downsides, what-runs-where, ssr:false and the loading template. Removed: the "no window on the server" example attributed to SSR, the cross-reference to a route rules skill, and the invented Verify step (curl).

Method: documentation only; no commands were run.
