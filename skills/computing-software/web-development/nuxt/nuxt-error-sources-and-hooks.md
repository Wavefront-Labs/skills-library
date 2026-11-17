---
id: computing-software.web-development.nuxt.nuxt-error-sources-and-hooks
name: nuxt-error-sources-and-hooks
category: computing-software
field: web-development
product: nuxt
tags: [nuxt, error-handling, vue-error, app-error, plugin]
level: practitioner
status: docs-checked
description: "Know where Nuxt errors originate (Vue, startup, Nitro, chunk loading) and hook them with vue:error, errorHandler and app:error."
sources:
  - https://github.com/nuxt/nuxt/blob/main/docs/1.getting-started/12.error-handling.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Nuxt has four sources of unpreventable user runtime errors: the Vue rendering lifecycle (SSR and CSR), server and client startup, the Nitro server lifecycle (the `server/` directory), and errors downloading JS chunks.

Vue errors: use `onErrorCaptured`, the Nuxt `vue:error` hook (called if any errors propagate up to the top level, and based on `onErrorCaptured`), or a global `vueApp.config.errorHandler` for error reporting frameworks (it receives all Vue errors, even if handled):

```ts
export default defineNuxtPlugin((nuxtApp) => {
  nuxtApp.vueApp.config.errorHandler = (error, instance, info) => {
    // handle error, e.g. report to a service
  }
  nuxtApp.hook('vue:error', (error, instance, info) => {
    // also possible
  })
})
```

Startup errors call the `app:error` hook. That includes running Nuxt plugins, processing `app:created` and `app:beforeMount` hooks, rendering the Vue app to HTML (during SSR), mounting the app on the client (which you should handle with `onErrorCaptured` or `vue:error`), and processing the `app:mounted` hook.

Nitro server errors: you cannot currently define a server-side handler for these, but you can render an error page.

Chunk errors come from network connectivity failure or a new deployment that invalidates old, hashed JS chunk URLs. Nuxt has built-in support: it performs a hard reload when a chunk fails to load during route navigation. Set `experimental.emitRouteChunkError` to `false` to disable hooking into these errors at all, or to `manual` to handle them yourself.

Plugin warning from the docs: check before using anything dependent on Nuxt plugins, such as `$route` or `useRouter`, on the error page; if a plugin threw, it won't be re-run until you clear the error.

## Checked

2026-11-04. Confirmed against the Nuxt error handling page: the four error sources, vue:error, errorHandler and plugin example, the app:error list, Nitro limitation, chunk reload behaviour and emitRouteChunkError values, plugin warning. Removed the Verify step.

Method: documentation only; no commands were run.
