---
id: computing-software.web-development.vue.lifecycle-hooks-and-template-refs
name: lifecycle-hooks-and-template-refs
category: computing-software
field: web-development
product: vue
tags: [vue, vue-lifecycle-hooks, template-refs, onmounted, usetemplateref, nexttick, composition-api, web-development]
level: practitioner
status: verified
description: "Using Vue 3 lifecycle hooks and template refs: onMounted/onUnmounted cleanup, useTemplateRef, refs in v-for, component refs with defineExpose and nextTick."
sources:
  - https://vuejs.org/guide/essentials/lifecycle.html
  - https://vuejs.org/guide/essentials/template-refs.html
  - https://vuejs.org/api/composition-api-lifecycle.html
  - https://vuejs.org/api/sfc-script-setup.html#defineexpose
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lifecycle hooks and template refs

**Goal:** touch the DOM and external resources at the right time and always clean up.

## 1. The hooks you use
```vue
<script setup>
import { onMounted, onBeforeUnmount, onUnmounted, onUpdated } from "vue";
let chart;
onMounted(() => { chart = new Chart(canvas.value, config); });   // DOM exists
onBeforeUnmount(() => chart?.destroy());                         // before DOM is removed
</script>
```
- `setup` / `<script setup>` body = "created": no DOM yet, runs on server too.
- `onBeforeMount`, `onMounted`, `onBeforeUpdate`, `onUpdated`, `onBeforeUnmount`, `onUnmounted`, `onActivated` and `onDeactivated` don't run during SSR. Browser-only code goes there.
- Register hooks **synchronously** in setup (Vue docs: "must be registered synchronously during component setup"). In a plain `async setup()` a hook after an `await` is not attached (Vue warns "no active component instance"); `<script setup>` top-level `await` is the exception, because the compiler restores the instance context, so hooks after it still attach (tested on 3.5.44).
- `onErrorCaptured` for subtree error handling; `onActivated`/`onDeactivated` inside `<KeepAlive>`.

## 2. Template refs
Vue 3.5+:
```vue
<script setup>
import { useTemplateRef, onMounted } from "vue";
const input = useTemplateRef("search");
onMounted(() => input.value?.focus());
</script>
<template><input ref="search" /></template>
```
Before 3.5: `const search = ref(null)` with a matching `ref="search"`. The ref is `null` until mounted and when a `v-if` removes the element.

## 3. Refs in v-for
`ref="items"` inside `v-for` gives an array (order not guaranteed to match source). Function refs give control:
```vue
<li v-for="i in list" :key="i.id" :ref="(el) => el ? map.set(i.id, el) : map.delete(i.id)">
```

## 4. Component refs
A ref on a `<script setup>` child is closed by default. Expose a narrow API:
```vue
<!-- Child -->
<script setup>
const open = () => { visible.value = true; };
defineExpose({ open });
</script>
```
Prefer props/events; use exposed methods for imperative actions (focus, open, scrollTo).

## 5. Timing after state changes
DOM updates are batched asynchronously. To measure after a change:
```js
items.value.push(x);
await nextTick();
listEl.value.lastElementChild.scrollIntoView();
```

## 6. Cleanup checklist
Event listeners on window/document, intervals, observers (Resize/Intersection), third-party widget instances, subscriptions. In composables, `onScopeDispose` covers both components and effect scopes.

## Verify
- [ ] Navigating away and back doesn't duplicate listeners or widget instances.
- [ ] SSR build doesn't touch `window` outside mounted hooks.
- [ ] Refs are null-checked where a `v-if` can remove the element.
