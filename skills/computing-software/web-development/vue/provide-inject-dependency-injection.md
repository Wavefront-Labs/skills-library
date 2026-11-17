---
id: computing-software.web-development.vue.provide-inject-dependency-injection
name: provide-inject-dependency-injection
category: computing-software
field: web-development
product: vue
tags: [vue-components, provide-inject, dependency-injection, injection-key, prop-drilling, app-provide, reactive-provide]
level: practitioner
status: verified
description: "Sharing data down Vue component trees with provide/inject: typed InjectionKeys, keeping injected values reactive, readonly state with mutation functions, and app-level provides."
sources:
  - https://vuejs.org/guide/components/provide-inject.html
  - https://vuejs.org/api/composition-api-dependency-injection.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Provide / inject

**Goal:** pass context (theme, form state, a compound component's parent state) to deep descendants without prop drilling, while keeping it typed and reactive.

## 1. Typed keys
```ts
// keys.ts
import type { InjectionKey, Ref } from 'vue';
export interface TabsContext { active: Readonly<Ref<string>>; select: (id: string) => void }
export const TabsKey: InjectionKey<TabsContext> = Symbol('Tabs');
```
Symbols avoid name collisions; `InjectionKey<T>` makes `inject` return `T | undefined`.

## 2. Provide reactive state + mutation functions
```ts
// Tabs.vue <script setup>
const active = ref(props.defaultValue);
provide(TabsKey, { active: readonly(active), select: (id) => { active.value = id; } });
```
```ts
// Tab.vue <script setup>
const tabs = inject(TabsKey);
if (!tabs) throw new Error('<Tab> must be used inside <Tabs>');
const isActive = computed(() => tabs.active.value === props.id);
```
- Provide refs/reactive objects, not their `.value` - a plain value is a snapshot and won't update.
- Expose `readonly()` state plus functions so mutations happen in the provider (traceable).

## 3. Defaults
`inject(Key, defaultValue)` or a factory: `inject(Key, () => createDefault(), true)` (third arg = treat as factory).

## 4. App-level
`app.provide(Key, value)` for app-wide services (API client, config) - plugins use this. Available to every component; in composables, `inject` works only inside `setup` (or `app.runWithContext`).

## 5. When not to
Global app state shared by unrelated parts -> Pinia (devtools, SSR handling). Provide/inject is for subtree-scoped context and component libraries.

## Verify
- [ ] Changing provided state updates descendants.
- [ ] Using a child outside its provider throws a clear error.
- [ ] vue-tsc infers injected types without casts.
