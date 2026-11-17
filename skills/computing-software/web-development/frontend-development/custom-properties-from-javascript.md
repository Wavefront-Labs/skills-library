---
id: computing-software.web-development.frontend-development.custom-properties-from-javascript
name: custom-properties-from-javascript
category: computing-software
field: web-development
product: frontend-development
tags: [custom-properties-javascript, css-custom-properties, css-variables, getcomputedstyle, javascript]
level: practitioner
status: docs-checked
description: "Reading and writing CSS custom properties from JavaScript: setProperty and getComputedStyle, scoping, passing pointer and scroll values to CSS, units, and performance of updates."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Cascading_variables/Using_custom_properties
  - https://developer.mozilla.org/en-US/docs/Web/API/CSSStyleDeclaration/setProperty
  - https://developer.mozilla.org/en-US/docs/Web/API/Window/getComputedStyle
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reading and writing custom properties from JavaScript

Custom properties are the cleanest bridge between JS state and CSS: JS writes a number, CSS decides what it means.

## 1. Write
```js
el.style.setProperty("--progress", 0.42);                 // inline on the element, inherits to children
document.documentElement.style.setProperty("--accent", "oklch(65% .2 250)");
el.style.removeProperty("--progress");
```
- Use `setProperty`/`getPropertyValue` for custom properties, as in MDN's "Values in JavaScript" section.
- Names are case-sensitive (`--my-color` and `--My-color` differ) and start with `--`.
- Write unitless numbers and let CSS add units: `transform: translateX(calc(var(--x) * 1px))`. Keeps JS free of styling decisions.

## 2. Read
```js
const raw = getComputedStyle(el).getPropertyValue("--gap").trim();   // string, e.g. " 1rem" -> "1rem"
```
To constrain the type, set an initial value or control inheritance, register the property with `@property --gap { syntax: "<length>"; inherits: true; initial-value: 0px; }`.

## 3. Patterns
```js
// Pointer-follow spotlight
card.addEventListener("pointermove", (e) => {
  const r = card.getBoundingClientRect();
  card.style.setProperty("--mx", e.clientX - r.left);
  card.style.setProperty("--my", e.clientY - r.top);
});
```
```css
.card { background: radial-gradient(20rem at calc(var(--mx) * 1px) calc(var(--my) * 1px), #fff3, transparent); }
```
- Theme switching: set a `data-theme` attribute and define tokens per attribute in CSS rather than writing dozens of properties from JS.

## 4. Performance
- A custom property declared with plain `--name` always inherits from its parent; register it with `@property` and `inherits: false` when it should not.
- Set a property on the smallest element that needs it rather than on `:root`, so style invalidation stays local.
- Batch writes in `requestAnimationFrame` for pointer input.

## Verify
- [ ] Values update the visual as expected and properties are scoped to the element, not root, where possible.

## Checked

Checked 2026-10-26 against mdn/content (main) Using CSS custom properties (Values in JavaScript, `@property` and inheritance, case sensitivity) and CSSStyleDeclaration.setProperty.

- Confirmed: `style.setProperty`/`getPropertyValue` and `getComputedStyle(el).getPropertyValue` work with custom properties; names are case-sensitive; a plain custom property always inherits, and `@property` controls inheritance, syntax and initial value.
- Removed: the claims that `style["--x"]` does not work, that unregistered properties return an unresolved token string from `computedStyleMap`, the React and scroll-driven-animation advice, and the `:root` invalidation and forced style recalculation statements, none of which the pages checked state.

Method: documentation only; no commands were run.
