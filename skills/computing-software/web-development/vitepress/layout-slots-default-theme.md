---
id: computing-software.web-development.vitepress.layout-slots-default-theme
name: layout-slots-default-theme
category: computing-software
field: web-development
product: vitepress
tags: [vitepress, layout-slots, doc-before, aside-outline-before, home-hero-info, nav-bar-content-after, layout-top, wrapper-layout]
level: advanced
status: docs-checked
description: "Inject content into the default theme Layout through named slots by wrapping Layout, listed per layout type."
sources:
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/guide/extending-default-theme.md
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/reference/default-theme-footer.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Wrap the default `Layout` and fill slots:

```js
// .vitepress/theme/index.js
import DefaultTheme from 'vitepress/theme'
import MyLayout from './MyLayout.vue'
export default { extends: DefaultTheme, Layout: MyLayout }
```

```vue
<script setup>
import DefaultTheme from 'vitepress/theme'
const { Layout } = DefaultTheme
</script>
<template>
  <Layout>
    <template #aside-outline-before>My custom sidebar top content</template>
  </Layout>
</template>
```

The default theme's `<Layout/>` has slots that inject content at fixed locations; the example above places a component before the outline. The wrapper replaces the theme's `Layout` while `extends` keeps everything else. A render-function form works too: `Layout() { return h(DefaultTheme.Layout, null, { 'aside-outline-before': () => h(MyComponent) }) }`.

**Slots by layout**
- `layout: doc` (default): `doc-top`, `doc-bottom`, `doc-footer-before`, `doc-before`, `doc-after`, `sidebar-nav-before`, `sidebar-nav-after`, `aside-top`, `aside-bottom`, `aside-outline-before`, `aside-outline-after`, `aside-ads-before`, `aside-ads-after`.
- `layout: home`: `home-hero-before`, `home-hero-info-before`, `home-hero-info`, `home-hero-info-after`, `home-hero-actions-before-actions`, `home-hero-actions-after`, `home-hero-image`, `home-hero-after`, `home-features-before`, `home-features-after`.
- `layout: page`: `page-top`, `page-bottom`.
- 404: `not-found`.
- Always: `layout-top`, `layout-bottom`, `nav-bar-title-before`, `nav-bar-title-after`, `nav-bar-content-before`, `nav-bar-content-after`, `nav-screen-content-before`, `nav-screen-content-after`.

The `footer` theme option takes inline elements only (it renders inside a `<p>`); for block-level footer content use the `layout-bottom` slot.

Verify: your component appears at the intended location on the right layout only.

## Checked

Read the extending-default-theme guide in full and the default-theme footer page. Confirmed: the `extends` plus `Layout` wrapper, the render-function form, every slot name per layout, and the inline-only footer note with the `layout-bottom` pointer. Removed the unsourced advice to use `doc-footer-before` for comment widgets.

Method: docs-only read of cited pages, 2026-11-08
