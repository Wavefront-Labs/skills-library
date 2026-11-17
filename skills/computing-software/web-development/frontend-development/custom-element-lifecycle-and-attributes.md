---
id: computing-software.web-development.frontend-development.custom-element-lifecycle-and-attributes
name: custom-element-lifecycle-and-attributes
category: computing-software
field: web-development
product: frontend-development
tags: [web-components, custom-elements, custom-element-lifecycle, observedattributes, attributechangedcallback, customelements-define, upgrade, customelements-whendefined]
level: practitioner
status: docs-checked
description: "Writing custom elements: define/upgrade, connected/disconnected/attributeChanged callbacks, attributes vs properties reflection and cleanup."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/Web_components/Using_custom_elements
  - https://html.spec.whatwg.org/multipage/custom-elements.html
  - https://developer.mozilla.org/en-US/docs/Web/API/CustomElementRegistry/define
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Custom element lifecycle and attributes

**Goal:** framework-agnostic elements that behave like built-ins: configurable by attributes and properties, safe to add/remove/move.

## 1. Skeleton
```js
class RelativeTime extends HTMLElement {
  static observedAttributes = ['datetime', 'lang'];
  #timer;
  get datetime() { return this.getAttribute('datetime'); }
  set datetime(v) { this.setAttribute('datetime', v); }          // reflect property -> attribute
  connectedCallback() { this.#render(); this.#timer = setInterval(() => this.#render(), 60_000); }
  disconnectedCallback() { clearInterval(this.#timer); }
  attributeChangedCallback(name, oldV, newV) { if (oldV !== newV && this.isConnected) this.#render(); }
  #render() {
    const d = new Date(this.datetime);
    const mins = Math.round((d - Date.now()) / 60000);
    this.textContent = new Intl.RelativeTimeFormat(this.lang || undefined, { numeric: 'auto' }).format(mins, 'minute');
  }
}
if (!customElements.get('relative-time')) customElements.define('relative-time', RelativeTime);
```
- Names must start with a lowercase letter and contain a hyphen. `define` throws `NotSupportedError` if the name or constructor is already registered - guard it (important with HMR and micro-frontends).
- **Constructor**: don't inspect or add attributes or children (the specification forbids it); do setup in `connectedCallback`.
- `connectedCallback` can run multiple times (element moved); make it idempotent and undo in `disconnectedCallback`. If the class defines `connectedMoveCallback()`, moving the element with `Element.moveBefore()` calls it instead of the connected/disconnected pair.
- Only attributes in `observedAttributes` trigger `attributeChangedCallback`.

## 2. Upgrade timing
Elements in HTML before `define` are "undefined" and get upgraded later. A property set on the element **before** upgrade shadows the class accessor - re-apply it:
```js
connectedCallback() { if (Object.hasOwn(this, 'datetime')) { const v = this.datetime; delete this.datetime; this.datetime = v; } }
```
Hide flash of un-upgraded content with `relative-time:not(:defined) { visibility: hidden }`. `await customElements.whenDefined('relative-time')` when scripting against it (it resolves immediately if already defined). Lit documents the same hazard: it saves properties set before upgrade and re-applies them.

## 3. Attributes vs properties
Strings/booleans/numbers for config: attributes (reflect them). Rich data (arrays, objects): properties only. Boolean attributes: presence = true (`hasAttribute`).

## 4. Events out
Dispatch `CustomEvent`s with `bubbles: true, composed: true` if they must cross shadow boundaries.

## Verify
- [ ] Element works when defined before and after it's in the DOM, and when moved.
- [ ] Removing it clears timers/listeners (no leaks in heap snapshots).
- [ ] Works in React/Vue templates via attributes and properties.

## Checked

Checked 2026-10-26 against mdn/content (main) Using custom elements and CustomElementRegistry.define/whenDefined, the WHATWG HTML source (custom element conformance requirements, `:defined`) and the Lit lifecycle docs.

- Confirmed: valid names start lowercase and contain a hyphen; `define` throws `NotSupportedError` for a duplicate name or constructor; constructors must not gain attributes or children; only `observedAttributes` entries trigger `attributeChangedCallback`; `connectedMoveCallback()` runs instead of connected/disconnected on `moveBefore()` (Chrome 133, Firefox 144); `whenDefined` and `:not(:defined)` exist.
- Changed: the constructor rule now states the specification wording; the web.dev source link was dropped because it could not be re-read.
- Not changed: the pre-upgrade own-property pattern is a widely used workaround, supported by Lit's documented behaviour.

Method: documentation only; no commands were run.
