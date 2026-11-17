---
id: computing-software.web-development.frontend-development.shadow-dom-slots
name: shadow-dom-slots
category: computing-software
field: web-development
product: frontend-development
tags: [web-components, custom-elements, shadow-dom-slots, named-slots, slotchange, slotted, assignednodes, imperative-slot-assignment]
level: practitioner
status: docs-checked
description: "Composing content into web components with default and named slots, fallback content, ::slotted styling, slotchange and assignedElements."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/Web_components/Using_templates_and_slots
  - https://developer.mozilla.org/en-US/docs/Web/API/HTMLSlotElement
  - https://developer.mozilla.org/en-US/docs/Web/CSS/::slotted
  - https://drafts.csswg.org/css-shadow-1/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Shadow DOM slots

**Goal:** components accept arbitrary markup in defined places and react when that content changes.

## 1. Default and named slots
```html
<template id="card-tpl">
  <style>
    ::slotted([slot="title"]) { margin: 0; font-size: 1.25rem; }
  </style>
  <header><slot name="title">Untitled</slot></header>
  <div class="body"><slot></slot></div>
  <footer><slot name="actions"></slot></footer>
</template>
<x-card>
  <h2 slot="title">Order #42</h2>
  <p>Shipped yesterday.</p>
  <button slot="actions">Track</button>
</x-card>
```
- Children without a `slot` attribute go into the unnamed (default) slot. If two slots share a name, matching children go to the first.
- Text inside `<slot>` is fallback content shown when nothing is assigned.
- Slotted nodes stay in the light DOM: page CSS styles them, `querySelector` finds them, they keep their event listeners. They are only **rendered** in the slot position.

## 2. Styling limits
`::slotted(selector)` matches only the top-level assigned elements (not descendants), and loses to page CSS on specificity. Put most styling of slotted content in page CSS.

## 3. Reacting to content
```js
const slot = this.shadowRoot.querySelector('slot[name="actions"]');
slot.addEventListener('slotchange', () => {
  const items = slot.assignedElements({ flatten: true });
  this.toggleAttribute('has-actions', items.length > 0);   // hide empty footer via :host([has-actions])
});
```
`slotchange` fires when the nodes contained in the slot change; use a MutationObserver to watch their content. `flatten: true` also returns the nodes assigned to slots nested inside this slot.

## 4. Accessibility
ARIA relationships (`aria-labelledby`) cannot reference ids across shadow boundaries; keep label and control in the same tree or use ElementInternals `ariaLabelledByElements` where supported.

## 5. Imperative assignment
`attachShadow({ mode:'open', slotAssignment:'manual' })` then `slot.assign(node)` to choose which children go where (tabs, carousels). Supported since Chrome 86, Firefox 92 and Safari 16.4; the declarative `shadowrootslotassignment` attribute is experimental.

## Verify
- [ ] Missing optional slots render fallback or hide their wrapper.
- [ ] Adding/removing slotted children at runtime updates `has-actions`.
- [ ] Screen reader reads content in a sensible order.

## Checked

Checked 2026-10-26 against mdn/content Using templates and slots, HTMLSlotElement, the `slotchange` event and `::slotted` pages, and mdn/browser-compat-data.

- Confirmed: default versus named slot assignment and duplicate-name behaviour; fallback content; `assignedElements({ flatten })`; manual assignment via `slotAssignment: "manual"` and `assign()`; `::slotted()` matches elements only, never text nodes, and works only in CSS inside a shadow tree (top-level assigned elements only, per the CSS Shadow draft).
- Removed: "children naming a non-existent slot are not rendered" and the accessibility-tree order sentence, which the pages checked do not state.

Method: documentation only; no commands were run.
