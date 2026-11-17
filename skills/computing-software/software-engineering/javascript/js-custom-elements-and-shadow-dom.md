---
id: computing-software.software-engineering.javascript.js-custom-elements-and-shadow-dom
name: js-custom-elements-and-shadow-dom
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, js-custom-elements, shadow-dom, web-components, html-templates, slots]
level: advanced
status: docs-checked
description: "Build Web Components with customElements, Shadow DOM, slots and lifecycle callbacks."
sources: ["https://developer.mozilla.org/en-US/docs/Web/API/Web_components/Using_custom_elements", "https://developer.mozilla.org/en-US/docs/Web/API/Web_components/Using_shadow_DOM"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom elements and Shadow DOM

- Define with `class MyEl extends HTMLElement {}` then `customElements.define("my-el", MyEl)` right after the class; the name must start with a lowercase letter and contain a hyphen. The browser calls the class, not you.
- Lifecycle: `constructor` (set up state, register listeners, create a shadow root; do not inspect or add attributes or children), `connectedCallback` (each time added to the document; the spec recommends doing setup here), `disconnectedCallback` (each time removed), `adoptedCallback` (moved to a new document), `attributeChangedCallback` (only for names in `static observedAttributes`; it also fires at parse time for observed attributes present in the markup).
- Moving an element (for example `insertBefore`) fires `disconnectedCallback` then `connectedCallback`; define `connectedMoveCallback` and move with `Element.moveBefore()` to keep state and skip both callbacks.
- Shadow DOM: `this.attachShadow({ mode: "open" })` creates the shadow root. With `open`, page JavaScript reaches it via `element.shadowRoot`; with `closed`, `shadowRoot` returns null. Declarative alternative: `<template shadowrootmode="open">`.
- Style hooks listed by MDN: `:host`, `:host()`, `:host-context()`, `::slotted()`, `::part`. An element assigned to a `<slot>` keeps inheriting from its parent outside the shadow tree.
- Clean up listeners and observers in `disconnectedCallback`.
- Customized built-ins register with `customElements.define("word-count", WordCount, { extends: "p" })`.

## Checked

Checked 2026-11-09 against MDN "Using custom elements" and "Using shadow DOM", with the lifecycle, `observedAttributes`, name rule, `mode` and slot inheritance sections read in full (partial read of the remaining sections via search).
Confirmed: every point above.
Removed as unconfirmed: `customElements.whenDefined`, `composed: true` event retargeting, `formAssociated`/`ElementInternals`, property-to-attribute reflection advice, the React 19 note, and the ECMAScript spec landing source.

Method: documentation only; no commands were run.
