---
id: computing-software.web-development.vitepress.ssr-compatibility-clientonly
name: ssr-compatibility-clientonly
category: computing-software
field: web-development
product: vitepress
tags: [vitepress, ssr, ssr-compat, clientonly, defineclientcomponent, import-meta-env-ssr, browser-api, hydration]
level: advanced
status: docs-checked
description: "Keep code SSR-safe: ClientOnly, onMounted dynamic imports, import.meta.env.SSR guards, and defineClientComponent."
sources:
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/guide/ssr-compat.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
VitePress pre-renders in Node during production builds, so all theme and page code must be SSR-compatible. Rule of thumb: touch browser/DOM APIs only in `beforeMount` or `mounted` hooks.

**`<ClientOnly>`** for components that are not SSR-friendly (for example, those with custom directives):

```md
<ClientOnly>
  <NonSSRFriendlyComponent />
</ClientOnly>
```

**Libraries that touch `window` on import** must be imported dynamically:

```vue
<script setup>
import { onMounted } from 'vue'
onMounted(() => {
  import('./lib-that-access-window-on-import').then((module) => { /* use */ })
})
</script>
```

or conditionally using the Vite flag:

```js
if (!import.meta.env.SSR) {
  import('./lib-that-access-window-on-import').then((module) => { /* use */ })
}
```

`Theme.enhanceApp` can be async, so you can register such Vue plugins there:

```ts
async enhanceApp({ app }) {
  if (!import.meta.env.SSR) {
    const plugin = await import('plugin-that-access-window-on-import')
    app.use(plugin.default)
  }
}
```

**`defineClientComponent`** wraps a client-only dynamic import:

```vue
<script setup>
import { defineClientComponent } from 'vitepress'
const ClientComp = defineClientComponent(() => import('component-that-access-window-on-import'))
</script>
<template><ClientComp /></template>
```

Its second argument is `h()` args (props, children, slots, refs) and a third optional callback runs after load; the component is only imported in the wrapper's mounted hook.

Verify: `vitepress build` succeeds, since the production build pre-renders pages in Node.

## Checked

Read the SSR Compatibility guide in full. Confirmed the rule of thumb, `ClientOnly`, the mounted-hook and `import.meta.env.SSR` imports, async `enhanceApp`, and `defineClientComponent` arguments and timing. Removed the unsourced claim about `window is not defined` errors appearing only in builds.

Method: docs-only read of cited pages, 2026-11-08
