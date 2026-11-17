---
id: computing-software.web-development.web-accessibility.css-background-images-and-text-alternatives
name: css-background-images-and-text-alternatives
category: computing-software
field: web-development
product: web-accessibility
tags: [css-background-image-alt, background-images, non-text-content, text-alternatives, wcag-1-1-1]
level: practitioner
status: docs-checked
description: "Handling CSS background images accessibly: when to use img instead, text alternatives for meaningful backgrounds, text over images and forced-colors behaviour."
sources:
  - https://www.w3.org/WAI/WCAG22/Techniques/failures/F3
  - https://www.w3.org/WAI/WCAG22/Understanding/non-text-content.html
  - https://developer.mozilla.org/en-US/docs/Web/CSS/background-image
  - https://www.w3.org/TR/css-color-adjust-1/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CSS background images and text alternatives

CSS backgrounds have no alt attribute and are invisible to assistive tech. WCAG failure F3: conveying important information only through a CSS image.

## 1. Decide: content or decoration
| Image | Implement as |
|---|---|
| Decorative texture, gradient, hero mood photo | CSS background, no alternative needed |
| Informative (product photo, chart, icon that is the only label) | `<img alt="...">` or inline SVG with a title |
| Hero photo with meaning **and** text overlay | `<img>` with `object-fit: cover` positioned behind text, alt or `alt=""` per meaning |

`<img>` with `object-fit`/`object-position` reproduces `background-size: cover` and gains alt, lazy loading, `srcset` and `fetchpriority`.

## 2. If it must stay a background
```html
<div class="flag flag-fr" role="img" aria-label="France"></div>
<!-- or -->
<a class="icon-link icon-download" href="/report.pdf"><span class="visually-hidden">Download report (PDF)</span></a>
```
`role="img"` + `aria-label` exposes it as an image; for controls, put visually hidden text inside so the name survives CSS failures and translation tools.

## 3. Text over background images
- Text contrast is measured against the busiest part of the image: add a scrim (`linear-gradient(rgb(0 0 0/.55), rgb(0 0 0/.55)), url(...)`) or a solid text panel.
- Always set a `background-color` fallback with sufficient contrast so text stays readable if the image fails or is blocked.

## 4. Forced colors
- In forced colors mode (`forced-colors: active`), `background-image` computes to `none` unless the value contains a `url()` (CSS Color Adjustment), so gradient-only backgrounds disappear and the background colour is forced. Images referenced with `url()` stay but cannot follow the forced palette: prefer inline SVG with `currentColor`, and use `forced-color-adjust: none` sparingly.

## Verify
- [ ] Turning off CSS (or images) loses no information; gradient-based icons still visible in forced-colors mode; text over images meets contrast with a fallback colour.

## Checked

- Date: 2026-10-26. Documentation: WCAG 2.2 technique F3 and 1.1.1, CSS Color Adjustment Module Level 1 (editor's draft source), MDN `background-image` and `content`.
- Confirmed: F3 is a failure of 1.1.1 for conveying information only through CSS background images; the WAI decision tree suggests CSS backgrounds for decorative images; in forced colors mode `background-image` computes to `none` unless it contains `url()`; `forced-color-adjust` exists.
- Corrected: the forced-colors paragraph (url() backgrounds are kept, gradients are dropped). Removed (no documentation found): the LCP remark and the print-default claim.
Method: documentation only; no commands were run.