---
id: computing-software.web-development.nuxt.nuxt-route-middleware-returns-and-order
name: nuxt-route-middleware-returns-and-order
category: computing-software
field: web-development
product: nuxt
tags: [nuxt, route-middleware, navigate-to, abort-navigation, middleware-order]
level: advanced
status: docs-checked
description: "Write route middleware with navigateTo and abortNavigation, understand registration rules, global ordering with numeric prefixes and execution order."
sources:
  - https://github.com/nuxt/nuxt/blob/main/docs/2.directory-structure/1.app/1.middleware.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Route middleware are navigation guards: `defineNuxtRouteMiddleware((to, from) => {...})`. Unlike vue-router there is no `next()` argument; redirect or cancellation is handled by returning a value:

- nothing: does not block navigation; moves to the next middleware, if any, or completes navigation.
- `navigateTo('/')`: redirects; the redirect code is 302 Found if it happens on the server side. `navigateTo('/', { redirectCode: 301 })` sets 301 Moved Permanently.
- `abortNavigation()` stops the current navigation; `abortNavigation(error)` rejects it with an error.

Check `to.path` before redirecting, or you might get an infinite redirect loop. The docs recommend these helpers; other return values from the vue-router docs may work but may break in future.

Registration: names are normalised to kebab-case (`myMiddleware` becomes `my-middleware`). Only files at the top level of `middleware/`, or index files within subdirectories, are registered; an index file takes the folder's name (`middleware/auth/index.ts` is `auth`). The `.global` suffix makes a middleware run on every route change.

Order: global middleware first, then page-defined middleware in array order. With `analytics.global.ts`, `setup.global.ts`, `auth.ts` and a page listing `[inlineFunction, 'auth']`, the sequence is analytics, setup, inline, auth. Global middleware runs alphabetically by filename by default; to force an order, prefix with numbers (`01.setup.global.ts`, `02.analytics.global.ts`). Filenames sort as strings, so `10.new.global.ts` comes before `2.new.global.ts`, which is why single digits are zero-padded.

## Checked

2026-11-08. Read in full from the nuxt/nuxt docs repository: docs/2.directory-structure/1.app/1.middleware.md. Confirmed: return values, 302/301 behaviour, registration notes, ordering and the string-sort caveat. Removed: the invented Verify step.

Method: documentation only; no commands were run.
