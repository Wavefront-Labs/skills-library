---
id: computing-software.web-development.vitepress.runtime-api-usedata-useroute
name: runtime-api-usedata-useroute
category: computing-software
field: web-development
product: vitepress
tags: [vitepress, runtime-api, usedata, useroute, page-data, site-data, isdark, frontmatter-ref, params]
level: practitioner
status: docs-checked
description: "Read page, site, theme, frontmatter, params, lang, dark mode and hash via useData(), and the current route via useRoute()."
sources:
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/reference/runtime-api.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Helpers are importable from `vitepress` in theme components and also in `.md` pages (compiled to SFCs). Names starting with `use` are Vue composables callable only in `setup()` or `<script setup>`.

**`useData()`** returns refs:

```ts
interface VitePressData<T = any> {
  site: Ref<SiteData<T>>        // site-level metadata
  theme: Ref<T>                 // themeConfig
  page: Ref<PageData>
  frontmatter: Ref<PageData['frontmatter']>
  params: Ref<PageData['params']>   // dynamic route params
  title: Ref<string>; description: Ref<string>; lang: Ref<string>
  isDark: Ref<boolean>
  dir: Ref<'ltr' | 'rtl' | 'auto'>
  localeIndex: Ref<string>
  hash: Ref<string>             // current location hash
}
interface PageData {
  title: string; titleTemplate?: string | boolean; description: string
  relativePath: string; filePath: string; headers: Header[]
  frontmatter: Record<string, any>; params?: Record<string, any>
  isNotFound?: boolean; lastUpdated?: number
}
```

`page.headers` is populated only when `markdown.headers` is enabled; otherwise it is an empty array (the default outline still works because it reads rendered headings).

```vue
<script setup>
import { useData } from 'vitepress'
const { theme } = useData()
</script>
<template><h1>{{ theme.footer.copyright }}</h1></template>
```

**`useRoute()`** returns `{ path: string, data: PageData, component: Component | null }`.

Inside Markdown, template globals `$frontmatter` and `$params` give direct access in expressions.

Gotcha: `use*` composables work only inside `setup()` or `<script setup>`, and the values `useData()` returns are `Ref`s.

Verify: print `page.value.relativePath` and compare with the file's location.

## Checked

2026-11-08. Read the VitePress docs source page reference/runtime-api. Confirmed the VitePressData and PageData types, the page.headers note tied to markdown.headers, the useData example, the Route shape, the use* composable rule and the $frontmatter and $params globals. Replaced a generic Vue gotcha that the page does not state.

Method: docs-only read of cited pages, 2026-11-08
