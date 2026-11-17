---
id: computing-software.web-development.vue.event-handling-and-modifiers
name: event-handling-and-modifiers
category: computing-software
field: web-development
product: vue
tags: [event-modifiers, vue-events, v-on, key-modifiers, vue]
level: intro
status: verified
description: "Vue event handling: v-on and @ shorthand, inline vs method handlers, $event, event modifiers (.prevent, .stop, .once, .passive), key and mouse modifiers, and component events."
sources:
  - https://vuejs.org/guide/essentials/event-handling.html
  - https://vuejs.org/guide/components/events.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Event handling and modifiers

## 1. Handlers
```vue
<button @click="count++">Add</button>                 <!-- inline statement -->
<button @click="save">Save</button>                   <!-- method: receives the native event -->
<button @click="remove(item.id, $event)">Delete</button>
<input @input="(e) => query = e.target.value">
```

## 2. Event modifiers
| Modifier | Effect |
|---|---|
| `.prevent` | `event.preventDefault()` - `<form @submit.prevent="onSubmit">` |
| `.stop` | `stopPropagation()` |
| `.self` | only when `event.target` is the element itself (backdrop clicks) |
| `.once` | handler runs once |
| `.capture` | listen in capture phase |
| `.passive` | passive listener for scroll/touch performance; don't combine with `.prevent` |

Modifiers chain in order: `@click.prevent.self` prevents all clicks; `@click.self.prevent` only clicks on the element itself.

## 3. Key and mouse modifiers
```vue
<input @keyup.enter="submit" @keydown.esc="cancel">
<textarea @keydown.ctrl.enter="send" @keydown.meta.enter="send"></textarea>
<div @click.right.prevent="openMenu"></div>
<button @click.exact="select" @click.shift.exact="extendSelection"></button>
```
- Key aliases: `.enter .tab .delete .esc .space .up .down .left .right`, or any `KeyboardEvent.key` in kebab-case (`.page-down`).
- System modifiers `.ctrl .alt .shift .meta`; `.exact` requires exactly those modifiers.
- For accessibility, interactive things should be `<button>`s: they get Enter/Space activation for free. Don't add `@click` to `<div>`s and then key handlers to compensate.

## 4. Component events
```vue
<script setup>
const emit = defineEmits<{ (e: "update", value: string): void; (e: "close"): void }>();
</script>
<template><button @click="emit('close')">Close</button></template>
<!-- parent -->
<Dialog @close="open = false" @update="onUpdate" />
```
- Declare events with `defineEmits` (typed, documented, and excluded from fallthrough attrs).
- Component events don't bubble; use provide/inject or a store for deep communication.
- Native listeners on a component's root work via fallthrough attributes unless declared as emits.

## Verify
- [ ] Forms use `@submit.prevent`; scroll/touch listeners passive; all component events declared in defineEmits; no click handlers on non-interactive elements.
