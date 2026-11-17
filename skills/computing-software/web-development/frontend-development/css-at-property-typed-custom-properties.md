---
id: computing-software.web-development.frontend-development.css-at-property-typed-custom-properties
name: css-at-property-typed-custom-properties
category: computing-software
field: web-development
product: frontend-development
tags: [css-custom-properties, at-property, registered-properties, css-animation, houdini, animating-custom-properties]
level: practitioner
status: docs-checked
description: "Registering typed custom properties with @property to animate gradients and numbers, control inheritance and initial values, and avoid invalid-value surprises."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@property
  - https://developer.mozilla.org/en-US/docs/Web/API/CSS/registerProperty_static
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@property/syntax
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/var
  - https://www.w3.org/TR/css-properties-values-api-1/
  - https://github.com/mdn/browser-compat-data
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# @property typed custom properties

## 1. Why
Unregistered custom properties are untyped token strings: the browser cannot interpolate them, so `transition: --angle 1s` jumps instantly. Registering gives a type, an initial value and inheritance control. Baseline 2024 (Firefox 128+).

## 2. Register
```css
@property --angle {
  syntax: "<angle>";
  inherits: false;
  initial-value: 0deg;
}
.spinner-border {
  background: conic-gradient(from var(--angle), #0b5fff, transparent 40%);
  animation: spin 2s linear infinite;
}
@keyframes spin { to { --angle: 360deg; } }

@property --progress { syntax: "<percentage>"; inherits: true; initial-value: 0%; }
.bar { background: linear-gradient(to right, var(--accent) var(--progress), #ddd 0); transition: --progress .4s; }
```
JS equivalent: `CSS.registerProperty({ name: "--progress", syntax: "<percentage>", inherits: true, initialValue: "0%" })`.

## 3. Syntax values
`<length>`, `<number>`, `<percentage>`, `<length-percentage>`, `<color>`, `<angle>`, `<time>`, `<integer>`, `<transform-function>`, `<image>`, `<url>`, `"*"` (any, no animation), lists `<length>+`, unions `<length> | auto`.

## 4. Behaviour changes
- A registered property with a non-universal `syntax` and an `initial-value` always has a usable value: `var()` substitutes that initial value when no other declaration applies, and the `var()` fallback is not used.
- `inherits: false` stops values cascading into children - useful for component-local variables.
- `syntax` and `inherits` are both required (the rule is ignored without them). `initial-value` is required unless syntax is `"*"`, and must be computationally independent (`10px` ok, `3em` not).
- Registration is global. If several valid `@property` rules use the same name, the last one in stylesheet order wins; if the name is also registered with `CSS.registerProperty()`, the JavaScript registration wins, and `registerProperty()` throws `InvalidModificationError` when the name is already registered.

## 5. Uses
Animating gradient stops/angles, smooth colour token transitions, typed design tokens.

## Verify
The animation interpolates smoothly instead of stepping.

## Checked

Checked 2026-10-26 against current documentation. MDN `@property` and its `syntax`, `inherits`, `initial-value` descriptor pages, `CSS.registerProperty()`, `var()` and CSS error-handling pages, plus browser-compat-data (Chrome 85, Firefox 128, Safari 16.4). Fixed: duplicate registrations are last-wins (and the JavaScript registration wins over `@property`), not first-wins.

Method: documentation only; no commands were run.
