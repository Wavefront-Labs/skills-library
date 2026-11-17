---
id: computing-software.web-development.nuxt.nuxt-vue-compiler-options
name: nuxt-vue-compiler-options
category: computing-software
field: web-development
product: nuxt
tags: [nuxt, vue, vite, vue-jsx, props-destructure]
level: practitioner
status: docs-checked
description: "Pass options to the Vue and Vue JSX Vite plugins, vue-loader under webpack, and enable experimental Vue features such as propsDestructure from nuxt.config."
sources:
  - https://github.com/nuxt/nuxt/blob/main/docs/1.getting-started/03.configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Vue options are set in `nuxt.config`, per builder.

With Vite, use `vite.vue` for `@vitejs/plugin-vue` options and `vite.vueJsx` for `@vitejs/plugin-vue-jsx` options:

```ts
export default defineNuxtConfig({
  vite: {
    vue: { customElement: true },
    vueJsx: { mergeProps: true },
  },
})
```

With webpack, configure `vue-loader` through the `webpack.loaders.vue` key:

```ts
export default defineNuxtConfig({
  webpack: { loaders: { vue: { hotReload: true } } },
})
```

To enable experimental Vue features such as `propsDestructure`, use the `vue` key. The page says this works no matter which builder you use:

```ts
export default defineNuxtConfig({
  vue: { propsDestructure: true },
})
```

Migration note from the page: since Nuxt 3.9 and Vue 3.4, the experimental `reactivityTransform` has moved from Vue to Vue Macros, which has a Nuxt integration.

The page links to each plugin's available options (plugin-vue, plugin-vue-jsx, and vue-loader's index source). It also says Nuxt uses `nuxt.config.ts` as the single source of truth and skips reading external config files such as `vite.config.ts` (configure Vite through the `vite` key).

## Checked

2026-11-08. Read in full from the nuxt/nuxt docs repository: docs/1.getting-started/03.configuration.md (Vue Configuration and External Configuration Files sections). Confirmed: the three config snippets, the builder-independence of the vue key, the reactivityTransform note. Removed: the claim that Vite is the default builder, the "do not look under vue any more" advice, and the invented Verify step (customElement/.ce.vue effects).

Method: documentation only; no commands were run.
