---
id: computing-software.software-engineering.javascript.js-custom-element-lifecycle-forms
name: js-custom-element-lifecycle-forms
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, form-associated-custom-elements, js-web-components]
level: advanced
status: docs-checked
description: "Register custom elements with customElements.define: valid names, lifecycle callbacks, observedAttributes, formAssociated hooks and errors."
sources: ["https://developer.mozilla.org/en-US/docs/Web/API/CustomElementRegistry/define"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom element lifecycle and form association

- `customElements.define(name, constructor)` or `define(name, constructor, { extends: "p" })` for a customized built-in element (class must inherit from the matching interface, such as `HTMLParagraphElement`, and is used as `<p is="...">`). Omit the options for an autonomous element.
- Valid names: start with an ASCII lowercase letter, contain a hyphen, no ASCII uppercase letters, no ASCII whitespace, NULL, `/` or `>`, and not one of the reserved names (`annotation-xml`, `color-profile`, `font-face`, `font-face-src`, `font-face-uri`, `font-face-format`, `font-face-name`, `missing-glyph`).
- Prototype methods read by `define()`: `connectedCallback`, `disconnectedCallback`, `connectedMoveCallback`, `adoptedCallback`, `attributeChangedCallback`. Static properties: `observedAttributes` (an array of strings, only read if `attributeChangedCallback` is defined), `disabledFeatures` (`"internals"` and/or `"shadow"`) and `formAssociated` (boolean).
- If `formAssociated` is true the class can also have `formAssociatedCallback`, `formResetCallback`, `formDisabledCallback` and `formStateRestoreCallback`.
- All these methods and properties are retrieved once, when `define()` is called, so adding them later has no effect. For the callbacks' timing, MDN points to its "Using custom elements" guide.
- On `define()`, existing elements already connected to the document (including in shadow trees) that match are upgraded automatically.
- Errors: `NotSupportedError` if the name or constructor is already registered, or `extends` names a custom element or an unknown element; `SyntaxError` for an invalid name; `TypeError` if the constructor is not a constructor.

Self-check: defining the same name twice throws `NotSupportedError`; a name without a hyphen throws `SyntaxError`.

## Checked

Confirmed on the MDN CustomElementRegistry.define page: signatures, name rules, callback and static property lists, form-associated callbacks, once-only retrieval, upgrade on define and the three exception types. Removed: cleanup-in-`disconnectedCallback` advice, `customElements.get`, the constructor-children caution, `attachInternals`/`setFormValue`/`setValidity` and property-reflection advice, which the page does not state (it defers to a separate guide).

Method: docs-only read of cited pages, 2026-11-08
