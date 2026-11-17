---
id: computing-software.web-development.frontend-development.css-logical-properties
name: css-logical-properties
category: computing-software
field: web-development
product: frontend-development
tags: [box-model, logical-properties, rtl-layout, writing-modes, css]
level: practitioner
status: docs-checked
description: "Using CSS logical properties (inline/block, start/end) instead of physical left/right/top/bottom so layouts adapt to RTL and vertical writing modes, with migration tips."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Logical_properties_and_values
  - https://www.w3.org/TR/css-logical-1/
  - https://github.com/csstools/stylelint-use-logical
  - https://tailwindcss.com/docs/margin
  - https://github.com/mdn/browser-compat-data
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CSS logical properties

## 1. Axes
- **Inline** axis = direction text runs (horizontal in English, right-to-left in Arabic, vertical in vertical Japanese).
- **Block** axis = direction blocks stack.
- `start`/`end` replace left/right/top/bottom relative to those axes.

## 2. Mapping
| Physical | Logical |
|---|---|
| `width` / `height` | `inline-size` / `block-size` |
| `min-width` | `min-inline-size` |
| `margin-left` / `margin-right` | `margin-inline-start` / `margin-inline-end` |
| `margin-top` + `margin-bottom` | `margin-block` (shorthand: start end) |
| `padding: 0 1rem` horizontal | `padding-inline: 1rem` |
| `top/right/bottom/left` | `inset-block-start` / `inset-inline-end` ... ; `inset-inline: 0` |
| `border-left` | `border-inline-start` |
| `border-top-left-radius` | `border-start-start-radius` |
| `text-align: left` | `text-align: start` |
| `float: left` | `float: inline-start` |
| `overflow-x` | `overflow-inline` (Chrome 135, Firefox 69, Safari 26) |

## 3. Example
```css
.callout { padding-inline: 1.25rem; padding-block: 1rem; border-inline-start: 4px solid var(--accent); margin-block-end: 1.5rem; }
.close { position: absolute; inset-block-start: .5rem; inset-inline-end: .5rem; }
```
With `<html dir="rtl">` the border and close button move to the correct side with zero extra CSS.

## 4. Migration
- New code: logical by default. Stylelint `liberty/use-logical-spec` or `stylelint-use-logical` flags physical properties.
- Tailwind: `ms-*`, `me-*`, `ps-*`, `pe-*`, `text-start`, `rounded-s-*`.
- Keep physical properties where the meaning is truly physical (shadows from a light source, visual effects tied to screen edges).
- `transform: translateX()` and background-position are not logical - flip with `:dir(rtl)`.

## Verify
Toggle `dir="rtl"` on `<html>` (and `writing-mode: vertical-rl` on a test container) - components mirror correctly.

## Checked

Checked 2026-10-26 against current documentation. MDN logical-properties overview (property list including `border-start-start-radius`, `float`, `text-align`, `inset-*`), browser-compat-data for `overflow-inline` (Chrome 135, Firefox 69, Safari 26), Tailwind documentation sources for `ms-*`/`me-*`/`ps-*`/`pe-*`/`text-start`/`rounded-s-*`, and the stylelint-use-logical package name. Removed Tailwind `start-*`/`end-*`, which was not found in its docs.

Method: documentation only; no commands were run.
