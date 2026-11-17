---
id: computing-software.software-engineering.javascript.js-shadow-dom-slots-styling
name: js-shadow-dom-slots-styling
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, shadow-dom-slots, js-web-components]
level: advanced
status: docs-checked
description: "Attach shadow roots, choose open or closed mode, style with constructable stylesheets, and know slot and attribute inheritance."
sources: ["https://developer.mozilla.org/en-US/docs/Web/API/Web_components/Using_shadow_DOM"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Shadow DOM slots and styling

- Terms: shadow host (the regular node), shadow tree, shadow boundary, shadow root (root of the tree). Code inside a shadow tree cannot affect anything outside it.
- `host.attachShadow({ mode: "open" })` lets page JavaScript reach the tree through `host.shadowRoot`. With `mode: "closed"`, `shadowRoot` returns `null`. MDN says not to treat closed mode as a strong security mechanism (browser extensions can evade it); it signals that the page should not access the internals.
- Declarative creation: `<template shadowrootmode="open">` (or `closed`), plus attributes such as `shadowrootclonable` and `shadowrootdelegatesfocus`; suited to server-rendered UI.
- Page CSS does not style nodes inside the shadow tree, and shadow-tree styles do not leak out.
- Style inside the tree with a `<style>` element in the template, or programmatically: create a `CSSStyleSheet`, set its content with `replace()` or `replaceSync()`, then assign `shadow.adoptedStyleSheets = [sheet]`. One sheet can be shared among many shadow trees (parsed once), and later changes to it propagate to every component using it.
- Slots: assigning an element to a `<slot>` does not change its parent node. The assigned element inherits `lang` and `dir` from its parent outside the shadow tree, while the slot and its fallback content inherit within the shadow tree. CSS `direction` is inherited through the flattened tree, so the rendered direction follows the slot.
- `lang` and `dir` on a shadow root's children are inherited from the shadow host.
- Related MDN topics for the styling and slot selectors (`::slotted()`, `::part`) and composed events are in separate pages: read them before relying on those details.

Self-check: a global stylesheet rule on `span` does not affect a span inside the shadow tree.

## Checked

2026-11-08. Confirmed on MDN Using shadow DOM: terminology, open versus closed mode, declarative shadow DOM, CSS encapsulation, constructable stylesheets with `adoptedStyleSheets`, and slot attribute inheritance. Removed the claims about `slotchange`, `::part(name)`, `::slotted(sel)`, CSS custom properties piercing the boundary, and `composed: true` / `composedPath()` event behaviour, which this page only links to.

Method: docs-only read of cited pages, 2026-11-08
