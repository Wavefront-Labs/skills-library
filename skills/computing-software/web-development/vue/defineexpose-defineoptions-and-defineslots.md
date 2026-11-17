---
id: computing-software.web-development.vue.defineexpose-defineoptions-and-defineslots
name: defineexpose-defineoptions-and-defineslots
category: computing-software
field: web-development
product: vue
tags: [defineexpose, defineoptions, defineslots, definemodel, script-setup, vue]
level: practitioner
status: verified
description: "Script setup macros beyond props and emits: defineExpose for template refs, defineOptions, defineSlots for typed slots, and defineModel for v-model."
sources:
  - https://vuejs.org/api/sfc-script-setup.html
  - https://vuejs.org/guide/components/v-model.html
  - https://vuejs.org/guide/typescript/composition-api.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# defineExpose, defineOptions, defineSlots (and defineModel)

Macros are compile-time only: no import needed, can't be called conditionally, and must be at the top level of `<script setup>`.

## 1. defineExpose
`<script setup>` components are **closed** by default: a parent's template ref sees nothing. Expose a deliberate API:
```vue
<script setup lang="ts">
const input = ref<HTMLInputElement>();
function focus() { input.value?.focus(); }
function reset() { /* ... */ }
defineExpose({ focus, reset });
</script>
<!-- parent -->
<script setup lang="ts">
const field = useTemplateRef<InstanceType<typeof TextField>>("field");   // 3.5+
onMounted(() => field.value?.focus());
</script>
<TextField ref="field" />
```
Keep exposed surfaces small (imperative actions like focus/scroll/reset); prefer props/events for data.

## 2. defineOptions (3.3+)
```ts
defineOptions({ name: "DataTable", inheritAttrs: false });
```
Replaces a separate `<script>` block for component options. `inheritAttrs: false` + `v-bind="$attrs"` on the right inner element (e.g. the `<input>` inside a wrapper label).

## 3. defineSlots (3.3+)
```ts
const slots = defineSlots<{
  default(props: { item: Row; index: number }): any;
  empty(): any;
}>();
```
Gives the parent type-checked scoped slot props and IDE completion. Runtime: returns the same object as `useSlots()`.

## 4. defineModel (3.4+)
```vue
<script setup>
const model = defineModel<string>({ required: true });
const open = defineModel<boolean>("open", { default: false });   // v-model:open
</script>
<input v-model="model">
```
Replaces the `modelValue` prop + `update:modelValue` emit boilerplate. Modifiers via `const [model, modifiers] = defineModel({ set(v) { return modifiers.trim ? v.trim() : v; } })`.

## 5. Gotchas
- `defineProps`, `defineEmits` and `defineOptions` arguments are hoisted out of `setup`, so they can't reference local variables (imports and literal constants are fine); type-only declarations are fine.
- Top-level `await` is allowed in `<script setup>` (the component becomes an async setup and needs a `<Suspense>` ancestor); `defineExpose` placed after an `await` still exposes its values (tested on Vue 3.5.44).

## Verify
- [ ] Parent refs only use exposed methods; component name set where devtools/recursion needs it; slot props type-checked with vue-tsc.
