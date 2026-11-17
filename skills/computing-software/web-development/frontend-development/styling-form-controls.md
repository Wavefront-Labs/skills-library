---
id: computing-software.web-development.frontend-development.styling-form-controls
name: styling-form-controls
category: computing-software
field: web-development
product: frontend-development
tags: [accent-color, customizable-select, appearance-none, field-sizing, color-scheme, form-styling, css]
level: practitioner
status: docs-checked
description: "Styling native form controls: accent-color, color-scheme, appearance none for custom checkboxes, field-sizing content and appearance base-select customizable select."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/accent-color
  - https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Forms/Customizable_select
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/field-sizing
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/color-scheme
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Styling native form controls

Keep the native element (keyboard, autofill, a11y for free); restyle it rather than rebuilding with divs.

## 1. Cheapest wins
```css
:root { color-scheme: light dark; accent-color: #4f46e5; }
textarea { field-sizing: content; min-block-size: 3lh; max-block-size: 12lh; }
```
- `accent-color` tints checkbox, radio, range, progress.
- `color-scheme` makes UA controls, scrollbars and default backgrounds follow dark mode.
- `field-sizing: content` auto-grows textarea/inputs (Chrome 123, Firefox 152, Safari 26.2; older browsers keep a fixed size).

## 2. Custom checkbox without losing semantics
```css
input[type="checkbox"] {
  appearance: none; inline-size: 1.25rem; block-size: 1.25rem;
  border: 2px solid currentColor; border-radius: .25rem; display: inline-grid; place-content: center;
}
input[type="checkbox"]::before { content: ""; inline-size: .65rem; block-size: .65rem;
  clip-path: polygon(14% 44%, 0 65%, 50% 100%, 100% 16%, 80% 0, 43% 62%);
  background: CanvasText; transform: scale(0); }
input[type="checkbox"]:checked::before { transform: scale(1); }
input[type="checkbox"]:focus-visible { outline: 2px solid; outline-offset: 2px; }
```
`appearance: none` keeps the input focusable and checkable.

## 3. Customizable select (Chrome 135+, Safari 27; Firefox behind a flag)
```css
select, ::picker(select) { appearance: base-select; }
select::picker-icon { content: "▾"; }
option:checked { font-weight: 600; }
```
```html
<select>
  <button><selectedcontent></selectedcontent></button>
  <option value="a"><img src="a.svg" alt=""> Alpha</option>
</select>
```
Unsupported browsers ignore `base-select`, drop the `<button>` structure and show only the text of each option, so this is progressive enhancement.

## Gotchas
- Test custom controls under `@media (forced-colors: active)`.
- Style the file input button with the standard `::file-selector-button` (Chrome 89, Firefox 82, Safari 14.1).
- Never remove focus outlines without a replacement.

## Verify
- [ ] Controls readable in dark mode and forced-colors mode.
- [ ] Space toggles custom checkboxes; screen reader still announces "checkbox, checked".

## Checked
2026-10-26. MDN accent-color, color-scheme, field-sizing and customizable select pages plus browser-compat-data (main, 2026-10-26): confirmed accent-color applies to checkbox, radio, range and progress, color-scheme sets the default colours of canvas, scrollbars and form controls, field-sizing: content support (Chrome 123, Firefox 152, Safari 26.2), appearance: base-select, ::picker(select), ::picker-icon and selectedcontent support (Chrome 135, Safari 27, Firefox flag only), the fallback behaviour in unsupported browsers, and ::file-selector-button support. Removed the unconfirmed forced-colors and pseudo-element claims.
Method: documentation only; no commands were run.
