---
id: computing-software.web-development.nuxt.nuxt-module-anatomy-definenuxtmodule
name: nuxt-module-anatomy-definenuxtmodule
category: computing-software
field: web-development
product: nuxt
tags: [nuxt, nuxt-module, define-nuxt-module, nuxt-kit, module-authoring]
level: advanced
status: docs-checked
description: "Structure a Nuxt module with defineNuxtModule: meta, configKey, defaults, hooks, moduleDependencies, setup and the runtime directory."
sources:
  - https://github.com/nuxt/nuxt/blob/main/docs/3.guide/4.modules/2.module-anatomy.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Two kinds of module: published modules distributed on npm, and "local" modules inside a Nuxt project, either inlined in Nuxt config or in the `modules` directory. In either case they work in the same way. At a low level a module is a simple, potentially asynchronous, function `(inlineOptions, nuxt) => {}` that can read `nuxt.options` and call `nuxt.hook`. The docs do not recommend that form; they recommend `defineNuxtModule` from `@nuxt/kit` with the object syntax and a `meta` property, especially when publishing to npm:

```ts
import { defineNuxtModule } from '@nuxt/kit'
export default defineNuxtModule({
  meta: {
    name: '@nuxtjs/example',      // usually the npm package name
    configKey: 'sample',          // key in nuxt.config that holds your module options
    compatibility: { nuxt: '>=3.0.0' },  // semver of supported Nuxt versions
  },
  defaults: {},                   // or a function returning the defaults
  hooks: {},                      // shorthand sugar to register Nuxt hooks
  moduleDependencies: {
    'some-module': { version: '>=2', optional: true, overrides: {}, defaults: {} },
  },
  setup (moduleOptions, nuxt) {}, // module logic, can be asynchronous
})
```

`moduleDependencies` is configuration for other modules: it does not ensure the module runs before yours, but lets you change the other module's configuration before it runs. `version` is a constraint; if the user has a different version installed, Nuxt throws an error on startup. By default dependencies are added to the list of modules Nuxt installs unless `optional` is set. `overrides` is configuration that overrides `nuxt.options`; `defaults` is configuration that overrides module defaults but not anything set in `nuxt.options`.

`defineNuxtModule` returns a wrapper with the low-level signature that applies defaults before calling `setup`. It supports `defaults` and `meta.configKey` for merging module options; type hints and inference; installing the module only once using a unique key from `meta.name` or `meta.configKey`; automatic hook registration; compatibility checks from module meta; exposing `getOptions` and `getMeta` for internal Nuxt usage; backward and upward compatibility as long as the module uses `defineNuxtModule` from the latest `@nuxt/kit`; and integration with module builder tooling.

Runtime code: modules, like everything in Nuxt config, are not included in the app runtime. To provide or inject runtime code, use a runtime directory (starter: `src/runtime/`; module definition at `src/module.ts`). It can hold Vue components, composables and Nuxt plugins; Nitro API routes, middlewares and plugins; or other assets such as stylesheets, 3D models and images, all injected from the module definition. Published modules cannot use auto-imports for assets in their runtime directory; they must import explicitly from `#imports` or similar, because auto-imports are not enabled for files within `node_modules` for performance reasons.

## Checked

2026-11-04. Confirmed against the Nuxt "Understand Module Structure" page: the two module kinds, low-level signature, the recommendation against it, every meta/defaults/hooks/moduleDependencies/setup field and its comment, the wrapper feature list, the runtime directory contents and the node_modules auto-import warning. Corrected the draft's loose wording of moduleDependencies defaults and overrides to the page's wording. Removed the Verify step.

Method: documentation only; no commands were run.
