---
id: computing-software.web-development.nuxt.nuxt-plugins-creation-and-registration
name: nuxt-plugins-creation-and-registration
category: computing-software
field: web-development
product: nuxt
tags: [nuxt, plugins, define-nuxt-plugin, nuxtapp, provide]
level: practitioner
status: docs-checked
description: "Create Nuxt plugins (function and object syntax), know which files auto-register, suffix by environment, and provide helpers on nuxtApp."
sources:
  - https://github.com/nuxt/nuxt/blob/main/docs/2.directory-structure/1.app/1.plugins.md
  - https://github.com/nuxt/nuxt/blob/main/docs/4.api/3.utils/define-nuxt-plugin.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Nuxt automatically reads the files in `app/plugins/` and loads them at creation of the Vue application. All plugins there are auto-registered; no `nuxt.config` entry is needed. A `.server` or `.client` suffix in the file name loads a plugin only on that side.

Only files at the top level (or index files within subdirectories) are auto-registered. In the docs example `foo.ts` is scanned, `bar/baz.ts` and `bar/foz.vue` are not, and `bar/index.ts` is "currently scanned but deprecated". To add plugins from subdirectories, list them in the `plugins` option of `nuxt.config.ts`: `plugins: ['~/plugins/bar/baz', '~/plugins/bar/foz']`.

The only argument passed to a plugin is `nuxtApp`:

```ts
export default defineNuxtPlugin((nuxtApp) => {
  // Doing something with nuxtApp
})
```

`defineNuxtPlugin` normalizes the formats into one structure. A function plugin receives `NuxtApp` and may return a promise with an object holding a `provide` property. The object syntax is for more advanced use cases:

```ts
export default defineNuxtPlugin({
  name: 'my-plugin',
  enforce: 'pre', // or 'post'
  async setup (nuxtApp) {
    // equivalent of a normal functional plugin
  },
  hooks: {
    'app:created' () {
      const nuxtApp = useNuxtApp()
    },
  },
  env: {
    // false: do not run when rendering server-only or island components
    islands: true,
  },
})
```

With object syntax, the properties are statically analyzed to produce a more optimized build, so do not define them at runtime (for example `enforce: import.meta.server ? 'pre' : 'post'` would defeat future optimization). Nuxt statically pre-loads hook listeners, so hooks can be defined without worrying about plugin registration order.

Providing helpers: return them under a `provide` key, from either syntax (in object syntax, from `setup`):

```ts
export default defineNuxtPlugin(() => {
  return {
    provide: {
      hello: (msg: string) => `Hello ${msg}!`,
    },
  }
})
```

Use the helper with `const { $hello } = useNuxtApp()` in a component script, or `{{ $hello('world') }}` in the template. The docs highly recommend composables instead, to avoid polluting the global namespace and keep the main bundle entry small.

Composables and utils can be used inside plugins, with two limits: a composable that depends on another plugin registered later might not work, because plugins are called in order, sequentially and before everything else; and a composable that depends on the Vue.js lifecycle will not work, because plugins are bound only to the `nuxtApp` instance, not to a component instance.

## Checked

2026-11-04. Confirmed against the Nuxt plugins directory page and the defineNuxtPlugin API page: auto-registration and suffixes, the scanned/not scanned listing including the index.ts deprecation, config plugins option, function and object syntax, env.islands, static analysis note, provide, usage in components, composable limits. Added the index.ts deprecation note. Removed the Verify step and rewrote the nested-backtick provide example as a code block.

Method: documentation only; no commands were run.
