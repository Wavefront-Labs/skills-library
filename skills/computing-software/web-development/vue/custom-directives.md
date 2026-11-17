---
id: computing-software.web-development.vue.custom-directives
name: custom-directives
category: computing-software
field: web-development
product: vue
tags: [vue, custom-directives, directive-hooks, v-focus, v-click-outside, dom-access, web-development]
level: practitioner
status: verified
description: "Writing Vue 3 custom directives for low-level DOM behaviour: hook lifecycle, arguments and modifiers, cleanup via el state, SSR getSSRProps and when to use a component instead."
sources:
  - https://vuejs.org/guide/reusability/custom-directives.html
  - https://vuejs.org/api/application.html#app-directive
  - https://vuejs.org/guide/scaling-up/ssr.html#custom-directives
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom directives

**Goal:** reusable DOM-level behaviour (focus, click-outside, tooltips, lazy images) with correct lifecycle and cleanup.

## 1. When a directive is right
Only for direct DOM manipulation on a plain element. If it needs template/markup or state, write a component or composable. Directives on components apply to the root node and warn for multi-root components.

## 2. Local directive in `<script setup>`
```vue
<script setup>
const vFocus = { mounted: (el) => el.focus() };     // any camelCase var starting with v
</script>
<template><input v-focus /></template>
```
Global: `app.directive("focus", { mounted: (el) => el.focus() })`.

## 3. Hooks
`created`, `beforeMount`, `mounted`, `beforeUpdate`, `updated`, `beforeUnmount`, `unmounted`. Each gets `(el, binding, vnode, prevVnode)`; `binding` has `value`, `oldValue`, `arg`, `modifiers`, `instance`.

## 4. Click-outside with cleanup
```ts
import type { Directive } from "vue";
type El = HTMLElement & { __outside?: (e: Event) => void };
export const vClickOutside: Directive<El, (e: Event) => void> = {
  mounted(el, { value }) {
    el.__outside = (e) => { if (!el.contains(e.target as Node)) value(e); };
    document.addEventListener("pointerdown", el.__outside);
  },
  unmounted(el) { document.removeEventListener("pointerdown", el.__outside!); },
};
```
```vue
<div v-click-outside="close">...</div>
```
Store per-element state on the element (or a WeakMap); the directive object is shared by all usages.

## 5. Arguments and modifiers
`v-pin:[direction].smooth="200"` → `binding.arg === direction value`, `binding.modifiers.smooth === true`, `binding.value === 200`. Dynamic args in brackets.

## 6. Function shorthand
`app.directive("color", (el, binding) => { el.style.color = binding.value; })` runs on `mounted` and `updated`.

## 7. SSR
Directive hooks don't run on the server. Provide `getSSRProps(binding)` to return attributes to render (e.g. `{ id: binding.value }`) so server HTML matches.

## Verify
- [ ] Mounting/unmounting 100 times leaves listener count unchanged (DevTools `getEventListeners(document)`).
- [ ] Updates to the bound value are handled in `updated` where relevant.
- [ ] No directive is doing what a component/composable should.
