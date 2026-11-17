---
id: computing-software.web-development.nuxt.nuxt-definepagemeta-macro-rules
name: nuxt-definepagemeta-macro-rules
category: computing-software
field: web-development
product: nuxt
tags: [nuxt, definepagemeta, page-meta, keepalive, typescript]
level: advanced
status: docs-checked
description: "Use definePageMeta correctly: compiler-macro limits, special keys (layout, middleware, keepalive, alias, path), and typing custom meta."
sources:
  - https://github.com/nuxt/nuxt/blob/main/docs/2.directory-structure/1.app/1.pages.md
  - https://github.com/nuxt/nuxt/blob/main/docs/4.api/3.utils/define-page-meta.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`definePageMeta` sets metadata for page components and works in `<script>` and `<script setup>`. The data is available throughout the app from the `route.meta` object. With nested routes, the page metadata from all these routes is merged into a single object.

It is a compiler macro, like `defineEmits` or `defineProps`: it is compiled away and the metadata passed to it is hoisted out of the component, so the page meta object cannot reference the component. It can reference imported bindings and locally defined pure functions. Do not reference reactive data or functions that cause side effects:

```vue
import { someData } from '~/utils/example'
function validateIdParam (route) {
  return route.params.id && !Number.isNaN(Number(route.params.id))
}
const title = ref('')
definePageMeta({ validate: validateIdParam, someData, title /* do not: ref is hoisted out */ })
```

Keys with a particular purpose:
- `name`: the route name (by default generated from the path inside the pages directory).
- `path`: a custom pattern, for example `definePageMeta({ path: '/:postId(\\d+)-:postSlug' })` in `[postId]-[postSlug].vue` so only digits match `postId` and `/test-category` goes to `[categorySlug].vue`.
- `alias`: a string or array of strings; all `alias` and `path` values must share the same params.
- `props`: access route `params` as props of the page component.
- `redirect`: happens before any navigation guard and triggers a new navigation.
- `keepalive`: `true` or `KeepAliveProps` to preserve page state across route changes. To preserve state for parent routes use `<NuxtPage keepalive />`.
- `key`: a string, `false` or a function of the route, for control over when `<NuxtPage>` re-renders.
- `layout`: `false` (disable any layout), a layout name, a ref/computed, or `{ name, props }` to pass typed props.
- `layoutTransition` / `pageTransition`: `TransitionProps` or `false` to disable the transition wrapper for that route.
- `middleware`: a string, a function or an array of them; merged with other middleware of matching parent/child routes.
- `validate`: return `true` if the route is valid; if no other match is found this means a 404. Can return an object with `status`/`statusText` to respond with an error immediately.
- `scrollToTop`: boolean or function; set `false` to disable scrolling to top.
- `viewTransition`: experimental, only when enabled in `nuxt.config`.
- `groups`: automatically populated for pages in route groups.

Type custom keys by augmenting `PageMeta` from `#app` in a `.d.ts` file; always import or export something when augmenting a type:

```ts
declare module '#app' { interface PageMeta { pageType?: string } }
export {}
```

## Checked

2026-11-04. Confirmed against the Nuxt pages directory page and the definePageMeta API page: macro behaviour and its hoisting warning, merged nested meta, each listed key and its type, the custom path regex example, keepalive syntax, PageMeta augmentation. Corrected the path regex backslash (the page writes it as \\d in a JS string). Removed the Verify step.

Method: documentation only; no commands were run.
