---
id: computing-software.web-development.tailwind-css.oklch-and-wide-gamut-colour
name: oklch-and-wide-gamut-colour
category: computing-software
field: web-development
product: tailwind-css
tags: [css-color, oklch, wide-gamut, display-p3, perceptual-colour, color-palettes, gamut-mapping, tailwind-v4-colors]
level: practitioner
status: verified
description: "Using OKLCH for perceptually even palettes and wide-gamut (P3) colours: syntax, generating scales, gamut fallbacks with @media (color-gamut) and Tailwind v4's OKLCH palette."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/color_value/oklch
  - https://evilmartians.com/chronicles/oklch-in-css-why-quit-rgb-hsl
  - https://webkit.org/blog/10042/wide-gamut-color-in-css-with-display-p3/
  - https://tailwindcss.com/docs/colors
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OKLCH and wide-gamut colour

**Goal:** colour scales where equal steps look equal, predictable contrast, and richer colours on P3 displays without breaking sRGB screens.

## 1. Syntax
```css
--brand: oklch(62% 0.19 255);          /* lightness 0-100%, chroma ~0-0.37, hue 0-360 */
--brand-50: oklch(97% 0.02 255);
--brand-900: oklch(30% 0.09 255);
color: oklch(from var(--brand) calc(l - 0.1) c h);   /* relative colour syntax: darker variant (l is a 0-1 number here) */
```
- **L** is perceptual lightness: two colours with the same L look equally light across hues (HSL's `l` doesn't - yellow at 50% is far lighter than blue at 50%). This makes contrast more predictable when building scales.
- `calc(l - 10%)` is invalid in Chromium 156 (`CSS.supports` false, the declaration is dropped); use `calc(l - 0.1)` (computed `oklch(0.52 0.19 255)` from `oklch(62% .19 255)`). Relative colour syntax: Chrome 122, Firefox 128, Safari 18 (MDN browser-compat-data); OKLCH itself: Chrome 111, Firefox 113, Safari 15.4.
- Change hue while keeping L and C to get consistent palettes; vary L for tints/shades.

## 2. Wide gamut
OKLCH can express colours outside sRGB (high chroma). On P3 displays they render more vividly; on sRGB displays browsers **gamut-map** them to the nearest displayable colour (CSS Color 4 uses a chroma-reduction in OKLCH, results are generally fine but may shift). For control:
```css
.button { background: #2563eb; }
@media (color-gamut: p3) { .button { background: oklch(55% 0.25 262); } }
```
Or `@supports (color: oklch(0% 0 0))` for old browsers (all current engines support OKLCH).

## 3. Tailwind v4
The default palette is defined in OKLCH (`--color-blue-600: oklch(...)`), giving more vivid colours on P3 screens. Custom palettes in `@theme { --color-brand-500: oklch(…); }`.

## 4. Tools
oklch.com (picker with gamut indicator), Huetone/Leonardo for accessible scales, `culori`/colorjs.io for programmatic generation and conversions.

## 5. Contrast
WCAG 2 contrast is still computed from sRGB relative luminance - check final colours with a contrast tool; L in OKLCH is a guide, not the WCAG formula. APCA (WCAG 3 draft) uses its own model.

## Verify
- [ ] Palette steps look evenly spaced across hues.
- [ ] Contrast pairs meet 4.5:1 / 3:1 after gamut mapping on sRGB.
- [ ] P3 vs sRGB rendering compared on a real P3 display or DevTools emulation (Rendering > Emulate CSS media feature color-gamut).
