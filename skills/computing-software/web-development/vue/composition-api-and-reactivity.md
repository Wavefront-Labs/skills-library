---
id: computing-software.web-development.vue.composition-api-and-reactivity
name: composition-api-and-reactivity
category: computing-software
field: web-development
product: vue
tags: [vue, vue3, composition-api, script-setup, reactivity, ref, reactive, torefs, toref, computed, watch, watcheffect, defineprops, defineemits, definemodel, v-model, pinia, storetorefs, v-for, key, nexttick, composables, shallowref, single-file-components, sfc, options-api, nuxt, web-development, ref-vs-reactive, vue-computed, vue-reactivity]
level: practitioner
status: verified
description: "Vue 3 Composition API: script setup, ref vs reactive, toRefs and lost reactivity, computed vs watch vs watchEffect, props/emits, Pinia stores, v-for keys, nextTick."
sources:
  - https://vuejs.org/guide/introduction.html
  - https://vuejs.org/guide/essentials/reactivity-fundamentals.html
  - https://pinia.vuejs.org/
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Vue Composition API and reactivity — keep the proxy, derive don't copy

**Goal:** write `<script setup>` components and composables where reactivity never
silently breaks, derived state uses `computed`, and side effects are explicit.

## 1. The baseline component
```vue
<script setup lang="ts">
import { ref, computed, watch } from 'vue';
const props = defineProps<{ items: Item[]; max?: number }>();
const emit = defineEmits<{ select: [id: string] }>();
const query = ref('');
const filtered = computed(() =>
  props.items.filter(i => i.name.includes(query.value)).slice(0, props.max ?? 10));
</script>
<template>
  <input v-model="query" />
  <li v-for="item in filtered" :key="item.id" @click="emit('select', item.id)">{{ item.name }}</li>
</template>
```
Everything declared at top level is available in the template; refs auto-unwrap there
(no `.value`).

## 2. ref vs reactive
| | `ref()` | `reactive()` |
|---|---|---|
| Holds | any value, incl. primitives | objects/arrays/Map/Set only |
| Access in script | `.value` | direct |
| Can reassign whole value | yes (`x.value = {...}`) | no — replacing the variable loses reactivity |
| Destructure safely | n/a | no |

Default to `ref` everywhere — the official docs recommend it as the primary API. Use
`shallowRef` for large immutable data (API responses, chart data) you replace wholesale; it
avoids deep proxying.

## 3. Where reactivity is lost
```ts
const state = reactive({ count: 0, name: 'a' });
let { count } = state;            // plain number now — never updates
const { count: c } = toRefs(state); // c is a ref linked to state.count  ✔

const store = useCartStore();
const { total } = store;                   // ✘ loses reactivity
const { total, items } = storeToRefs(store); // ✔ (actions destructure directly)
```
Props: in Vue 3.5+ destructuring `defineProps()` in `<script setup>` stays reactive (the
compiler rewrites access), but passing a destructured prop into `watch` or a composable
still needs a getter: `watch(() => count, ...)`. In older 3.x, destructuring props breaks
reactivity — use `toRefs(props)` or `props.x`.

## 4. computed vs watch vs watchEffect
- **`computed`** — derived values. Cached, lazy, must be side-effect free. If you're writing
  `watch(a, v => b.value = f(v))`, it should be `const b = computed(() => f(a.value))`.
- **`watch(source, cb)`** — side effects on specific sources; gives old and new values; lazy
  unless `{ immediate: true }`. Watching a `reactive` object is deep by default; watching a
  getter is not (add `{ deep: true }` or a depth number in 3.5+).
- **`watchEffect(fn)`** — runs immediately and tracks whatever it reads synchronously.
  Dependencies read after an `await` are not tracked — a common bug.

Use `onWatcherCleanup` (3.5+) or the `onCleanup` argument to cancel stale requests:
```ts
watch(id, async (newId, _old, onCleanup) => {
  const ctrl = new AbortController();
  onCleanup(() => ctrl.abort());
  data.value = await fetch(`/api/items/${newId}`, { signal: ctrl.signal }).then(r => r.json());
});
```

## 5. Props, emits and v-model
Props are read-only: never mutate `props.x` (or an object inside it). Emit an event, or
use `defineModel()` (3.4+) for two-way binding: `const model = defineModel<string>()` and the
parent writes `<MyInput v-model="name" />`.

## 6. Pinia
```ts
export const useCartStore = defineStore('cart', () => {
  const items = ref<Item[]>([]);
  const total = computed(() => items.value.reduce((s, i) => s + i.price, 0));
  function add(item: Item) { items.value.push(item); }
  return { items, total, add };
});
```
Setup stores must return every piece of state, or devtools and SSR hydration miss it. In
SSR (Nuxt), never create stores or module-level `ref`s outside a request — state leaks
between users.

## 7. Lists and DOM timing
- `v-for` always gets `:key` with a stable id (not the index when items reorder or are removed).
- Don't put `v-if` and `v-for` on the same element; in Vue 3 `v-if` wins and can't see the loop variable. Filter with a `computed`.
- DOM updates are batched per tick. To measure or focus after a state change: `await nextTick()`.
- Template refs: `useTemplateRef('el')` in 3.5+, or a same-named `ref(null)` in older versions.

## Verify
- [ ] No destructuring of `reactive` objects or stores without `toRefs`/`storeToRefs`.
- [ ] Derived values use `computed`; no watcher just copies one ref into another.
- [ ] Watchers that fetch abort or ignore stale responses.
- [ ] No component mutates its props; two-way binding uses `defineModel` or emits.
- [ ] Every `v-for` has a stable `:key`; Vue Devtools shows the expected store state.
