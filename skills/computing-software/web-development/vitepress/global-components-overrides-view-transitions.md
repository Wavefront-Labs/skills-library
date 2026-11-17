---
id: computing-software.web-development.vitepress.global-components-overrides-view-transitions
name: global-components-overrides-view-transitions
category: computing-software
field: web-development
product: vitepress
tags: [vitepress, global-components, component-alias, override-internal-components, view-transitions-api, vpnavbar, appearance-toggle]
level: sme
status: docs-checked
description: "Register global Vue components, override internal default-theme components via Vite aliases, and know the View Transitions notes."
sources:
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/guide/extending-default-theme.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Register global components** in `enhanceApp`:

```ts
import type { Theme } from 'vitepress'
import DefaultTheme from 'vitepress/theme'

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    app.component('MyGlobalComponent' /* ... */)
  }
} satisfies Theme
```

With Vite you can use glob imports to auto-register a whole directory of components. Names with a hyphen or PascalCase only (see the Vue components skill). Components referenced from nav config (`component: 'Name'`) or a custom `layout: foo` frontmatter must be registered this way.

**Override internal components** with Vite aliases in config:

```ts
import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vitepress'

export default defineConfig({
  vite: {
    resolve: {
      alias: [{
        find: /^.*\/VPNavBar\.vue$/,
        replacement: fileURLToPath(new URL('./theme/components/CustomNavBar.vue', import.meta.url))
      }]
    }
  }
})
```

Find the exact names in the repo folder `src/client/theme-default/components`. They are internal, so names can change between minor releases.

**View Transitions API.** The docs show a custom `Layout.vue` (a component from their docs source) that animates the light/dark toggle, with a warning about flashing colours and sudden movement. Route-change transitions are marked "coming soon". See Chrome's View Transitions documentation for the API itself.

## Checked

2026-11-04. Confirmed against the VitePress extending-default-theme guide (Registering Global Components, Overriding Internal Components, Using View Transitions API), the using-vue guide (hyphen or PascalCase names) and the default-theme-nav page (custom components must be registered globally). Removed: the advice to prefer slots or variables over aliasing, and the Verify step.

Method: documentation only; no commands were run.
