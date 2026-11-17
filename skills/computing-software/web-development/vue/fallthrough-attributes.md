---
id: computing-software.web-development.vue.fallthrough-attributes
name: fallthrough-attributes
category: computing-software
field: web-development
product: vue
tags: [vue-components, fallthrough-attributes, attrs, inheritattrs, v-bind-attrs, multi-root-components, wrapper-components]
level: practitioner
status: verified
description: "Controlling Vue fallthrough attributes: automatic class/style/listener inheritance, inheritAttrs false with v-bind='$attrs' for wrappers, multi-root components and useAttrs."
sources:
  - https://vuejs.org/guide/components/attrs.html
  - https://vuejs.org/api/sfc-script-setup.html#useslots-useattrs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fallthrough attributes

**Goal:** wrapper components pass `class`, `aria-*`, `data-*` and listeners to the right inner element.

## 1. Default behaviour
Attributes and `v-on` listeners passed to a component that are **not** declared as props or emits fall through to its single root element. `class` and `style` merge with the root's own.
```vue
<MyButton class="wide" aria-label="Close" @click="close" />   <!-- lands on MyButton's root <button> -->
```
Declaring an event in `defineEmits` stops the native listener from falling through (the component now owns it).

## 2. Wrapper components: target an inner element
```vue
<!-- TextField.vue -->
<script setup>
defineOptions({ inheritAttrs: false });
const props = defineProps({ label: String });
const model = defineModel();
</script>
<template>
  <div class="field">
    <label :for="id">{{ label }}</label>
    <input :id="id" v-model="model" v-bind="$attrs" />     <!-- placeholder, required, autocomplete, aria-* go to the input -->
  </div>
</template>
```
With `inheritAttrs: false`, `class`/`style` also go wherever you bind `$attrs` - split them if the wrapper should keep the class:
```ts
const attrs = useAttrs();
const rootAttrs = computed(() => ({ class: attrs.class, style: attrs.style }));
const inputAttrs = computed(() => { const { class: _, style: __, ...rest } = attrs; return rest; });
```

## 3. Multi-root components
Fragments (multiple root nodes) have no automatic fallthrough; Vue warns "Extraneous non-props attributes" unless you bind `$attrs` explicitly to one root.

## 4. Notes
- `$attrs` isn't reactive for watching (`useAttrs()` returns the latest value each render, but `watch(attrs)` doesn't trigger) - use `onUpdated` or props if you must react.
- Listeners appear in `$attrs` as `onClick` etc.
- TypeScript: attrs are untyped; for typed passthrough of native input attributes declare the important ones as props.

## Verify
- [ ] `aria-describedby`, `required`, `autocomplete` passed to TextField end up on the `<input>` (inspect DOM).
- [ ] No "Extraneous non-props attributes" warnings.
- [ ] Classes from the parent apply where intended.
