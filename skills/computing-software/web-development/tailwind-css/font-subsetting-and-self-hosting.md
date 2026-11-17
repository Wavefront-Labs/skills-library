---
id: computing-software.web-development.tailwind-css.font-subsetting-and-self-hosting
name: font-subsetting-and-self-hosting
category: computing-software
field: web-development
product: tailwind-css
tags: [web-fonts, typography, font-subsetting, self-hosted-fonts, unicode-range, pyftsubset, glyphhanger, woff2, font-preload]
level: practitioner
status: docs-checked
description: "Self-hosting and subsetting web fonts: WOFF2 conversion, unicode-range splitting, pyftsubset/glyphhanger, preloading the critical file, caching and licensing checks."
sources:
  - https://web.dev/learn/performance/optimize-web-fonts
  - https://fonttools.readthedocs.io/en/latest/subset/
  - https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/unicode-range
  - https://github.com/zachleat/glyphhanger
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Font subsetting and self-hosting

**Goal:** fonts load from your origin, contain only the glyphs you need, and the critical one starts downloading immediately.

## 1. Why self-host
A third-party font service makes the page open a connection to the provider's domain before fonts download, which can delay discovery. In most cases self-hosting is faster than cross-origin downloads; use a CDN, HTTP/2 or HTTP/3 and correct caching headers. Check the font licence allows web self-hosting (OFL fonts do).

## 2. Subset and convert
```bash
pip install fonttools brotli
pyftsubset Inter.ttf --output-file=inter-latin.woff2 --flavor=woff2 \
  --unicodes="U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+2074,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD" \
  --layout-features='kern,liga,calt,tnum' --no-hinting
```
- `--flavor=woff2` needs the Brotli Python extension (`pip install brotli`).
- Keep OpenType features you use (`tnum` tabular numbers, `ss01` stylistic sets); dropping them silently changes rendering.
- glyphhanger finds the unicode-ranges used on a site and can subset fonts automatically (`glyphhanger URL --subset="*.ttf"`); careful with user-generated content - you'll need fallback ranges.

## 3. unicode-range splitting
```css
@font-face { font-family: Inter; src: url(/fonts/inter-latin.woff2) format("woff2"); unicode-range: U+0000-00FF, U+2000-206F, U+20AC; font-display: swap; }
@font-face { font-family: Inter; src: url(/fonts/inter-cyrillic.woff2) format("woff2"); unicode-range: U+0400-045F, U+0490-0491; font-display: swap; }
```
If the page uses no character in a range, that font is not downloaded; if it uses at least one, the whole file is downloaded.

## 4. Load it early
```html
<link rel="preload" href="/fonts/inter-latin.woff2" as="font" type="font/woff2" crossorigin>
```
`crossorigin` is required even for self-hosted fonts (fonts are CORS resources). Preload only the files used above the fold and serve them with long-lived caching headers.

## 5. Fallback metrics
Reduce swap CLS with `size-adjust`, `ascent-override`, `descent-override` on a local fallback `@font-face` .

## Verify
- [ ] Network: font requests same-origin, WOFF2, small, preloaded one starts in the first round trip.
- [ ] Rendering unchanged (ligatures, tabular numbers) after subsetting.
- [ ] Characters outside the subset (e.g. names with diacritics) still render via the right range or fallback.

## Checked
2026-10-31. Confirmed against web.dev optimize-web-fonts, the fonttools subset docs, MDN unicode-range and the glyphhanger README: self-hosting rationale, crossorigin on font preloads, --flavor=woff2 needing Brotli, --no-hinting, --layout-features, unicode-range download behaviour, glyphhanger subsetting, size-adjust/ascent-override/descent-override (web.dev optimize-cls). Removed: cache-partitioning and EU ruling claims, KB size figures, tool names, specific Cache-Control value.
Method: documentation only; no commands were run.
