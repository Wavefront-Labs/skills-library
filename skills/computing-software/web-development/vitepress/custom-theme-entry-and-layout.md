---
id: computing-software.web-development.vitepress.custom-theme-entry-and-layout
name: custom-theme-entry-and-layout
category: computing-software
field: web-development
product: vitepress
tags: [vitepress, custom-theme, theme-interface, enhanceapp, layout-component, content-component, theme-entry, usedata]
level: advanced
status: docs-checked
description: "Create .vitepress/theme/index.ts exporting Layout, enhanceApp, setup and extends, then build a layout with Content, 404 and layout: home handling."
sources:
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/guide/custom-theme.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Resolving.** A theme entry file at `.vitepress/theme/index.js` or `index.ts` replaces the default theme entirely (unless it `extends` it).

**Interface**

```ts
interface Theme {
  Layout: Component                                     // required, root layout for every page
  enhanceApp?: (ctx: EnhanceAppContext) => Awaitable<void>
  setup?: () => void                                    // runs inside root setup()
  extends?: Theme                                       // base theme; its enhanceApp and setup run first
}
interface EnhanceAppContext { app: App; router: Router; siteData: Ref<SiteData> }
```

Only `Layout` is required; a theme can be one Vue component. `@vitejs/plugin-vue` is pre-configured, so import `.vue` files directly. Theme code must be SSR-compatible.

**Router hooks in enhanceApp.**

```ts
enhanceApp({ router }) {
  router.onBeforeRouteChange = (to) => { /* return false to cancel */ }
  router.onAfterRouteChange = (to) => { }
}
```

**`setup`** allows composables like `watch` and `onMounted` without wrapping the layout; with `extends` it runs base-first and also during SSR, so keep browser work in `onMounted`.

**Minimal layout.** It must contain `<Content />` (renders the page's Markdown):

```vue
<script setup>
import { useData } from 'vitepress'
const { page, frontmatter } = useData()
</script>
<template>
  <div v-if="page.isNotFound">Custom 404 page!</div>
  <div v-else-if="frontmatter.layout === 'home'">Custom home page!</div>
  <Content v-else />
</template>
```

Split into `NotFound`, `Home`, `Page` components as it grows. Combine with data loaders for post lists.

## Checked

2026-11-04. Confirmed against the VitePress custom-theme guide (Theme Resolving, Theme Interface, router hooks, setup hook, Building a Layout). The minimal layout template uses a v-else-if chain, which is plain Vue and not taken from the page (the page's example uses separate v-if blocks). Removed: the remark about a pitfall in the docs example and the Verify step.

Method: documentation only; no commands were run.
