---
id: computing-software.web-development.nuxt.nuxt-pages-dynamic-catchall-nested
name: nuxt-pages-dynamic-catchall-nested
category: computing-software
field: web-development
product: nuxt
tags: [nuxt, pages, dynamic-routes, catch-all, nested-routes]
level: practitioner
status: docs-checked
description: "Build Nuxt routes from filenames: [param], [[optional]], [...slug] catch-all, nested parent/child with NuxtPage, and precedence rules."
sources:
  - https://github.com/nuxt/nuxt/blob/main/docs/2.directory-structure/1.app/1.pages.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The `pages/` directory is optional: vue-router is not included if you only use `app.vue`. To force the pages system set `pages: true` in `nuxt.config`. Pages are Vue components with any valid extension Nuxt supports (by default `.vue`, `.js`, `.jsx`, `.mjs`, `.ts` or `.tsx`). With an `app.vue`, use `<NuxtPage />` to display the current page.

Pages must have a single root element (HTML comments count as elements) to allow route transitions. Otherwise the route renders fine when server-rendered or statically generated, but during client-side navigation the transition fails and the route is not rendered.

Naming rules:
- Anything in square brackets becomes a dynamic route parameter; `users-[group]/[id].vue` at `/users-admins/123` gives `$route.params.group` of `admins` and `params.id` of `123`. Read it with `useRoute().params` or `$route`.
- `[[slug]].vue` or `[[slug]]/index.vue` makes the parameter optional and matches both `/` and `/test`.
- `[...slug].vue` is a catch-all that matches all routes under that path; `$route.params.slug` is an array (`["hello", "world"]` for `/hello/world`).
- Nested routes: `parent.vue` plus `parent/child.vue` produce a parent route with children; insert `<NuxtPage>` inside `parent.vue` to display the child. Props passed to it (`<NuxtPage :foobar="123" />`) are received by the child component.
- Precedence: named parent routes take priority over nested dynamic routes, so for `/foo/hello`, `pages/foo.vue` wins over `pages/foo/[slug].vue`. Use `pages/foo/index.vue` and `pages/foo/[slug].vue` to match `/foo` and `/foo/hello` with different pages.

Child route keys: for more control over when `<NuxtPage>` re-renders, pass a string or function via the `pageKey` prop (`:page-key="route => route.fullPath"`) or define `key` in `definePageMeta` in the child.

Prerendering note from the docs: pages are only automatically registered for prerendering if you have not disabled `prerender.crawlLinks` and you have at least one page in your `prerender.routes` list.

## Checked

2026-11-04. Confirmed against the Nuxt pages directory page: optional pages directory and pages: true, extensions, single-root rule and its client-navigation failure, dynamic, optional and catch-all naming, nested routes and props, precedence note, child route keys, prerendering tip. Reworded the prerendering note to match the page (crawlLinks not disabled). Removed the Verify step.

Method: documentation only; no commands were run.
