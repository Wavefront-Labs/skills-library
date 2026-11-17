---
id: computing-software.web-development.vue.create-vue-vite-and-vue-devtools
name: create-vue-vite-and-vue-devtools
category: computing-software
field: web-development
product: vue
tags: [create-vue, vue-devtools, vite, vue-tooling, vue-tsc]
level: intro
status: gated
description: "Vue tooling: scaffolding with create-vue, Vite config essentials, the Vue - Official extension and vue-tsc, Vue DevTools, and linting and formatting."
sources:
  - https://vuejs.org/guide/scaling-up/tooling.html
  - https://github.com/vuejs/create-vue
  - https://devtools.vuejs.org/
  - https://eslint.vuejs.org/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# create-vue, Vite and Vue DevTools

## 1. Scaffold
```bash
npm create vue@latest my-app      # or pass flags: --ts --jsx --router --pinia --vitest --cypress --playwright --eslint --prettier --oxfmt (see `npm create vue@latest -- --help`)
cd my-app && npm install && npm run dev
```
create-vue is the official Vite-based scaffolder (Vue CLI is in maintenance mode; migrate webpack-based Vue CLI apps to Vite). Nuxt has its own `npm create nuxt@latest`.

## 2. Vite essentials
```ts
// vite.config.ts
import { defineConfig } from "vite"; import vue from "@vitejs/plugin-vue"; import vueDevTools from "vite-plugin-vue-devtools";
import { fileURLToPath, URL } from "node:url";
export default defineConfig({
  plugins: [vue(), vueDevTools()],
  resolve: { alias: { "@": fileURLToPath(new URL("./src", import.meta.url)) } },
  server: { proxy: { "/api": "http://localhost:8000" } },     // avoid CORS in dev
});
```
Env vars: only `VITE_*` are exposed to client code via `import.meta.env`.

## 3. Editor and type checking
- VS Code: "Vue - Official" extension (Volar-based language tools); disable Vetur.
- Type-check in CI with `vue-tsc --build` (the scaffold's `type-check` script); Vite itself only transpiles.
- `tsconfig` from `@vue/tsconfig`.

## 4. Vue DevTools
- Browser extension, standalone Electron app, or the Vite plugin (`vite-plugin-vue-devtools`, included in the create-vue template) that embeds DevTools in the page. Supported browsers, "open in editor", the Pinia and router tabs and the timeline are documented at devtools.vuejs.org (gated: unconfirmed, source is paywalled or blocked).
- Inspect component props/state, edit values live, see emitted events, Pinia store state and time-travel.
- DevTools support is excluded from production builds by default: the compile-time flag `__VUE_PROD_DEVTOOLS__` defaults to `false` (esm-bundler build).

## 5. Lint and format
`eslint-plugin-vue` flat config (`pluginVue.configs["flat/recommended"]`) + `@vue/eslint-config-typescript`; Prettier for formatting (`skipFormatting` from `eslint-config-prettier/flat`, as in the create-vue template, to avoid rule conflicts). Rules worth enforcing: `vue/no-v-html`, `vue/require-v-for-key`, `vue/no-mutating-props`.

## Verify
- [ ] `npm run type-check`, `lint` and `test:unit` run in CI; DevTools shows component tree and Pinia stores in dev; no Vue CLI/webpack leftovers.
