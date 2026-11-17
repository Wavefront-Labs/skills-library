---
id: computing-software.web-development.vue.async-components-and-lazy-loading
name: async-components-and-lazy-loading
category: computing-software
field: web-development
product: vue
tags: [vue-components, defineasynccomponent, async-components, lazy-loading-components, code-splitting, vue-suspense, lazy-hydration]
level: practitioner
status: verified
description: "Lazy-loading Vue components with defineAsyncComponent: loading/error components, delay and timeout, Suspense interplay and lazy hydration strategies in Vue 3.5."
sources:
  - https://vuejs.org/guide/components/async.html
  - https://vuejs.org/guide/built-ins/suspense.html
  - https://vuejs.org/guide/components/async.html#lazy-hydration
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Async components and lazy loading

**Goal:** heavy components (editors, charts, maps, modals) download only when needed, with sensible loading/error states.

## 1. Basic
```ts
import { defineAsyncComponent } from 'vue';
const RichEditor = defineAsyncComponent(() => import('./RichEditor.vue'));
```
Use it like any component; the chunk loads on first render. Combine with `v-if` so it renders (and loads) only when opened.

## 2. Options
```ts
const Chart = defineAsyncComponent({
  loader: () => import('./Chart.vue'),
  loadingComponent: ChartSkeleton,
  delay: 200,                 // show loading only if it takes longer (avoid flicker)
  errorComponent: LoadError,
  timeout: 10000,
  onError(error, retry, fail, attempts) { attempts <= 2 ? retry() : fail(); },
});
```

## 3. Suspense
An async component inside `<Suspense>` defers to the Suspense boundary's fallback (its own loading/error options are ignored) unless created with `suspensible: false`. Components with async `setup()` (top-level `await` in `<script setup>`) **require** a Suspense ancestor.

## 4. Lazy hydration (Vue 3.5+, SSR)
```ts
import { defineAsyncComponent, hydrateOnVisible, hydrateOnIdle, hydrateOnInteraction } from 'vue';
const Comments = defineAsyncComponent({ loader: () => import('./Comments.vue'), hydrate: hydrateOnVisible({ rootMargin: '200px' }) });
```
Server-rendered HTML shows immediately; JS loads/hydrates when visible, idle or interacted with (`hydrateOnInteraction('click')`). Nuxt: `<LazyComments hydrate-on-visible />`.

## 5. Routes
Vue Router route components as `() => import('./views/Settings.vue')` are lazy automatically (no `defineAsyncComponent` needed).

## Verify
- [ ] Network: chunk loads only when the component first renders.
- [ ] Simulated chunk failure shows the error component and retries.
- [ ] SSR pages with lazy hydration: content visible before JS, interactive after trigger.
