---
id: computing-software.web-development.frontend-development.z-index-and-stacking-contexts
name: z-index-and-stacking-contexts
category: computing-software
field: web-development
product: frontend-development
tags: [box-model, stacking-context, z-index, css, layering]
level: practitioner
status: docs-checked
description: "Debugging z-index with stacking contexts: what creates a context, why z-index 9999 fails, isolation:isolate, layer scales, and using the top layer for overlays."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Positioned_layout/Stacking_context
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/isolation
  - https://developer.mozilla.org/en-US/docs/Glossary/Top_layer
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# z-index and stacking contexts

## 1. The rule
`z-index` only orders elements **within the same stacking context**. A child with `z-index: 9999` inside a parent context with `z-index: 1` can never rise above a sibling context with `z-index: 2`.

## 2. What creates a stacking context
- Root element.
- `position: relative/absolute` with `z-index` other than `auto`; `position: fixed/sticky` always.
- Flex/grid children with `z-index` other than `auto`.
- `opacity < 1`, `transform`, `filter`, `backdrop-filter`, `perspective`, `clip-path`, `mask`, `mix-blend-mode` other than normal.
- `isolation: isolate`, `will-change` naming any of the above, `contain: layout/paint`, `container-type: size|inline-size`.
Common surprise: adding `transform` for an animation or `opacity: .99` creates a context and traps a dropdown beneath the next section.

## 3. Debug
- Walk up the ancestors of the element that is too low; find the first that creates a context; compare z at that level.

## 4. Practices
- `isolation: isolate` on component roots creates a context without side effects, so internal z-indexes cannot leak.
- Use a small scale with tokens: `--z-dropdown: 100; --z-sticky: 200; --z-modal: 300; --z-toast: 400`. No arbitrary 9999s.
- Portal overlays (modals, menus, tooltips) to the end of `body` or, better, use the **top layer**: `<dialog>.showModal()` and the `popover` attribute render above everything regardless of z-index or ancestors' overflow.

## Verify
the dropdown renders above subsequent sections after removing the stray context or moving it to the top layer.

## Checked
2026-10-26. MDN stacking context page (main, 2026-10-26): confirmed the full creator list (positioned with z-index not auto, fixed/sticky, container-type size/inline-size, flex and grid items with z-index not auto, opacity below 1, mix-blend-mode, transform/scale/rotate/translate/filter/backdrop-filter/perspective/clip-path/mask, isolation: isolate, will-change, contain layout/paint, top-layer elements). Removed unconfirmed DevTools panel names and the negative z-index paragraph.
Method: documentation only; no commands were run.
