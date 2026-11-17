---
id: creative-arts.graphic-design.typography.web-font-loading-and-font-display
name: web-font-loading-and-font-display
category: creative-arts
field: graphic-design
product: typography
tags: [graphic-design, typography, web-typography, screen-typography, font-loading, font-display, woff2, preload, font-face, size-adjust, fallback-fonts, cls, subsetting]
level: practitioner
status: draft
description: "Load web fonts fast without layout shift: @font-face with WOFF2, font-display choices, preloading key files, subsetting, and size-adjust fallbacks that match metrics."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/font-display
  - https://web.dev/articles/font-best-practices
  - https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/size-adjust
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Web font loading and font-display

**Goal:** brand fonts on the web that appear quickly, do not hide text, and do not make the page jump.

## @font-face basics
```css
@font-face {
  font-family: "Brand Sans";
  src: url("/fonts/brand-sans-var.woff2") format("woff2");
  font-weight: 100 900;          /* variable font range */
  font-style: normal;
  font-display: swap;
  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+2000-206F; /* Latin subset */
}
```
- Serve **WOFF2** only for modern browsers (best compression). Self-host or use a CDN; check the licence
  allows web use and self-hosting (see font-licensing skill).
- One variable font often replaces 4-8 static files.

## font-display values
| Value | Block period | Swap period | Use |
|---|---|---|---|
| `auto` | browser default (~3 s block) | | avoid |
| `block` | ~3 s invisible text | infinite | icon fonts only |
| `swap` | ~0-100 ms | infinite | brand headings and body where the font matters |
| `fallback` | ~100 ms | ~3 s, then fallback stays | body text on slow networks |
| `optional` | ~100 ms | none: font used only if cached/fast | performance-first sites |

## Speed
- `<link rel="preload" href="/fonts/brand-sans-var.woff2" as="font" type="font/woff2" crossorigin>` for the
  1-2 fonts used above the fold. Preloading many fonts slows everything.
- Subset to the languages you need (pyftsubset from fonttools, or the foundry's subsetting) and split with
  `unicode-range`.
- Cache with long `Cache-Control` and versioned file names.

## Avoid layout shift (CLS)
- Define a fallback face with adjusted metrics so the swap does not reflow:
```css
@font-face { font-family: "Brand Fallback"; src: local("Arial");
  size-adjust: 104%; ascent-override: 92%; descent-override: 24%; line-gap-override: 0%; }
body { font-family: "Brand Sans", "Brand Fallback", sans-serif; }
```
  Tools such as Fontaine or Next.js `next/font` compute these overrides automatically.

## Gotchas
- `crossorigin` is required on font preloads even from the same origin, or the file downloads twice.
- Fonts declared but not used in visible text are not downloaded; preload forces it.
- Google Fonts CSS URLs accept `&display=swap`.
- Invisible text (FOIT) for 3 seconds on slow connections is the real cost of `block` and `auto`.

## Verify
- [ ] Lighthouse: no "Ensure text remains visible during webfont load" warning; CLS under 0.1.
- [ ] Network panel: only WOFF2 files, preloaded ones requested once.
