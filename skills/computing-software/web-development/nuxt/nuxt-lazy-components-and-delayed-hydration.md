---
id: computing-software.web-development.nuxt.nuxt-lazy-components-and-delayed-hydration
name: nuxt-lazy-components-and-delayed-hydration
category: computing-software
field: web-development
product: nuxt
tags: [nuxt, lazy-components, lazy-hydration, hydrate-on-visible, performance]
level: advanced
status: docs-checked
description: "Lazy-load components with the Lazy prefix and delay hydration using hydrate-on-visible, idle, interaction, media-query, after, when and never."
sources:
  - https://github.com/nuxt/nuxt/blob/main/docs/2.directory-structure/1.app/1.components.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Add the `Lazy` prefix to a component's name (`<LazyMountainsList v-if="show" />`) to delay loading its code until the right moment, which can reduce the JavaScript bundle size. Lazy components still load eagerly unless conditionally rendered, so for runtime performance Nuxt also supports lazy (delayed) hydration, which controls when components become interactive. Only one strategy can be used per lazy component.

- `hydrate-on-visible`: when it becomes visible in the viewport.
- `hydrate-on-idle`: when the browser is idle; you can also pass a number as a max timeout.
- `hydrate-on-interaction="mouseover"`: after the given event(s); with no event it defaults to `pointerenter`, `click` and `focus`.
- `hydrate-on-media-query="(max-width: 768px)"`: when the window matches the query.
- `:hydrate-after="2000"`: after a delay in milliseconds.
- `:hydrate-when="isReady"`: based on a boolean condition.
- `hydrate-never`: never hydrates.

All delayed hydration components emit a `@hydrated` event when hydrated. Any prop change on a lazily hydrated component triggers hydration immediately (even with `hydrate-never`).

Limits and advice from the docs: Nuxt's built-in lazy hydration currently works only in single-file components, requires the prop to be written in the template (not spread via a `v-bind` object), and does not work with direct imports from `#components`. Avoid delayed hydration for critical above-the-fold content. When using `v-if="false"` on a lazy component you might not need delayed hydration; a normal lazy component is enough. Shared state (`v-model`) across several components can trigger hydration in all components bound to that model. Do not use `hydrate-never` on components that need user interaction.

## Checked

2026-11-04. Confirmed against the Nuxt components directory page: Lazy prefix, all seven hydrate strategies and their arguments, interaction default events, idle timeout, @hydrated, prop-change note, SFC/template-prop/#components limits, the five caveats. Reworded the Lazy-prefix effect to what the page says (delayed code loading, not a promise about chunks). Removed the Verify step.

Method: documentation only; no commands were run.
