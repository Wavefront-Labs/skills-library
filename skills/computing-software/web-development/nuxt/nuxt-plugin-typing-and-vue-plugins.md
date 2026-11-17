---
id: computing-software.web-development.nuxt.nuxt-plugin-typing-and-vue-plugins
name: nuxt-plugin-typing-and-vue-plugins
category: computing-software
field: web-development
product: nuxt
tags: [nuxt, plugins, vue-plugin, typescript, provide]
level: advanced
status: docs-checked
description: "Type helpers provided by Nuxt plugins, avoid ref-unwrapping surprises, and register third-party Vue plugins via a Nuxt plugin."
sources:
  - https://github.com/nuxt/nuxt/blob/main/docs/2.directory-structure/1.app/1.plugins.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Typing: if you return your helpers from the plugin (under `provide`), they are typed automatically; you find them typed on the return of `useNuxtApp()` and within templates. To use a provided helper inside another plugin, call `useNuxtApp()` for the typed version, but the docs say this should generally be avoided unless you are certain of the plugins' order.

For advanced cases, declare the injected property types yourself:

```ts
declare module '#app' {
  interface NuxtApp { $hello (msg: string): string }
}
declare module 'vue' {
  interface ComponentCustomProperties { $hello (msg: string): string }
}
export {}
```

The docs highly recommend composables instead of providing helpers, to avoid polluting the global namespace and keep the main bundle entry small.

Warning: if your plugin provides a `ref` or `computed`, it is not unwrapped in a component `<template>`. The docs attribute this to how Vue works with refs that are not top-level to the template and point to the Vue documentation caveat on unwrapping in templates.

Vue plugins: to use a Vue plugin such as `vue-gtag-next` (Google Analytics tags), install the dependency, then create a Nuxt plugin file, for example `app/plugins/vue-gtag.client.ts`, that calls `nuxtApp.vueApp.use(VueGtag, { property: { id: 'GA_MEASUREMENT_ID' } })` and `trackRouter(useRouter())`.

Vue directives: register with `nuxtApp.vueApp.directive('focus', { mounted (el) { el.focus() }, getSSRProps (binding, vnode) { return {} } })`. A directive must be registered on both client and server unless you only use it when rendering one side. If it only makes sense on the client, put it in `~/plugins/my-directive.client.ts` and provide a stub directive for the server in `~/plugins/my-directive.server.ts`.

## Checked

2026-11-04. Confirmed against the Nuxt plugins directory page, sections "Typing Plugins", "Providing Helpers", "Vue Plugins" and "Vue Directives". Removed the draft's advice to access `.value` or expose the ref through a composable (not on the page) and the Verify step. Added the Vue directives section.

Method: documentation only; no commands were run.
