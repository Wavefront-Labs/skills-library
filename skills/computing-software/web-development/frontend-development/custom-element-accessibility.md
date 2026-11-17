---
id: computing-software.web-development.frontend-development.custom-element-accessibility
name: custom-element-accessibility
category: computing-software
field: web-development
product: frontend-development
tags: [elementinternals-aria, delegatesfocus, custom-states, web-components-accessibility, shadow-dom-aria]
level: advanced
status: docs-checked
description: "Making custom elements accessible: ElementInternals default ARIA, delegatesFocus, custom :state(), focusability, labels, and cross-shadow-root ID reference limits."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/ElementInternals
  - https://developer.mozilla.org/en-US/docs/Web/API/ShadowRoot/delegatesFocus
  - https://developer.mozilla.org/en-US/docs/Web/API/CustomStateSet
  - https://developer.mozilla.org/en-US/docs/Web/API/Web_components/Using_custom_elements
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom element accessibility

## 1. Prefer wrapping native elements
A `<button>` inside the shadow root is focusable, keyboard-operable and announced correctly. Build from native controls; reach for ARIA only for widgets HTML lacks.

## 2. Default semantics with ElementInternals
```js
class XSwitch extends HTMLElement {
  static formAssociated = true;
  #i = this.attachInternals();
  constructor() {
    super();
    this.#i.role = "switch";
    this.#i.ariaChecked = "false";
    this.addEventListener("click", () => this.toggle());
    this.addEventListener("keydown", e => { if (e.key === " " || e.key === "Enter") { e.preventDefault(); this.toggle(); } });
  }
  connectedCallback() {
    if (!this.hasAttribute("tabindex")) this.tabIndex = 0;   // not in the constructor: it must not add attributes
  }
  toggle() {
    const on = this.#i.ariaChecked !== "true";
    this.#i.ariaChecked = String(on);
    on ? this.#i.states.add("checked") : this.#i.states.delete("checked");
    this.#i.setFormValue(on ? "on" : null);
  }
}
customElements.define("x-switch", XSwitch);
```
```css
x-switch:state(checked) { background: green; }
```
Internals ARIA is a default: an author's `role`/`aria-*` attribute on the host overrides it, and the host is not cluttered with attributes. `formAssociated` makes `<label for>` and form submission work.

## 3. Focus delegation
```js
this.attachShadow({ mode: "open", delegatesFocus: true });
```
Clicking non-focusable shadow content or calling `host.focus()` focuses the first focusable element inside; the host matches `:focus`. Good for composite inputs (text field + clear button).

## 4. The ID reference problem
`aria-labelledby`, `aria-describedby`, `aria-controls`, `for` cannot point across a shadow boundary. Options:
- Keep label and control in the same root (put the label inside the component via a slot or `label` property).
- `ariaLabelledByElements` / element reflection (where supported) to set element references from JS.
- `referenceTarget` (the `referenceTarget` option of `attachShadow()` or `shadowrootreferencetarget` on `<template>`) lets a host forward ID references to an inner element. MDN marks it experimental and non-standard, so do not depend on it.

## Gotchas
- `tabindex` on the host plus a focusable inner element = two tab stops.
- Custom element constructors must not add attributes or children, so set `tabindex` in `connectedCallback()`.

## Verify
- [ ] DevTools Accessibility pane shows correct role, name and state on the host.
- [ ] NVDA/VoiceOver announce "switch, off" and update on Space.

## Checked

Checked 2026-10-26 against mdn/content (main) pages for ElementInternals, ShadowRoot.delegatesFocus, CustomStateSet, Using custom elements, Element.attachShadow and the template element, plus the WHATWG HTML source and mdn/browser-compat-data.

- Confirmed: `delegatesFocus` focuses the first focusable shadow part on click or `host.focus()` and gives the host `:focus` styling; `ElementInternals.states` returns a `CustomStateSet` matched by `:state(name)` (Chrome 125, Firefox 126, Safari 17.4); internals ARIA properties are defaults that author attributes may overwrite; `ariaLabelledByElements` exists on ElementInternals; `referenceTarget` is experimental.
- Fixed: the example set `tabIndex` and read `hasAttribute` in the constructor, but custom element constructors must not inspect or add attributes (MDN, WHATWG HTML); it now sets `tabindex` in `connectedCallback()`.
- Removed: the `aria-hidden`/`inert` and flattened-tree gotchas, which no checked page covers.

Method: documentation only; no commands were run.
