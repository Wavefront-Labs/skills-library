---
id: computing-software.web-development.nuxt.nuxt-components-auto-import-naming
name: nuxt-components-auto-import-naming
category: computing-software
field: web-development
product: nuxt
tags: [nuxt, components, auto-import, pathprefix, naming]
level: intro
status: docs-checked
description: "How Nuxt names auto-imported components from folder paths, grouping directories with parentheses, and the pathPrefix option."
sources:
  - https://github.com/nuxt/nuxt/blob/main/docs/2.directory-structure/1.app/1.components.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Nuxt auto-imports any component in the components directory (along with components registered by modules). A component in nested directories is named from its own path directory and filename, with duplicate segments removed: `components/base/foo/Button.vue` becomes `<BaseFooButton />`. The docs recommend that the filename matches the name (rename to `BaseFooButton.vue`) for clarity.

To group components in a directory without affecting their name, name the grouping directory with parentheses: `components/base/(foo)/Button.vue` becomes `<BaseButton />`.

To auto-import components by name only, not path, set `pathPrefix` to `false` using the extended form:

```ts
export default defineNuxtConfig({
  components: [{ path: '~/components', pathPrefix: false }],
})
```

This registers components the way Nuxt 2 did: `~/components/Some/MyComponent.vue` is `<MyComponent>`, not `<SomeMyComponent>`.

Dynamic components: for `<component :is="...">` use Vue's `resolveComponent('MyButton')` or import the component from `#components` and pass it to `is`. The `resolveComponent` argument must be a literal string, not a variable or containing one, because it is statically analysed at the compilation step.

Global registration (`components: { global: true, dirs: ['~/components'] }`) is not recommended; it creates async chunks for all components. You can register selected components globally by placing them in `~/components/global` or by using a `.global.vue` filename suffix; each global component is rendered in a separate chunk, so do not overuse it. The `global` option can also be set per component directory.

Direct imports from `#components` bypass Nuxt's auto-importing: `import { LazyMountainsList, NuxtLink } from '#components'`.

## Checked

2026-11-04. Confirmed against the Nuxt components directory page: naming rule with duplicate-segment removal, filename recommendation, parenthesis grouping, pathPrefix false and Nuxt 2 comparison, resolveComponent literal-string rule, #components, global options, direct imports. Corrected the parenthesis example (the page uses base/(foo)/Button.vue giving BaseButton). Removed the Verify step.

Method: documentation only; no commands were run.
