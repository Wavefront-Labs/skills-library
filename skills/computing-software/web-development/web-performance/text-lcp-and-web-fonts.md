---
id: computing-software.web-development.web-performance.text-lcp-and-web-fonts
name: text-lcp-and-web-fonts
category: computing-software
field: web-development
product: web-performance
tags: [text-lcp, web-fonts, font-display, lcp, largest-contentful-paint]
level: practitioner
status: docs-checked
description: "Optimising LCP when the largest element is text: how font loading delays it, font-display choices, preloading fonts, WOFF2 and subsetting, and server rendering."
sources:
  - https://web.dev/articles/optimize-lcp
  - https://web.dev/articles/font-best-practices
  - https://developer.chrome.com/blog/font-fallbacks
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Text LCP and web fonts

When the LCP element is a text node that needs a web font, the font is an LCP resource: it must be discoverable early and must not block text display.

## 1. How fonts affect text LCP
- Default browser behaviour (web.dev): Chromium-based browsers and Firefox block text rendering for up to 3 seconds if the web font has not loaded; Safari blocks indefinitely. `font-display` changes this, and it can affect LCP, FCP and layout stability.
- web.dev (optimize-lcp): with a `font-display` value other than `auto` or `block`, text is always visible during load and LCP is not blocked on an additional network request.
- Periods per value: `block` 2-3 s block then infinite swap; `swap` 0 ms block then infinite swap; `fallback` 100 ms block then 3 s swap; `optional` 100 ms block and no swap period; `auto` varies by browser.

## 2. Recipe
```html
<link rel="preload" href="/fonts/brand.woff2" as="font" type="font/woff2" crossorigin>
<style>
@font-face { font-family: "Brand"; src: url(/fonts/brand.woff2) format("woff2"); font-display: swap; }
h1, body { font-family: "Brand", "Brand Fallback", sans-serif; }
</style>
```
- Discovery: a text LCP that needs a web font is discoverable from the HTML when the font is preloaded with `<link rel="preload">` or a `Link` header. With external stylesheets, preloading the most important fonts can be very effective since the browser otherwise discovers the font much later.
- Preload caution (font-best-practices): it takes browser resources from other resources and ignores `unicode-range`, so use it prudently, for a single font format.
- Fonts must be fetched over CORS, so a font preload (and a preconnect for the font file's origin) needs the `crossorigin` attribute.
- Third-party font host: use `preconnect` for the stylesheet origin and a separate `crossorigin` preconnect for the font file origin (for Google Fonts, `fonts.googleapis.com` and `fonts.gstatic.com`).
- Self-hosting removes the third-party connection in theory, but web.dev says the real difference is less clear-cut; it advises confirming a CDN and HTTP/2 first, and measuring.
- Use WOFF2 only (best support and compression, about 30% better than WOFF per web.dev); subset with `unicode-range` and tools such as subfont or glyphhanger; variable fonts can replace several files but are larger than a single static style.
- Font-display choice: `optional` is the most performant (text delayed at most 100 ms, no swap-related shift, but a late font is not used); `swap` shows text quickly but shifts if the font arrives late; `block` delays initial text. `swap` can be used for branding and `optional` for body text.

## 3. Reduce the swap shift
Metric-adjusted fallback fonts (`size-adjust`, `ascent-override`, `descent-override`, `line-gap-override` on an `@font-face` with `src: local(...)`) make the fallback match the web font's dimensions; see the Chrome font-fallbacks article. Tools such as next/font, `@nuxtjs/fontaine` and Fontaine generate them.

## 4. Other text-LCP delays (optimize-lcp)
- Render delay: large render-blocking stylesheets, synchronous scripts in the head, an element not yet in the DOM, an A/B-testing library hiding it, long main-thread tasks.
- Client-side rendering: server-side rendering or prerendering makes content available without extra JavaScript requests (SSR can raise TTFB).

## Verify
- [ ] In the network waterfall the font starts loading with the first resources, and the Performance panel LCP element matches the intended text.

## Checked
2026-11-09. Read optimize-lcp in full, the web-vitals-adjacent font-best-practices sections (preconnect, preload, self-hosting, WOFF2, subsetting, variable fonts, font-display) and the Chrome font-fallbacks article (override sections). Removed (not on those pages): the claim that swapped fallback text counts as LCP and does not create a new entry, the 200 ms and 0.01 verification thresholds, the W3C LCP spec source (not fetched), the sample metric values and unicode-range list, and the `lcpEntry.element` attribution tip.
Method: documentation only; no commands were run.
