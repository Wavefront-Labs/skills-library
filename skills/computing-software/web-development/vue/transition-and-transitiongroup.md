---
id: computing-software.web-development.vue.transition-and-transitiongroup
name: transition-and-transitiongroup
category: computing-software
field: web-development
product: vue
tags: [vue, vue-transition, transitiongroup, animations, enter-leave, move-transitions, prefers-reduced-motion, web-development]
level: practitioner
status: verified
description: "Animating with Vue Transition and TransitionGroup: class lifecycle, modes, appear, list move animations, JS hooks, route transitions and reduced motion."
sources:
  - https://vuejs.org/guide/built-ins/transition.html
  - https://vuejs.org/guide/built-ins/transition-group.html
  - https://router.vuejs.org/guide/advanced/transitions.html
  - https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Transition and TransitionGroup

**Goal:** smooth enter/leave/move animations that don't break layout or accessibility.

## 1. Transition basics
```vue
<Transition name="fade"><p v-if="show">Hello</p></Transition>
<style>
.fade-enter-active, .fade-leave-active { transition: opacity .2s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>
```
Classes: `*-enter-from`, `*-enter-active`, `*-enter-to`, `*-leave-from`, `*-leave-active`, `*-leave-to`. Triggered by `v-if`, `v-show`, dynamic `<component :is>`, or a changing `key`. Exactly one child element.

## 2. Modes and options
- `mode="out-in"`: old leaves before new enters (avoids both in layout at once). Default is simultaneous.
- `appear`: animate on initial render.
- `:duration="{ enter: 300, leave: 200 }"` when nested children animate longer than the root.
- Animate only `transform` and `opacity` for 60fps.

## 3. Swap content by key
```vue
<Transition name="slide" mode="out-in"><span :key="count">{{ count }}</span></Transition>
```

## 4. TransitionGroup for lists
```vue
<TransitionGroup name="list" tag="ul">
  <li v-for="item in items" :key="item.id">{{ item.text }}</li>
</TransitionGroup>
<style>
.list-move, .list-enter-active, .list-leave-active { transition: all .3s ease; }
.list-enter-from, .list-leave-to { opacity: 0; transform: translateX(30px); }
.list-leave-active { position: absolute; }   /* lets siblings animate into the gap */
</style>
```
Every child needs a stable `key`. `.list-move` gives FLIP reorder animations. No `mode` support.

## 5. JS hooks
```vue
<Transition :css="false" @enter="(el, done) => gsap.from(el, { opacity: 0, onComplete: done })" @leave="onLeave">
```
Call `done` or the transition ends immediately with `:css="false"`.

## 6. Route transitions
```vue
<RouterView v-slot="{ Component, route }">
  <Transition :name="route.meta.transition || 'fade'" mode="out-in">
    <component :is="Component" :key="route.path" />
  </Transition>
</RouterView>
```

## 7. Reduced motion
```css
@media (prefers-reduced-motion: reduce) {
  .fade-enter-active, .fade-leave-active, .list-move { transition: none; }
}
```

## Verify
- [ ] No layout jump when an element leaves (absolute positioning / out-in mode).
- [ ] Reordering a list animates items; keys are ids, not indices.
- [ ] With OS reduced motion on, transitions are removed or minimal.
