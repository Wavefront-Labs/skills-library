---
id: computing-software.web-development.web-performance.font-loading-layout-shift
name: font-loading-layout-shift
category: computing-software
field: web-development
product: web-performance
tags: [cls, font-layout-shift, font-display, size-adjust, web-fonts, performance]
level: practitioner
status: docs-checked
description: "Eliminating font-swap layout shift: font-display choices, metric-matched fallbacks with size-adjust and ascent-override, and loading fonts early."
sources:
  - https://web.dev/articles/css-size-adjust
  - https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/size-adjust
  - https://developer.chrome.com/blog/font-fallbacks
  - https://web.dev/articles/font-best-practices
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Font swap layout shift

Layout shifts happen when a web font and its fallback take up different amounts of space (web.dev font-best-practices).

## 1. Choose font-display
- `optional`: block period 100 ms, no swap period. web.dev: no font-swap layout shift, but a late font is not used.
- `swap`: 0 ms block, infinite swap. Text shows fastest; deliver the font early or the late swap is jarring.
- `fallback`: 100 ms block, 3 s swap. `block`: 2-3 s block, infinite swap; the text is drawn invisibly using fallback space, so it can still shift.
- `auto`, `block`, `swap` and `fallback` can all shift when the font is swapped. Combining is fine: `swap` for branding, `optional` for body text.
- Icon fonts shift badly because their fallback looks different; web.dev suggests SVG instead.

## 2. Metric-matched fallback
Use a local font as the fallback face and override its metrics to match the web font:
```css
@font-face {
  font-family: "fallback for Poppins";
  src: local("Arial");
  size-adjust: 60.85099821%;
  ascent-override: 164.3358416%;
  descent-override: 57.51754455%;
  line-gap-override: 16.43358416%;
}
body { font-family: "Poppins", "fallback for Poppins", sans-serif; }
```
(Those numbers are the Chrome article's Poppins-over-Arial example; they depend on both fonts.)
- `size-adjust` scales glyphs and all metrics by the percentage; MDN notes the descriptor makes it easier to harmonize fonts rendered at the same font size.
- Override formulas from the Chrome article: `size-adjust = avgCharacterWidth(web) / avgCharacterWidth(fallback)`; `ascent-override = web ascent / (web UPM * size-adjust)`; the same for descent and line-gap. Without `size-adjust`, the overrides are simply ascent/UPM, descent/UPM and line-gap/UPM. Read the values from the font's tables (fontkit, Capsize, fontdrop.info, FontForge).
- The override values and `size-adjust` change per fallback font, so give each fallback (for example Arial, Roboto) its own `@font-face` and list several, since `local(Arial)` may not exist on every device.
- Cross-platform: for most fonts (about 90% of Google Fonts, per the article) the overrides are the same on every OS; otherwise vary the stylesheet by OS or skip the technique.
- Generators: next/font (Next 13 onward) and `@nuxtjs/fontaine` apply this automatically, Fontaine generates fallbacks, and a repository of Google Fonts overrides exists.
- Browser support (web.dev css-size-adjust): the override descriptors are implemented in Chromium 87+ and Firefox 89+.

## 3. Load faster
Delivering the font early can eliminate swap shift (web.dev). Use WOFF2, subset with `unicode-range`, consider variable fonts if you use many weights, and preload only the most important fonts (preload ignores `unicode-range` and takes resources from others).

## Verify
- [ ] Layout Shifts track in the Performance panel shows no shift when the font loads.

## Checked
2026-11-09. Read the css-size-adjust article, the MDN size-adjust page, the Chrome font-fallbacks article (override, size-adjust and cross-device sections) and font-best-practices (font-display, icon fonts, loading). Removed (not on those pages): the fontaine repository source (not fetched), `@fontsource` metric packages, per-platform `local()` list advice, the `pyftsubset` command, inlining `@font-face` in the head, faux bold or italic remark, the throttling test recipe and the invented sample override values.
Method: documentation only; no commands were run.
