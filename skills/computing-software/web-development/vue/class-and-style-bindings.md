---
id: computing-software.web-development.vue.class-and-style-bindings
name: class-and-style-bindings
category: computing-software
field: web-development
product: vue
tags: [class-style-bindings, vue-class-binding, vue-style-binding, css-variables, vue]
level: intro
status: verified
description: "Vue class and style bindings: object and array syntax, computed class objects, binding on components and $attrs, inline styles with auto-prefixing, and v-bind() in scoped CSS."
sources:
  - https://vuejs.org/guide/essentials/class-and-style.html
  - https://vuejs.org/api/sfc-css-features.html#v-bind-in-css
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Class and style bindings

## 1. Classes
```vue
<div class="card" :class="{ 'card--active': active, 'card--error': hasError }"></div>
<div :class="[sizeClass, { disabled }]"></div>
<div :class="classes"></div>
<script setup>
const classes = computed(() => ({ "btn": true, [`btn--${props.variant}`]: true, "btn--loading": props.loading }));
</script>
```
- Static `class` and bound `:class` merge.
- Move complex logic into a computed for readability and testability.
- With Tailwind, keep full class names in source (`'bg-red-500'`, not `` `bg-${color}-500` ``) so they are detected; map props to full strings.

## 2. On components
Classes on a component merge onto its **root element**. Multi-root components need explicit placement: `<div :class="$attrs.class">` (and `inheritAttrs: false` if needed).

## 3. Styles
```vue
<div :style="{ color: textColor, fontSize: size + 'px', '--progress': progress }"></div>
<div :style="[baseStyles, overrideStyles]"></div>
```
- camelCase or quoted kebab-case keys; Vue auto-prefixes when needed; array values provide fallbacks (`{ display: ['-webkit-box', 'flex'] }`).
- Prefer classes for static styling; inline style for truly dynamic values (positions, progress, user colours).

## 4. v-bind() in `<style>`
```vue
<script setup>const theme = ref({ accent: "#6366f1" });</script>
<style scoped>
.button { background: v-bind("theme.accent"); }
</style>
```
Compiles to a custom property set on the component root and updates reactively. Good for a few themeable values; for many tokens use global CSS variables.

## 5. Gotchas
- `:class="active ? 'on' : ''"` works but object syntax reads better.
- Vue does not add `px` to numbers in `:style` (React does): always include units.
- Scoped styles don't reach child component internals: use `:deep(.child-class)` deliberately.

## Verify
- [ ] Class logic lives in computed properties for complex cases; Tailwind classes are static strings; dynamic styles include units.
