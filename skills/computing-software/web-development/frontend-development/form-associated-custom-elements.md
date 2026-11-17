---
id: computing-software.web-development.frontend-development.form-associated-custom-elements
name: form-associated-custom-elements
category: computing-software
field: web-development
product: frontend-development
tags: [web-components, custom-elements, form-associated-custom-elements, elementinternals, setformvalue, setvalidity, formresetcallback, custom-form-controls]
level: practitioner
status: docs-checked
description: "Making custom elements real form controls with ElementInternals: submitting values, validity, labels, reset/restore callbacks and accessibility semantics."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/ElementInternals
  - https://html.spec.whatwg.org/multipage/custom-elements.html#form-associated-custom-elements
  - https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/attachInternals
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Form-associated custom elements

**Goal:** a custom control (rating, tag input, date range) submits with the surrounding `<form>`, validates, resets and labels like a native input.

## 1. Opt in
```js
class StarRating extends HTMLElement {
  static formAssociated = true;
  static observedAttributes = ['value', 'required'];
  #internals = this.attachInternals();
  #value = '';
  constructor() { super(); this.#internals.role = 'slider'; }
  get value() { return this.#value; }
  set value(v) {
    this.#value = String(v);
    this.#internals.setFormValue(this.#value);                     // what gets submitted under name=
    this.#internals.ariaValueNow = this.#value;
    this.#validate();
  }
  get form() { return this.#internals.form; }
  get name() { return this.getAttribute('name'); }
  get validity() { return this.#internals.validity; }
  checkValidity() { return this.#internals.checkValidity(); }
  #validate() {
    if (this.hasAttribute('required') && !this.#value)
      this.#internals.setValidity({ valueMissing: true }, 'Choose a rating', this);
    else this.#internals.setValidity({});
  }
  formResetCallback() { this.value = this.getAttribute('value') ?? ''; }
  formStateRestoreCallback(state) { this.value = state; }          // back/forward and autofill restore
  formDisabledCallback(disabled) { this.toggleAttribute('aria-disabled', disabled); }
  connectedCallback() {
    if (!this.hasAttribute('tabindex')) this.tabIndex = 0;   // not in the constructor: it must not add attributes
    this.#validate();
  }
}
customElements.define('star-rating', StarRating);
```

## 2. What you get
- `<label for="r">` and wrapping labels work; `internals.labels` lists them.
- `new FormData(form)` includes the value; `form.reset()` calls `formResetCallback`.
- Form-associated custom elements are listed, labelable and submittable; `:user-invalid` is defined for them; `form.checkValidity()` includes them. `formDisabledCallback(disabled)` runs when the element's disabled state changes.
- `setFormValue(value, state)` accepts null, a string, a File or FormData (multiple entries); the optional `state` is what `formStateRestoreCallback` receives.

## 3. Accessibility
Default ARIA via `internals.role`, `ariaValueNow`, `ariaLabel`, etc. sets semantics without sprinkling attributes the page could overwrite. You still implement keyboard handling (arrow keys for a slider).

## 4. Support
ElementInternals shipped in Chrome 77, Firefox 93 and Safari 16.4.

## Verify
- [ ] Submitting the form sends `name=value`; required empty blocks submit and shows the message.
- [ ] Reset and back/forward restore values.
- [ ] Screen reader announces the label, role and value.

## Checked

Checked 2026-10-26 against the WHATWG HTML source (form-associated custom elements: callbacks, submission value and state, labelable/listed/submittable), mdn/content ElementInternals and mdn/browser-compat-data.

- Fixed: the class set `tabIndex` in the constructor, which custom element constructors must not do (it adds an attribute); it moved to `connectedCallback()`.
- Confirmed: `formAssociated`, `formResetCallback`, `formStateRestoreCallback(state, mode)`, `formDisabledCallback`, `setValidity`, `checkValidity`, `labels`; the state may be null, a string, a File or a list of entries; support versions.
- Removed: the `element-internals-polyfill` mention and the `:disabled`/`<fieldset disabled>` sentence, which were not confirmed in the pages checked.

Method: documentation only; no commands were run.
