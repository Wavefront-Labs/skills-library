---
id: computing-software.web-development.vue.render-functions-and-jsx
name: render-functions-and-jsx
category: computing-software
field: web-development
product: vue
tags: [render-functions, vue-jsx, h-function, functional-components, vnode, vue]
level: advanced
status: gated
description: "Vue render functions and JSX: h() signature, props/events/slots, v-model and directive equivalents, functional components, and when templates are better."
sources:
  - https://vuejs.org/guide/extras/render-function.html
  - https://github.com/vuejs/babel-plugin-jsx
  - https://vuejs.org/api/render-function.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Render functions and JSX

Templates are compiled to render functions and get compiler optimisations (static hoisting, patch flags). Write render functions only when you need full JS power: dynamic tags, generic library components, programmatic slot manipulation.

## 1. h()
```ts
import { h, defineComponent } from "vue";
export const Heading = defineComponent({
  props: { level: { type: Number, default: 2 } },
  setup(props, { slots }) {
    return () => h(`h${props.level}`, { class: "heading" }, slots.default?.());
  },
});
```
`h(type, props?, children?)`: type is a tag string or component; props include attrs, `class`, `style`, DOM props and listeners as `onXxx`.

## 2. Equivalents of template features
| Template | Render function |
|---|---|
| `v-if` / `v-for` | JS `cond ? h(A) : null`, `items.map(i => h(Row, { key: i.id, item: i }))` |
| `@click="f"` | `{ onClick: f }` (modifiers: `withModifiers(f, ["stop", "prevent"])`) |
| `v-model="x"` | `{ modelValue: x.value, "onUpdate:modelValue": v => (x.value = v) }` |
| slots to a child | `h(Child, null, { default: () => "text", header: (p) => h("b", p.title) })` |
| custom directive | `withDirectives(h("input"), [[vFocus]])` |
| component by name | `resolveComponent("RouterLink")` |

## 3. JSX
```bash
npm i -D @vitejs/plugin-vue-jsx
```
```tsx
export default defineComponent({
  setup(_, { slots }) {
    const count = ref(0);
    return () => <button onClick={() => count.value++}>{slots.default?.()} {count.value}</button>;
  },
});
```
Vue JSX uses `class`, `onClick` and `v-model` support via the plugin (`@vue/babel-plugin-jsx` README), and slots as objects. Whether `className` is also accepted is unconfirmed (gated: unconfirmed, source is paywalled or blocked).

## 4. Functional components
```ts
const Badge = (props: { tone: string }, { slots }) => h("span", { class: `badge badge-${props.tone}` }, slots.default?.());
Badge.props = ["tone"];
```
Stateless, no instance; in Vue 3 the performance difference from stateful components is negligible, so use them for simplicity, not speed.

## Gotchas
- Return a **function** from `setup` (render), not a VNode, or it will not update.
- Re-creating child VNodes each render is fine; re-creating components (new definitions per render) remounts them.

## Verify
- [ ] Component renders identically to its template version; reactivity updates the output; events and slots work.
