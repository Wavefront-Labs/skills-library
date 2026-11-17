---
id: computing-software.web-development.nuxt.nuxt-named-views-and-route-groups
name: nuxt-named-views-and-route-groups
category: computing-software
field: web-development
product: nuxt
tags: [nuxt, pages, named-views, route-groups, nuxt-page]
level: advanced
status: docs-checked
description: "Render one route into several NuxtPage outlets with name@view.vue files, and group routes in (folder) without changing URLs."
sources:
  - https://github.com/nuxt/nuxt/blob/main/docs/2.directory-structure/1.app/1.pages.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Named views (the docs mark this v4.5): a single route can render into multiple `<NuxtPage>` outlets in a parent component by giving each outlet a `name` and providing a sibling page file for each name. Use the `name@view.vue` filename convention alongside the default route file:

```bash
pages/
  parent/
    child.vue
    child@sidebar.vue
  parent.vue
```

```vue
<!-- pages/parent.vue -->
<div>
  <NuxtPage />
  <aside><NuxtPage name="sidebar" /></aside>
</div>
```

When the user navigates to `/parent/child`, `child.vue` renders into the default `<NuxtPage />` and `child@sidebar.vue` into `<NuxtPage name="sidebar" />`. Outlets without a matching named view are left empty. `definePageMeta` is read from the default route file only; meta declared inside a `name@view.vue` sibling has no effect on the route.

Route groups: to group routes without affecting file-based routing, put files in a folder wrapped in parentheses. `pages/(marketing)/about.vue` and `contact.vue` produce `/about` and `/contact`; the `marketing` group is ignored for the URL structure.

From v4.3 (per the docs) route groups are automatically available in route metadata as `route.meta.groups`, for example `['marketing']`, for conditional logic or styling:

```vue
const route = useRoute()
route.meta.groups?.includes('marketing')
```

## Checked

2026-11-04. Confirmed against the Nuxt pages directory page: named view convention, example tree and outlets, empty-outlet and definePageMeta notes, route group behaviour, route.meta.groups, version badges (v4.5 and v4.3). Removed the Verify step.

Method: documentation only; no commands were run.
