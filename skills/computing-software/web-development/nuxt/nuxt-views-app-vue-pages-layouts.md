---
id: computing-software.web-development.nuxt.nuxt-views-app-vue-pages-layouts
name: nuxt-views-app-vue-pages-layouts
category: computing-software
field: web-development
product: nuxt
tags: [nuxt, app-vue, pages, layouts, nuxt-page, nuxt-layout]
level: intro
status: docs-checked
description: "Understand Nuxt's view layers: app.vue entry, auto-imported components, pages with NuxtPage, and layouts with NuxtLayout and a default slot."
sources:
  - https://github.com/nuxt/nuxt/blob/main/docs/1.getting-started/04.views.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Nuxt builds the UI from four layers, all under `app/`.

1. `app/app.vue` is the entrypoint rendered for every route. There is no `main.js`; Nuxt creates the Vue app for you.
2. `app/components/` holds reusable pieces that are auto-imported, so `<AppAlert>` works in any template without an import.
3. `app/pages/` turns each file into a route. To use pages, add `app/pages/index.vue` and put `<NuxtPage />` in `app.vue` (or remove `app/app.vue` to use the default entry).
4. `app/layouts/` holds wrappers with a `<slot />`. `app/layouts/default.vue` is used by default; wrap `<NuxtPage />` in `<NuxtLayout>` in `app.vue` as below.

```vue
<template>
  <div>
    <NuxtLayout>
      <NuxtPage />
    </NuxtLayout>
  </div>
</template>
```

```vue
<template>
  <div>
    <AppHeader />
    <slot />
    <AppFooter />
  </div>
</template>
```

If the app has only one layout, the docs recommend skipping layouts and putting the shared header and footer straight in `app.vue` around `<NuxtPage />`. More layouts are chosen per page (see the layouts skill).

Verify: `/about` renders `pages/about.vue` inside the default layout, and a component placed in `app/components/` appears with no import statement.

## Checked

2026-11-08. Read the Nuxt Views doc in full. Confirmed app.vue, auto-imported components, pages, layouts and the single-layout recommendation. Reworded two sentences that went beyond the doc (default entry behaviour, default layout usage).

Method: documentation only; no commands were run.
