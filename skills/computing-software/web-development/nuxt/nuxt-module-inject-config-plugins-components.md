---
id: computing-software.web-development.nuxt.nuxt-module-inject-config-plugins-components
name: nuxt-module-inject-config-plugins-components
category: computing-software
field: web-development
product: nuxt
tags: [nuxt, nuxt-module, add-plugin, add-component, add-imports]
level: advanced
status: docs-checked
description: "Module recipes: modify nuxt.options, expose options via runtimeConfig with defu, and register plugins, components and composables with the Kit utilities."
sources:
  - https://github.com/nuxt/nuxt/blob/main/docs/3.guide/4.modules/3.recipes-basics.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Modify config: `nuxt.options.experimental ||= {}; nuxt.options.experimental.componentIslands = true`. For more complex alterations the docs suggest `defu`.

Expose module options to runtime: modules are not part of the app runtime, so their options are not either. Expose what is needed through `runtimeConfig`, extending the user's values rather than overwriting them:

```js
nuxt.options.runtimeConfig.public.myModule = defu(nuxt.options.runtimeConfig.public.myModule, { foo: options.foo })
```

It can then be read in a plugin, component or the app like any other runtime configuration (`useRuntimeConfig().public.myModule`). Do not put sensitive module configuration, such as private API keys, in the public runtime config: it ends up in the public bundle.

Plugins: `const resolver = createResolver(import.meta.url)` then `addPlugin(resolver.resolve('./runtime/plugin'))`.

Components: `addComponent({ name: 'MySuperComponent', export: 'MySuperComponent', filePath: resolver.resolve('runtime/app/components/MySuperComponent.vue') })` (`name` is the name used in templates; `export` is optional, for named rather than default exports). From a library, use `filePath: '@vue/awesome-components'`. Add a whole directory with `addComponentsDir({ path: resolver.resolve('runtime/app/components') })`.

Composables: `addImports({ name: 'useComposable', as: 'useMyComposable', from: resolver.resolve('runtime/app/composables/useComposable') })`, where `as` is an optional alias for consuming apps. Pass an array for several entries, or add a directory with `addImportsDir(resolver.resolve('runtime/composables'))`.

The page highly recommends prefixing exports to avoid conflicts with user code or other modules, and notes that components, pages, composables and other files that would normally be in `app/` need to be in `runtime/app/` so they can be type checked properly.

Other recipes on the same page: `addRouteMiddleware({ global: true, name, path })`; `addServerHandler({ route, handler })`, including dynamic routes such as `/api/_my-module/hello/:name` and catch-all `/api/_my-module/files/**:path`; `nuxt.options.css.push(...)` for a stylesheet; Nitro `publicAssets` via the `nitro:config` hook; and `moduleDependencies` to depend on other modules.

## Checked

2026-11-04. Confirmed against the Nuxt "Add Plugins, Components and More" page: config alteration, the defu runtimeConfig pattern with its secrets warning, addPlugin, addComponent and addComponentsDir, addImports and addImportsDir, the prefix and runtime/app notes, and the other recipes listed. Removed the draft's closing paragraph on order of work and createResolver reuse (not stated on the page) and the Verify step.

Method: documentation only; no commands were run.
