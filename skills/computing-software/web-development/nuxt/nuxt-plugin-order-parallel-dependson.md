---
id: computing-software.web-development.nuxt.nuxt-plugin-order-parallel-dependson
name: nuxt-plugin-order-parallel-dependson
category: computing-software
field: web-development
product: nuxt
tags: [nuxt, plugins, plugin-order, parallel, dependson]
level: advanced
status: docs-checked
description: "Control plugin order with numeric filename prefixes, run plugins in parallel, and declare dependencies with dependsOn."
sources:
  - https://github.com/nuxt/nuxt/blob/main/docs/2.directory-structure/1.app/1.plugins.md
  - https://github.com/nuxt/nuxt/blob/main/docs/4.api/3.utils/define-nuxt-plugin.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Registration order: control the order in which plugins are registered by prefixing the file names with "alphabetical" numbering, for example `plugins/01.myPlugin.ts` then `plugins/02.myOtherPlugin.ts`. `02.myOtherPlugin.ts` can then access anything injected by `01.myPlugin.ts`, which is useful when one plugin depends on another. Filenames are sorted as strings, not numbers, so `10.myPlugin.ts` comes before `2.myOtherPlugin.ts`; this is why the example prefixes single digits with `0`.

Parallel plugins: by default Nuxt loads plugins sequentially. Define a plugin with `parallel: true` (object syntax) so Nuxt does not wait until the end of its execution before loading the next plugin.

```ts
export default defineNuxtPlugin({
  name: 'my-plugin',
  parallel: true,
  async setup (nuxtApp) {
    // the next plugin will be executed immediately
  },
})
```

Plugins with dependencies: if a plugin needs to wait for another plugin before it runs, add that plugin's `name` to the `dependsOn` array:

```ts
export default defineNuxtPlugin({
  name: 'depends-on-my-plugin',
  dependsOn: ['my-plugin'],
  async setup (nuxtApp) {
    // this plugin will wait for the end of `my-plugin`'s execution before it runs
  },
})
```

The API page lists the related object-syntax properties: `name` (optional, useful for debugging and dependency management), `enforce` (`'pre'`, `'default'` or `'post'`; controls when the plugin runs relative to other plugins), `dependsOn` (names of plugins this one depends on), `order` (granular control for advanced users only; it overrides `enforce` and is used to sort plugins) and `parallel` (execute in parallel with other parallel plugins).

With object syntax the properties are statically analyzed to produce a more optimized build, so do not define them at runtime. Setting `enforce: import.meta.server ? 'pre' : 'post'` would defeat any future optimization Nuxt can do.

Plugins are called in order, sequentially, before everything else, so a composable used in a plugin may depend on another plugin that has not been called yet.

## Checked

2026-11-04. Confirmed against the Nuxt plugins directory page (registration order, parallel, dependsOn, static analysis note, composable ordering warning) and the defineNuxtPlugin API page (property table including enforce values and order). Removed the draft's claim that default order is alphabetical filename order (the page only describes numbering), the claim that dependsOn works "even when parallel loading is used", the "typical use" paragraph and the Verify step.

Method: documentation only; no commands were run.
