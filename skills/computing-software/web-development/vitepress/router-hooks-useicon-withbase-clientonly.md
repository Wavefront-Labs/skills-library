---
id: computing-software.web-development.vitepress.router-hooks-useicon-withbase-clientonly
name: router-hooks-useicon-withbase-clientonly
category: computing-software
field: web-development
product: vitepress
tags: [vitepress, userouter, router-hooks, onbeforeroutechange, useicon, iconify, withbase, content-component]
level: sme
status: docs-checked
description: "Navigate with useRouter().go, hook route changes, render iconify icons with useIcon/VPIcon, and use withBase, Content and ClientOnly."
sources:
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/reference/runtime-api.md
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/reference/site-config.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**`useRouter()`** returns the router:

```ts
interface Router {
  route: Route
  go: (to?: string) => Promise<void>
  onBeforeRouteChange?: (to: string) => Awaitable<void | boolean>   // false cancels
  onBeforePageLoad?: (to: string) => Awaitable<void | boolean>      // false cancels
  onAfterPageLoad?: (to: string) => Awaitable<void>
  onAfterRouteChange?: (to: string) => Awaitable<void>
}
```

Assign handlers on the instance (`router.onBeforeRouteChange = (to) => {...}`), also available from `enhanceApp({ router })`.

**`useIcon(icon, el?)`** renders an iconify icon via VitePress's icon pipeline. Pass a fully qualified `collection:name` resolved against the `@iconify-json/*` packages in your dependencies; it returns the class `vpi-<collection>-<name>`.

```vue
<script setup>
import { useIcon } from 'vitepress'
import { useTemplateRef } from 'vue'
const el = useTemplateRef('el')
const iconClass = useIcon('lucide:rocket', el)
</script>
<template><span ref="el" :class="iconClass" /></template>
```

Icons are collected during SSR so the build emits their styles; nothing is fetched from an external service. In dev they are served on demand. Pass the element ref so dev can resolve it. The default theme's `VPIcon` component wraps this (`<VPIcon icon="lucide:rocket" />`, also accepting `{ svg }`). Icons rendered only on the client (inside `<ClientOnly>`) cannot be collected; list them in the `icons.include` site option.

**`withBase(path)`** prepends the configured base. **`<Content />`** renders the page's Markdown (for custom layouts). **`<ClientOnly />`** renders its slot only in the browser.

Verify: install `@iconify-json/lucide`, render an icon and confirm it appears in a production build.

## Checked

Read the runtime-api reference in full and the `icons` option in the site-config reference. Confirmed the Router interface and hooks, assigning handlers on the router, `useIcon` behaviour and its `vpi-<collection>-<name>` class, `VPIcon`, `icons.include`, `withBase`, `Content` and `ClientOnly`. Nothing removed.

Method: docs-only read of cited pages, 2026-11-08
