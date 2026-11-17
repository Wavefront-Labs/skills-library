---
id: computing-software.web-development.nuxt.nuxt-file-system-routing-basics
name: nuxt-file-system-routing-basics
category: computing-software
field: web-development
product: nuxt
tags: [nuxt, routing, vue-router, pages, nuxt-link]
level: intro
status: docs-checked
description: "Nuxt file-system routing: pages/ files become vue-router routes, NuxtLink for navigation with prefetch, and route params through useRoute."
sources:
  - https://github.com/nuxt/nuxt/blob/main/docs/1.getting-started/07.routing.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Nuxt routing is based on vue-router. Every Vue file inside the `app/pages/` directory creates a corresponding route, based on its filename: `pages/index.vue` is `/`, `pages/about.vue` is `/about`, `pages/posts/[id].vue` is `/posts/:id`. Nuxt uses dynamic imports for each page, so code-splitting ships the minimum JavaScript for the requested route.

Navigate with `<NuxtLink to="/about">About</NuxtLink>`. It renders an `<a>` tag with the `href` set to the route of the page. Once the application is hydrated, page transitions are performed in JavaScript by updating the browser URL, which prevents full-page refreshes. When a `<NuxtLink>` enters the viewport on the client side, Nuxt automatically prefetches components and payload (generated pages) of the linked page ahead of time.

Read parameters with `useRoute()` in a `<script setup>` block or `setup()` method:

```vue
<script setup lang="ts">
const route = useRoute()
// When accessing /posts/1, route.params.id will be 1
console.log(route.params.id)
</script>
```

Code-splitting is enabled by default and recommended for most apps. The docs show how to disable it (`vite.$client.build.rolldownOptions.output.codeSplitting: false` in `nuxt.config`) but note that it ships all JavaScript in one file, rarely helps, and usually increases the initial download even on slow connections, so only disable it if you have measured that it helps.

## Checked

2026-11-04. Confirmed against the Nuxt routing page: file-system routes and the generated route examples, dynamic-import code splitting, NuxtLink rendering, hydration behaviour and viewport prefetch, useRoute example, the codeSplitting option and its caveat. Removed the cross-reference sentence to other skills and the Verify step.

Method: documentation only; no commands were run.
