---
id: computing-software.web-development.nuxt.nuxt-usestate-shared-ssr-state
name: nuxt-usestate-shared-ssr-state
category: computing-software
field: web-development
product: nuxt
tags: [nuxt, usestate, state-management, ssr, hydration]
level: practitioner
status: docs-checked
description: "Use useState for SSR-friendly shared state, avoid module-level refs that leak across requests, and wrap state in composables."
sources:
  - https://github.com/nuxt/nuxt/blob/main/docs/1.getting-started/11.state-management.md
  - https://github.com/nuxt/nuxt/blob/main/docs/4.api/2.composables/use-state.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`useState(key, init)` is an SSR-friendly replacement for `ref`. Its value is preserved after server-side rendering (during client-side hydration) and shared across all components using the same unique key. If you omit the key, one unique to the file and line number of the call is generated. `init` provides the initial value and may also return a `Ref`.

```vue
<script setup lang="ts">
const counter = useState('counter', () => Math.round(Math.random() * 1000))
</script>
```

Rules from the pages:
- State is serialised to JSON, so it must not contain classes, functions or symbols. The error `Cannot stringify arbitrary non-POJOs` means a non-serialisable payload such as a class instance; for classes Nuxt does not support, `definePayloadPlugin` can add a custom serializer and deserializer.
- Never define `const state = ref()` (or `export myState = ref({})`) outside `<script setup>` or `setup()`: on the server the state would be shared across requests and can lead to memory leaks. Instead use `const useX = () => useState('x')`.
- `useState` is a reserved function name transformed by the compiler; do not name your own function `useState`.
- To globally invalidate cached state, see the `clearNuxtState` util.
- If state need not be deeply reactive, combine with `shallowRef`: `useState('my-shallow-state', () => shallowRef({ deep: 'not reactive' }))`.

A composable wrapper keeps keys in one place, for example `export const useColor = () => useState<string>('color', () => 'pink')`, auto-imported from `composables/`.

Async initialisation: use `callOnce` in `app/app.vue`:

```ts
const websiteConfig = useState('config')
await callOnce(async () => {
  websiteConfig.value = await $fetch('https://my-cms.com/api/website-config')
})
```

The page says this is similar to Nuxt 2's `nuxtServerInit`, filling initial state server-side before rendering. For a Pinia store (module installed with `npx nuxt module add pinia`), the page uses `await callOnce(website.fetch)`. Nuxt is not opinionated about state management; the page lists Pinia, Harlem and XState integrations.

## Checked

2026-11-08. Read in full from the nuxt/nuxt docs repository: docs/1.getting-started/11.state-management.md and docs/4.api/2.composables/use-state.md. Confirmed: all rules and examples above. Changed: the leak warning now says what the page says (memory leaks), not "user data"; removed the unsupported explanation that callOnce avoids refetch on hydration, and the invented Verify step (view source).

Method: documentation only; no commands were run.
