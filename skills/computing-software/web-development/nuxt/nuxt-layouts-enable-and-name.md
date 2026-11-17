---
id: computing-software.web-development.nuxt.nuxt-layouts-enable-and-name
name: nuxt-layouts-enable-and-name
category: computing-software
field: web-development
product: nuxt
tags: [nuxt, layouts, nuxt-layout, define-page-meta, default-layout]
level: practitioner
status: docs-checked
description: "Enable layouts with NuxtLayout, pick them via definePageMeta, the name prop or appLayout route rules, and understand layout name normalisation."
sources:
  - https://github.com/nuxt/nuxt/blob/main/docs/2.directory-structure/1.app/1.layouts.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Components in the layouts directory are loaded via asynchronous import when used. Enable layouts by adding `<NuxtLayout>` to `app.vue`, around `<NuxtPage />`. In a layout file, the page content is displayed in the `<slot />`.

Pick a layout in one of three ways: set `layout` with `definePageMeta` on the page, set the `name` prop of `<NuxtLayout>` (for example `<NuxtLayout :name="layout">` chosen from an API call or logged-in status), or set the `appLayout` property in route rules (marked v4.3 in the docs). Route rules are useful to manage layouts centrally or for routes without page components, such as catchall pages:

```ts
export default defineNuxtConfig({
  routeRules: {
    '/admin': { appLayout: 'admin' },
    '/dashboard/**': { appLayout: 'dashboard' },
    '/landing': { appLayout: false }, // disable layout for a route
  },
})
```

Rules from the docs:
- With no layout specified, `app/layouts/default.vue` is used.
- Names are normalized to kebab-case: `someLayout` becomes `some-layout`.
- Layouts in nested directories are named from their path directory and filename, with duplicate segments removed: `~/layouts/desktop/default.vue` is `desktop-default`, `~/layouts/desktop-base/base.vue` is `desktop-base`, `~/layouts/desktop/index.vue` is `desktop`. For clarity the docs recommend the filename match the name (`DesktopDefault.vue`).
- Layouts must have a single root element to allow Nuxt to apply transitions between layout changes, and this root element cannot be a `<slot />`.
- If you only have a single layout in your application, the docs recommend using `app.vue` instead.

Typing: layout names can be declared via the `NuxtLayouts` interface in `declare module 'nuxt/app'`.

## Checked

2026-11-04. Confirmed against the Nuxt layouts page: NuxtLayout in app.vue, the three ways to choose a layout, appLayout route rules and v4.3 badge, default.vue, kebab-case normalisation, nested naming table, single-root rule, app.vue recommendation, NuxtLayouts augmentation. Replaced the empty routeRules placeholder with the page's example. Removed the Verify step.

Method: documentation only; no commands were run.
