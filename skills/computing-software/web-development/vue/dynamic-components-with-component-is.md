---
id: computing-software.web-development.vue.dynamic-components-with-component-is
name: dynamic-components-with-component-is
category: computing-software
field: web-development
product: vue
tags: [dynamic-components, component-is, keepalive, vue-components, vue]
level: practitioner
status: verified
description: "Rendering components dynamically in Vue with component :is: passing definitions vs names, KeepAlive for preserving state, shallowRef for component maps, and async components."
sources:
  - https://vuejs.org/guide/essentials/component-basics.html#dynamic-components
  - https://vuejs.org/guide/built-ins/keep-alive.html
  - https://vuejs.org/api/built-in-special-elements.html#component
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dynamic components with component :is

## 1. Basics
```vue
<script setup>
import { shallowRef } from "vue";
import TabProfile from "./TabProfile.vue"; import TabBilling from "./TabBilling.vue";
const tabs = { profile: TabProfile, billing: TabBilling };
const current = shallowRef("profile");
</script>
<template>
  <button v-for="(_, key) in tabs" :key="key" @click="current = key">{{ key }}</button>
  <component :is="tabs[current]" :user="user" @saved="onSaved" />
</template>
```
- `:is` accepts an imported component definition (preferred in `<script setup>`), a registered component name string, or a native tag name (`:is="level === 1 ? 'h1' : 'h2'"`).
- Store component definitions in plain objects or `shallowRef`/`markRaw` - making a component object deeply reactive triggers a warning and wastes memory.

## 2. Preserving state with KeepAlive
```vue
<KeepAlive :include="['TabProfile']" :max="5">
  <component :is="tabs[current]" />
</KeepAlive>
```
- Without KeepAlive, switching unmounts and loses component state.
- `include`/`exclude` match the component `name` (auto-inferred from filename for SFCs in `<script setup>`, or set with `defineOptions`).
- Cached components get `onActivated`/`onDeactivated` hooks instead of mount/unmount: pause polling there.
- `:max` evicts least recently used instances.

## 3. Async components
```ts
const tabs = { reports: defineAsyncComponent(() => import("./TabReports.vue")) };
```
Combine with `<Suspense>` or the `loadingComponent`/`errorComponent` options.

## 4. Use cases and alternatives
- Tabs, wizards, CMS-driven page blocks (map block type -> component), polymorphic "as" props (`<component :is="as ?? 'button'">`).
- For routing, use Vue Router's `<RouterView v-slot="{ Component }"><KeepAlive><component :is="Component" /></KeepAlive></RouterView>`.
- Unknown CMS block types: fall back to a placeholder component rather than rendering nothing silently.

## Verify
- [ ] No "made a component reactive" warnings; cached tabs keep state and stop background work on deactivate; unknown dynamic types handled.
