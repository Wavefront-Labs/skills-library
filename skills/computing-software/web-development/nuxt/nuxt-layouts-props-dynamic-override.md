---
id: computing-software.web-development.nuxt.nuxt-layouts-props-dynamic-override
name: nuxt-layouts-props-dynamic-override
category: computing-software
field: web-development
product: nuxt
tags: [nuxt, layouts, set-page-layout, layout-props, nuxt-layout]
level: advanced
status: docs-checked
description: "Change layouts at runtime with setPageLayout, pass typed props to layouts, and take manual control with layout false plus NuxtLayout in a page."
sources:
  - https://github.com/nuxt/nuxt/blob/main/docs/2.directory-structure/1.app/1.layouts.md
  - https://github.com/nuxt/nuxt/blob/main/docs/4.api/3.utils/set-page-layout.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Dynamic switching: `setPageLayout('custom')` changes the layout dynamically (the docs' example calls it from a button handler in a page that sets `definePageMeta({ layout: false })`). It relies on the Nuxt context, so it can only be called within the Nuxt context. A common place is route middleware, where it sets the layout of the route you are navigating to:

```ts
export default defineNuxtRouteMiddleware((to) => {
  setPageLayout('other')
})
```

If you set the layout dynamically on the server side, you must do so before the layout is rendered by Vue (within a plugin or route middleware) to avoid a hydration mismatch.

Props to layouts (the layouts page marks this +4.4, the setPageLayout page marks its props v4.3):
- From the page: `definePageMeta({ layout: { name: 'panel', props: { sidebar: true, title: 'Dashboard' } } })`.
- From code (second argument): `setPageLayout('panel', { sidebar: true, title: 'Dashboard' })`.

The layout declares them with `defineProps<{ sidebar?: boolean, title?: string }>()`. Props set via `definePageMeta` are typed from the layout's `defineProps`, with autocomplete and type-checking in your editor.

Per-page override: if you are using pages, set `layout: false` in `definePageMeta` and use the `<NuxtLayout name="custom">` component inside the page yourself; the page can then fill named layout slots such as `<template #header>`. If you use `<NuxtLayout>` within your pages, make sure it is not the root element (or disable layout/page transitions).

## Checked

2026-11-04. Confirmed against the Nuxt layouts page and the setPageLayout page: setPageLayout usage, Nuxt-context requirement, middleware example, server-side timing note, props via definePageMeta and setPageLayout, typing tip, per-page NuxtLayout override and its root-element warning. Removed: the v4.4-only version claim (the two pages disagree), the claim about wrapping multi-element layouts in a div, the appLayout advice sentence and the Verify step.

Method: documentation only; no commands were run.
