---
id: computing-software.web-development.vue.migrating-vue-2-to-vue-3
name: migrating-vue-2-to-vue-3
category: computing-software
field: web-development
product: vue
tags: [vue-2-migration, vue-compat-build, vue-3-upgrade, vue-router-4, pinia-migration, vue]
level: advanced
status: verified
description: "Migrating a Vue 2 app to Vue 3: assessing blockers, Vue 2.7 stepping stone, @vue/compat migration build, the main breaking changes, Router 4/Pinia, and moving to Vite."
sources:
  - https://v3-migration.vuejs.org/
  - https://v3-migration.vuejs.org/migration-build.html
  - https://v2.vuejs.org/lts/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migrating Vue 2 to Vue 3

Vue 2 reached end of life on 31 Dec 2023 (no security fixes without paid extended support). Options API still works in Vue 3: migration does not require rewriting components to the Composition API.

## 1. Assess blockers
- UI libraries without Vue 3 versions (BootstrapVue, Vuetify 2 -> 3 is a rewrite, Element UI -> Element Plus).
- Plugins relying on Vue 2 internals; IE11 support (Vue 3 dropped it).
- Build: Vue CLI/webpack 4 -> Vite (recommended) or webpack 5 with a Vue 3 compatible `vue-loader` (the migration build page says `^16.0.0` or later).

## 2. Stepping stones
- **Vue 2.7**: backports Composition API, `<script setup>`, `defineComponent`; start writing new code that runs on both.
- **Migration build** `@vue/compat`: Vue 3 with Vue 2 behaviours switchable per feature, logging deprecation warnings:
```js
// vite.config.js
resolve: { alias: { vue: "@vue/compat" } },
plugins: [vue({ template: { compilerOptions: { compatConfig: { MODE: 2 } } } })]
```
Fix warnings feature by feature, then switch to `MODE: 3` per component and remove the alias.

## 3. Breaking changes to fix
| Vue 2 | Vue 3 |
|---|---|
| `new Vue({ ... }).$mount` | `createApp(App).mount("#app")`, plugins via `app.use` |
| `Vue.prototype.$x` | `app.config.globalProperties.$x` |
| filters `{{ x | currency }}` | methods/computed |
| `v-model` uses `value`/`input` | `modelValue`/`update:modelValue`; `.sync` -> `v-model:prop` |
| `$listeners`, `$scopedSlots` | merged into `$attrs`, `$slots` |
| event bus `$on/$off/$once` | `mitt` or provide/inject/stores |
| `v-if` vs `v-for` priority | `v-if` now wins: never put both on one element |
| `.native` modifier, keyCode modifiers | removed; declare `emits` |
| transition classes `v-enter` | `v-enter-from`, `v-leave-from` |
| `Vue.set` / `Vue.delete` | not needed (Proxy reactivity) |

## 4. Ecosystem
- Vue Router 3 -> 4: `createRouter({ history: createWebHistory(), routes })`; catch-all `/:pathMatch(.*)*`; `router.push` returns a promise.
- Vuex 3 -> Vuex 4 (minimal change) or Pinia (recommended).
- Testing: Vue Test Utils 1 -> 2 (`mount` options changed: `props`, `global.plugins`).

## Verify
- [ ] Migration build shows zero compat warnings; `@vue/compat` removed; e2e suite passes on the final Vue 3 build.
