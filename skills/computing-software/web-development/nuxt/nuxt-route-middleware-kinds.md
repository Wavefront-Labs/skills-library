---
id: computing-software.web-development.nuxt.nuxt-route-middleware-kinds
name: nuxt-route-middleware-kinds
category: computing-software
field: web-development
product: nuxt
tags: [nuxt, route-middleware, auth, define-nuxt-route-middleware, navigate-to]
level: practitioner
status: docs-checked
description: "The three kinds of Nuxt route middleware (inline, named, global), how to attach them and why they never run for server routes."
sources:
  - https://github.com/nuxt/nuxt/blob/main/docs/1.getting-started/07.routing.md
  - https://github.com/nuxt/nuxt/blob/main/docs/2.directory-structure/1.app/1.middleware.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Route middleware runs within the Vue part of the app, before navigating to a route. It is completely different from server middleware (Nitro) and does not run for server routes such as `/api/*` or other server requests; use server middleware for those.

Three kinds:
1. Anonymous (inline): defined directly in the page that uses it.
2. Named: a file in `app/middleware/`, loaded by asynchronous import when used on a page. Names are normalised to kebab-case.
3. Global: a file in `app/middleware/` with a `.global` suffix, run on every route change.

The first two kinds can be defined in `definePageMeta` (`middleware: 'auth'`, or an array that may mix inline functions and names).

Example guard from the routing page:

```ts
// app/middleware/auth.ts
export default defineNuxtRouteMiddleware((to, from) => {
  if (isAuthenticated() === false) {
    return navigateTo('/login')
  }
})
```

```vue
<script setup lang="ts">
definePageMeta({ middleware: 'auth' })
</script>
```

Return nothing to continue, `navigateTo()` to redirect, or `abortNavigation()` to stop. `isAuthenticated()` is, per the page, an example method.

## Checked

2026-11-08. Read in full from the nuxt/nuxt docs repository: docs/1.getting-started/07.routing.md (Route Middleware section) and docs/2.directory-structure/1.app/1.middleware.md. Confirmed: three kinds, kebab-case, the not-for-server-routes warning, the example. Changed: dropped the unsupported inline syntax `middleware(to, from)` in favour of what the page states. Removed: the invented Verify step.

Method: documentation only; no commands were run.
