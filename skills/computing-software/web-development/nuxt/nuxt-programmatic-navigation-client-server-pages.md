---
id: computing-software.web-development.nuxt.nuxt-programmatic-navigation-client-server-pages
name: nuxt-programmatic-navigation-client-server-pages
category: computing-software
field: web-development
product: nuxt
tags: [nuxt, navigate-to, client-pages, server-pages, nuxt-link]
level: practitioner
status: docs-checked
description: "Navigate programmatically with navigateTo, and mark pages as client-only (.client.vue) or server-only (.server.vue) with their constraints."
sources:
  - https://github.com/nuxt/nuxt/blob/main/docs/2.directory-structure/1.app/1.pages.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Use `<NuxtLink>` (included with Nuxt, no import needed) to navigate between pages and the `navigateTo()` utility for programmatic navigation. Always `await` `navigateTo` or chain its result by returning it from functions:

```ts
function navigate () {
  return navigateTo({ path: '/search', query: { name: name.value, type: type.value } })
}
```

Client-only pages: give the file a `.client.vue` suffix; none of the content of the page is rendered on the server.

Server-only pages: give the file a `.server.vue` suffix. You can navigate to the page with client-side navigation (controlled by `vue-router`), but it is rendered with a server component automatically, so the code required to render the page is not in your client-side bundle. They must have a single root element (HTML comments count). Navigating to one needs a request to render it, so when a `<NuxtLink>` to one is prefetched, Nuxt prefetches that response as well.

Custom routing: Nuxt exposes the router, routes and router options for customization (see the custom routing recipe in the docs). By default all pages live in one `pages` directory at the project root; to group pages in several places use Nuxt Layers: a folder such as `some-app/` with its own `nuxt.config.ts` and `pages/`, then `extends: ['./some-app']` in the root `nuxt.config.ts`.

## Checked

2026-11-04. Confirmed against the Nuxt pages directory page: NuxtLink and navigateTo with the await note and search example, .client.vue and .server.vue behaviour, single-root warning, prefetch note, custom routing pointer, Layers example. Corrected the layers folder to pages/ (the page shows some-app/pages). Removed the Verify step.

Method: documentation only; no commands were run.
