---
id: computing-software.web-development.frontend-development.inline-svg-icons-and-sprites
name: inline-svg-icons-and-sprites
category: computing-software
field: web-development
product: frontend-development
tags: [canvas-api, inline-svg, svg-sprites, icons, accessible-svg, svg, svg-sprite, svg-symbol-use]
level: practitioner
status: docs-checked
description: "Using SVG for icons and graphics: inline vs sprite vs img, currentColor theming, viewBox sizing, SVGO, and accessible names or hiding for decorative icons."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/SVG/Element/use
  - https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/viewBox
  - https://www.w3.org/WAI/tutorials/images/decorative/
  - https://github.com/svg/svgo
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Inline SVG, icons and sprites

## 1. Choose the delivery
| Method | Styling with CSS | Caching | Use for |
|---|---|---|---|
| Inline `<svg>` | full (fill, stroke, currentColor, animation) | no (in HTML/JS) | a few icons, interactive graphics |
| Sprite + `<use href="/icons.svg#x">` | `currentColor` and inherited props | yes | icon systems |
| `<img src=x.svg>` | none from page | yes | illustrations, logos |
| CSS `mask-image` | colour via background | yes | decorative icons in CSS |

## 2. Sprite
```html
<!-- icons.svg -->
<svg xmlns="http://www.w3.org/2000/svg"><symbol id="search" viewBox="0 0 24 24"><path d="…"/></symbol></svg>
<!-- usage -->
<svg class="icon" aria-hidden="true" focusable="false"><use href="/icons.svg#search"/></svg>
```
```css
.icon { width: 1em; height: 1em; fill: currentColor; vertical-align: -0.125em; }
```
External sprite files must be same-origin (`<use>` does not do CORS).

## 3. Clean the source
Run SVGO to strip editor metadata. Keep `viewBox`, remove fixed `width`/`height` and hardcoded `fill="#000"` (replace with `currentColor`). Ensure `viewBox` matches artwork or icons appear offset.

## 4. Accessibility
- Decorative / next to visible text: `aria-hidden="true"`.
- Standalone meaningful graphic: `<svg role="img" aria-labelledby="t"><title id="t">Warning</title>…</svg>`.
- Icon-only button: name the button, hide the icon:
```html
<button type="button" aria-label="Search"><svg aria-hidden="true">…</svg></button>
```

## 5. Pitfalls
- Duplicate `id`s when inlining the same SVG with gradients/clipPaths multiple times - later instances break. Prefix ids per instance or use sprites.
- Forced colours mode: use `currentColor` so icons follow system colours; hardcoded fills may vanish.
- Inline SVG in JS bundles adds bytes to every page - sprite large icon sets.

## Verify
Run an accessibility checker on the page; emulate forced colours in DevTools and confirm icons stay visible.

## Checked
2026-10-28. Confirmed on MDN `<use>`: browsers may apply the same-origin policy to `<use>` and there is no defined way to set a cross-origin policy, so external sprites should be same-origin. Removed: icon-font claims, focusable and role=img compatibility notes, axe rule id and SVGO merge behaviour (not confirmed on fetched pages).
Method: documentation only; no commands were run.
