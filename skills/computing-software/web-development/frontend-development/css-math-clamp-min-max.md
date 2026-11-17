---
id: computing-software.web-development.frontend-development.css-math-clamp-min-max
name: css-math-clamp-min-max
category: computing-software
field: web-development
product: frontend-development
tags: [css-custom-properties, css-clamp, css-math-functions, fluid-typography, calc, css]
level: practitioner
status: docs-checked
description: "Using calc, min, max and clamp for fluid typography and spacing: deriving the preferred value, combining with custom properties, accessibility with zoom, and trig/round functions."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/clamp
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/calc
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/round
  - https://www.w3.org/TR/css-values-4/#math
  - https://github.com/mdn/browser-compat-data
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# calc / min / max / clamp

## 1. Functions
- `calc()` mixes units: `calc(100% - 2 * var(--gutter))`. Spaces around `+` and `-` are required.
- `min(a, b)` picks the smaller (acts as a max-limit): `width: min(100%, 70ch)`.
- `max(a, b)` picks the larger (acts as a min-limit): `padding: max(1rem, env(safe-area-inset-left))`.
- `clamp(MIN, PREFERRED, MAX)` = `max(MIN, min(PREFERRED, MAX))`.
Newer: `round()`, `mod()`, `rem()`, `abs()`, `sign()`, `sin()/cos()/tan()`, `pow()`, `sqrt()`; check browser-compat-data per function (for example `round()`: Chrome 125, Firefox 118, Safari 15.4).

## 2. Fluid type formula
Font grows from 1rem at 360px viewport to 1.5rem at 1280px:
```
slope_vw  = (24px - 16px) / (1280px - 360px) * 100 = 0.8696vw
intercept = 16px - 0.8696vw * 360/100 = 12.87px = 0.8043rem
```
```css
h1 { font-size: clamp(1rem, 0.8043rem + 0.8696vw, 1.5rem); }
```

## 3. Accessibility
- **Always include a rem term** in the preferred value. Pure `vw` font sizes don't respond to browser zoom/text size settings (WCAG 1.4.4 resize text).

## 4. With custom properties
```css
:root { --space-s: clamp(.75rem, .69rem + .29vw, 1rem); --space-m: clamp(1rem, .9rem + .5vw, 1.5rem); }
.stack > * + * { margin-block-start: var(--space-m); }
.container { width: min(100% - 2 * var(--space-m), 75rem); margin-inline: auto; }
```
Container query units (`cqi`) give component-relative fluid sizes: `font-size: clamp(1rem, 4cqi, 1.5rem)`.

## 5. Gotchas
- `clamp` with MIN > MAX: MIN wins.
- `calc()` is type-checked and its result must suit the property (`calc(1 + 2)` is invalid for `margin`); write `0px`, not `0`, next to lengths.
- Percentages resolve against different bases per property (width vs font-size vs translate).

## Verify
Zoom to 200%: text grows; resize from 320 to 1440px: sizes interpolate smoothly between bounds (DevTools computed value).

## Checked

Checked 2026-10-26 against current documentation. MDN `clamp()` (resolves as `max(MIN, min(VAL, MAX))`), `calc()` (typed arithmetic, `+`/`-` whitespace, `*` and `/` rules), `round()` support (Chrome 125, Firefox 118, Safari 15.4) and the `cqi` unit. The fluid-type arithmetic (0.8696vw slope, 12.87px intercept) was recomputed. Removed the Utopia reference and the unconfirmed 2.5x ratio rule.

Method: documentation only; no commands were run.
