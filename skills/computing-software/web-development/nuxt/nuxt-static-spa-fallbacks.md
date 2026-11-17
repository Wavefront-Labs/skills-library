---
id: computing-software.web-development.nuxt.nuxt-static-spa-fallbacks
name: nuxt-static-spa-fallbacks
category: computing-software
field: web-development
product: nuxt
tags: [nuxt, static-hosting, spa, prerender, error-page]
level: advanced
status: docs-checked
description: "Deploy a client-rendered Nuxt app statically with only index.html, 200.html and 404.html, and prerender the 404 error page."
sources:
  - https://github.com/nuxt/nuxt/blob/main/docs/3.guide/1.concepts/1.rendering.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
With `nuxt generate` or `nuxt build --prerender`, Nuxt renders every page as a separate static HTML file by default, and no server endpoints are included in the output (use `nuxt build` if you need server functionality). For purely client-side rendering you may only need a single `index.html` plus `200.html` and `404.html` fallbacks, served by your static host for all requests. Clear the route list with a hook:

```ts
export default defineNuxtConfig({
  hooks: {
    'prerender:routes' ({ routes }) {
      routes.clear() // do not generate any routes (except the defaults)
    },
  },
})
```

Output: `index.html`, `200.html`, `404.html`. `nuxt generate` and `nuxt build --prerender` write them into `.output/public/`; a plain `nuxt build` without prerender does not. Serve `200.html` for unmatched paths when the client router should handle the URL; serve `404.html` when the host should keep a 404 status and still load the app. Point your host at the file your provider expects.

By default `404.html` is an empty shell, so `error.vue` appears only once the client app has booted. Prerender it with `experimental: { prerenderErrorPages: true }`; Nuxt renders `error.vue` at build time with a synthetic 404 error and writes it to `404.html`. An array of status codes between 400 and 599 (for example `[404, 500]`) emits additional pages, if your host can serve them. Because one file serves every missing path, the error page cannot depend on the request: `useRoute()`, `useRequestURL()` and data fetched with the current path hold build-time values until hydration corrects them. Wrap request-specific markup in `<ClientOnly>` and skip request-specific fetching with `{ server: !import.meta.prerender }`, which is true only while the page is generated.

To skip any of the files, use Nitro's `prerender:generate` hook (under `nitro.hooks`) and set `route.skip = true` for `/index.html`, `/200.html` or `/404.html`.

## Checked

2026-11-08. Read in full from the nuxt/nuxt docs repository: docs/3.guide/1.concepts/1.rendering.md (Deploying a Static Client-Rendered App and subsections). Confirmed: hook, outputs, fallbacks, prerenderErrorPages, import.meta.prerender and the skip hook. Added the `nuxt build` alternative and the status-code array. Removed: the invented Verify step.

Method: documentation only; no commands were run.
