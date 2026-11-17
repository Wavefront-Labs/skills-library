---
id: creative-arts.design-for-form-and-experience.design-systems.loading-web-fonts-without-layout-shift
name: loading-web-fonts-without-layout-shift
category: creative-arts
field: design-for-form-and-experience
product: design-systems
tags: [font-loading, web-font-loading, font-display, font-preload, font-subsetting, cumulative-layout-shift]
level: practitioner
status: draft
description: "Load web fonts fast and stable: WOFF2, font-display, preload, subsetting, variable fonts and fallback metrics to limit layout shift."
sources:
  - "MDN Web Docs, @font-face and font-display (developer.mozilla.org)"
  - "web.dev (web.dev) performance guidance on web fonts"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Web font loading strategy

Goal: show text quickly, avoid layout shift when the font arrives, and keep font bytes low.

## Steps
1. **Format:** serve WOFF2 (broadly supported and compressed).
2. **Self-host** where licences allow, to avoid third-party connection cost and gain caching control.
3. **`font-display`** in `@font-face`:
   - `swap`: show fallback immediately then swap (can cause visible shift).
   - `fallback`: short block period, short swap window.
   - `optional`: use the font only if it loads very quickly, otherwise stay with the fallback; the least shift.
   - `block`: invisible text for a period (avoid for body text).
4. **Preload** the one or two critical fonts: `<link rel="preload" as="font" type="font/woff2" href="/fonts/x.woff2" crossorigin>` (the `crossorigin` attribute is required for fonts).
5. **Subset** to the needed character sets and use `unicode-range` so scripts are loaded on demand.
6. **Use a variable font** when you need several weights; it can be smaller than several static files.
7. **Match the fallback metrics** to reduce shift: define a local fallback `@font-face` with `size-adjust`, `ascent-override`, `descent-override` and `line-gap-override` so the fallback occupies the same space (tools that compute the values exist).
8. **Limit weights and styles** actually used.
9. **Measure:** check Cumulative Layout Shift and Largest Contentful Paint in Lighthouse or field data; test on slow connections.

## Verify
- [ ] Only needed font files load, in WOFF2.
- [ ] No visible jump when the font swaps.
- [ ] Critical fonts are preloaded with crossorigin.
