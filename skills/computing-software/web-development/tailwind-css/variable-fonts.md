---
id: computing-software.web-development.tailwind-css.variable-fonts
name: variable-fonts
category: computing-software
field: web-development
product: tailwind-css
tags: [web-fonts, typography, variable-fonts, font-variation-settings, font-weight-range, optical-sizing, opsz, wght-axis]
level: practitioner
status: docs-checked
description: "Using variable fonts: @font-face weight ranges, standard axes via font-weight/font-stretch/optical sizing, custom axes with font-variation-settings, size trade-offs."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_fonts/Variable_fonts_guide
  - https://web.dev/articles/variable-fonts
  - https://fonts.google.com/knowledge/introducing_type/introducing_variable_fonts
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Variable fonts

**Goal:** one font file supplies every weight/width you need, with smooth control and fewer requests.

## 1. Declare ranges
```css
@font-face {
  font-family: "Inter";
  src: url("/fonts/InterVariable.woff2") format("woff2") tech(variations), url("/fonts/InterVariable.woff2") format("woff2-variations");
  font-weight: 100 900;          /* range, not a single value */
  font-style: normal;
  font-display: swap;
}
@font-face { font-family: "Inter"; src: url("/fonts/InterVariable-Italic.woff2") format("woff2"); font-weight: 100 900; font-style: italic; }
```
Without the range, browsers treat it as one weight and synthesise bold (faux bold).

## 2. Registered axes -> normal CSS properties
| Axis | Tag | Use |
|---|---|---|
| Weight | `wght` | `font-weight: 650` (any number in range) |
| Width | `wdth` | `font-stretch: 85%` |
| Italic / slant | `ital` / `slnt` | `font-style: italic` / `oblique 10deg` |
| Optical size | `opsz` | `font-optical-sizing: auto` (default) adjusts to font-size |
Prefer these properties over `font-variation-settings` - they inherit and compose properly.

## 3. Custom axes
`font-variation-settings: "GRAD" 50, "CASL" 1;` (uppercase = custom). Caveat: `font-variation-settings` is all-or-nothing - setting one axis on a child resets others set on the parent. Use custom properties:
```css
:root { --grad: 0; --casl: 0; }
body { font-variation-settings: "GRAD" var(--grad), "CASL" var(--casl); }
.dark { --grad: -25; }   /* adjust grade in dark mode */
```

## 4. Size trade-off
A variable file is bigger than one static weight. Using 1-2 weights only? Static subsets may win - measure. Subset (latin) the variable file too.


## Verify
- [ ] DevTools Fonts/Computed shows the variable font used at intermediate weights (no faux bold).
- [ ] Total font bytes not larger than the static set it replaced.
- [ ] Dark-mode grade adjustment doesn't shift layout.

## Checked

2026-10-28. Confirmed in the MDN variable fonts guide and web.dev: font-weight range in @font-face, registered axes (wght, wdth, ital, slnt, opsz) with their CSS properties, font-optical-sizing, case-sensitive axis tags (registered lowercase, custom uppercase), font-synthesis and faux styles. Removed: the file-size comparison with 3+ static weights, the claim that GRAD changes do not reflow, and the animation section.

Method: documentation only; no commands were run.
