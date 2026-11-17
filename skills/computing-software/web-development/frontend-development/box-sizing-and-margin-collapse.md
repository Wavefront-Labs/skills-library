---
id: computing-software.web-development.frontend-development.box-sizing-and-margin-collapse
name: box-sizing-and-margin-collapse
category: computing-software
field: web-development
product: frontend-development
tags: [box-model, box-sizing, margin-collapse, css, layout, margin-collapsing, block-formatting-context]
level: practitioner
status: docs-checked
description: "Controlling CSS box sizing and margin collapsing: border-box resets, when vertical margins collapse or do not, and spacing strategies like gap and the owl selector."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/box-sizing
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Box_model/Margin_collapsing
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Display/Block_formatting_context
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# box-sizing and margin collapsing

## 1. border-box everywhere
```css
*, *::before, *::after { box-sizing: border-box; }
```
With the default `content-box`, `width: 100%; padding: 1rem` overflows its parent by 2rem. `border-box` makes `width` include padding and border. Form controls already default to border-box for some types - the reset makes them consistent.

## 2. When margins collapse
Adjacent **vertical** block margins in normal flow combine into the larger of the two (negative margins: the sum of max positive and most negative):
- Siblings: `h2 { margin-bottom: 24px }` + `p { margin-top: 16px }` = 24px gap, not 40.
- Parent and first/last child: child's `margin-top` escapes through the parent if the parent has no border, padding, inline content, or new formatting context. Classic symptom: a heading's margin pushes the whole card down.
- Empty blocks: own top and bottom margins collapse.

## 3. When they do not
Flex and grid items, floats, absolutely positioned elements, inline-blocks, elements with `display: flow-root` or other BFC creators (`overflow` other than visible/clip), and horizontal margins never collapse.

## 4. Fix the escaping-margin bug
```css
.card { display: flow-root; }        /* new block formatting context, no side effects */
/* or padding-block: 1px, or make it a flex/grid container */
```

## 5. Spacing strategy
- Use `gap` in flex/grid layouts - no collapsing surprises, no last-child overrides.
- Single-direction margins (only `margin-block-start` or only end) in flow content.
- Flow utility for prose: `.flow > * + * { margin-block-start: var(--flow-space, 1em); }`.
- Component roots should not set outer margins; let the parent layout space them.

## Verify
DevTools box-model diagram shows the computed margins; toggling `display: flow-root` on the parent confirms a collapse issue.

## Checked
2026-10-26. MDN content repository (main, 2026-10-26): box-sizing page confirms table, select, button and radio/checkbox-type inputs default to border-box; margin collapsing page confirms the negative-margin rule (largest positive plus most negative), the parent/first-child conditions (no border, padding or inline content) and that flex and grid containers do not collapse; block formatting context page confirms overflow other than visible/clip, floats, absolutely positioned elements, inline-block and display: flow-root create a BFC that suppresses margin collapsing and contains floats.
Method: documentation only; no commands were run.
