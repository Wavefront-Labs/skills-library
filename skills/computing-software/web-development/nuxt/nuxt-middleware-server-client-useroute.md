---
id: computing-software.web-development.nuxt.nuxt-middleware-server-client-useroute
name: nuxt-middleware-server-client-useroute
category: computing-software
field: web-development
product: nuxt
tags: [nuxt, route-middleware, ssr, useroute, import-meta]
level: advanced
status: docs-checked
description: "Control where route middleware runs (server, client, hydration), avoid useRoute inside middleware, and add middleware dynamically or via pages:extend."
sources:
  - https://github.com/nuxt/nuxt/blob/main/docs/2.directory-structure/1.app/1.middleware.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
If your site is server-rendered or generated, middleware for the initial page runs when the page is rendered and then again on the client. This is true even if you throw an error in the middleware on the server and an error page is rendered, because rendering an error page is a separate page load. Skip it as needed:

```ts
export default defineNuxtRouteMiddleware((to) => {
  if (import.meta.server) { return } // skip middleware on server
  // if (import.meta.client) { return } // skip middleware on client side entirely
  const nuxtApp = useNuxtApp()
  // or only skip middleware on initial client load
  if (import.meta.client && nuxtApp.isHydrating && nuxtApp.payload.serverRendered) { return }
})
```

You can use `useError` in middleware to check whether an error is being handled.

Always use the `to` and `from` parameters to access the next and previous routes; avoid `useRoute()` in middleware altogether. There is no concept of a "current route" in middleware, as middleware can abort a navigation or redirect elsewhere, so `useRoute()` is always inaccurate there and triggers a warning. Calling a composable that uses `useRoute()` internally has the same problem; structure helpers to accept the route as an argument, for example `function doSomethingWithRoute (route = useRoute())`, and call `doSomethingWithRoute(to)`.

Dynamic registration, for example from a plugin: `addRouteMiddleware('name', fn, { global: true })` adds a global middleware; without that option it adds a named middleware that would override any existing middleware of the same name.

Build time: instead of `definePageMeta` on each page, use the `pages:extend` hook in `nuxt.config` to set `page.meta.middleware = ['named']`, recursing over `page.children`. Note this overrides any middleware set in `definePageMeta` in the page.

## Checked

2026-11-04. Confirmed against the Nuxt middleware directory page: double execution on SSR/generated sites and the error-page note, the import.meta guards example, useError tip, the no-current-route warning and argument pattern, addRouteMiddleware with global option, pages:extend hook and its override note. Removed the Verify step.

Method: documentation only; no commands were run.
