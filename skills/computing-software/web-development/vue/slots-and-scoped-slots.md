---
id: computing-software.web-development.vue.slots-and-scoped-slots
name: slots-and-scoped-slots
category: computing-software
field: web-development
product: vue
tags: [vue-components, vue-slots, scoped-slots, named-slots, slot-props, renderless-components, v-slot]
level: practitioner
status: verified
description: "Composing Vue components with default, named and scoped slots: v-slot shorthand, slot props, fallback content, conditional slots and renderless patterns."
sources:
  - https://vuejs.org/guide/components/slots.html
  - https://vuejs.org/api/sfc-script-setup.html#useslots-useattrs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Slots and scoped slots

**Goal:** components that let parents supply markup in defined places, including markup that uses the child's data.

## 1. Default and named slots
```vue
<!-- Card.vue -->
<template>
  <article class="card">
    <header v-if="$slots.header"><slot name="header" /></header>
    <slot>Nothing here yet.</slot>                    <!-- fallback content -->
    <footer v-if="$slots.footer"><slot name="footer" /></footer>
  </article>
</template>

<!-- Parent -->
<Card>
  <template #header><h2>Orders</h2></template>
  <OrderList />
  <template #footer><Pager /></template>
</Card>
```
`$slots.name` (or `useSlots()` in `<script setup>`) checks whether a slot was provided - wrap optional regions so empty wrappers don't render.

## 2. Scoped slots: child passes data up to the slot
```vue
<!-- DataTable.vue -->
<tr v-for="row in rows" :key="row.id">
  <td v-for="col in columns" :key="col.key">
    <slot :name="`cell-${col.key}`" :row="row" :value="row[col.key]">{{ row[col.key] }}</slot>
  </td>
</tr>

<!-- Parent -->
<DataTable :rows="orders" :columns="cols">
  <template #cell-status="{ value }"><StatusBadge :status="value" /></template>
  <template #cell-total="{ row }">{{ formatMoney(row.total, row.currency) }}</template>
</DataTable>
```
Dynamic slot names (`#[name]`) and destructuring with defaults (`#item="{ item, index = 0 }"`) work.

## 3. Renderless components
A component that only provides logic via its default scoped slot (`<MouseTracker v-slot="{ x, y }">`). In Vue 3 prefer a composable (`useMouse()`) unless you need the template-scoped API.

## 4. TypeScript
`defineSlots<{ default(props: { item: Item }): any; header(): any }>()` types slot props for consumers (Volar/vue-tsc checks usage).

## 5. Gotchas
- Slot content is compiled in the **parent's** scope - it can't see child data except via slot props.
- Mixing `v-slot` on the component with named `<template #x>` children is an error; use `<template #default>` explicitly.

## Verify
- [ ] Optional slots don't leave empty wrappers.
- [ ] vue-tsc catches wrong slot prop usage.
- [ ] Fallback content shows when a slot isn't provided.
