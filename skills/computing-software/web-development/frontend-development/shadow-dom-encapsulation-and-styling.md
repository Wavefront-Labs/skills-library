---
id: computing-software.web-development.frontend-development.shadow-dom-encapsulation-and-styling
name: shadow-dom-encapsulation-and-styling
category: computing-software
field: web-development
product: frontend-development
tags: [web-components, custom-elements, shadow-dom, css-parts, host-selector, adoptedstylesheets, constructable-stylesheets, css-custom-properties-theming]
level: practitioner
status: docs-checked
description: "Styling Shadow DOM components: :host, ::part, CSS custom properties for theming, constructable/adopted stylesheets, and what does and doesn't cross the boundary."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/Web_components/Using_shadow_DOM
  - https://developer.mozilla.org/en-US/docs/Web/CSS/::part
  - https://developer.mozilla.org/en-US/docs/Web/API/Document/adoptedStyleSheets
  - https://drafts.csswg.org/css-shadow-1/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Shadow DOM encapsulation and styling

**Goal:** component styles don't leak in or out, while consumers can still theme the component through a deliberate API.

## 1. Attach and style
```js
const sheet = new CSSStyleSheet();
sheet.replaceSync(`
  :host { display: inline-block; --btn-bg: #1d4ed8; }
  :host([disabled]) { opacity: .5; pointer-events: none; }
  :host(:focus-within) button { outline: 2px solid var(--focus-ring, currentColor); }
  button { background: var(--btn-bg); color: white; border: 0; padding: .5em 1em; }
`);
class XButton extends HTMLElement {
  constructor() { super(); const root = this.attachShadow({ mode: 'open', delegatesFocus: true });
    root.adoptedStyleSheets = [sheet]; root.innerHTML = `<button part="control"><slot></slot></button>`; }
}
```
Constructable stylesheets are parsed once and shared by every instance (cheaper than a `<style>` per instance).

## 2. What crosses the boundary
| Crosses in | Doesn't |
|---|---|
| Inherited properties (`color`, `font-*`, `line-height`) | Page selectors (`.btn`, `button {}`) |
| CSS custom properties | Global resets |
| `::part()` from outside on elements with `part` | IDs - `document.querySelector` can't see inside |

## 3. Theming API, in order of preference
1. **Custom properties** documented per component (`--btn-bg`).
2. **`::part(name)`** for structural styling: `x-button::part(control) { border-radius: 999px }`. Parts are visible only to the parent DOM, so use `exportparts` to forward parts from nested components. `::part()` cannot be followed by another `::part()`, but `::before`/`::after` and `:state()` can follow it.
3. Slotted content is styled by the light DOM (page CSS), and from inside only top-level via `::slotted(*)`.

## 4. Gotchas
- `delegatesFocus: true` makes clicking/focusing the host focus the inner control.
- Page stylesheets do not apply inside shadow roots (MDN, Encapsulation from CSS): adopt a shared constructable sheet for utility CSS, or skip shadow DOM for app-internal components.
- With `mode: 'closed'`, `element.shadowRoot` returns `null`; with `mode: 'open'` the page can reach inside.

## Verify
- [ ] Page CSS like `button { all: unset }` doesn't affect the component.
- [ ] Custom properties and `::part` changes from the page restyle it.
- [ ] Focus ring visible when tabbing to the host.

## Checked

Checked 2026-10-26 against mdn/content Using shadow DOM, `::part`, `::slotted`, `:host` and ShadowRoot.delegatesFocus pages and the CSS Shadow Module Level 1 draft.

- Confirmed: constructable stylesheets assigned to `adoptedStyleSheets` are parsed once and shared across trees; page styles do not reach into the shadow tree; `mode: "closed"` makes `shadowRoot` return null; `::part()` is visible only to the parent DOM and `exportparts` forwards parts; `delegatesFocus` behaviour; inheritance and custom properties flow through the flattened tree.
- Removed: the claims that outer rules override `:host` rules, that `@font-face` inside shadow roots is ignored in some engines, that form controls in shadow DOM do not submit with outer forms, and that `closed` does not make anything secure; none is stated in the pages checked (the CSS Shadow draft says `@font-face` is honoured inside the shadow tree).

Method: documentation only; no commands were run.
