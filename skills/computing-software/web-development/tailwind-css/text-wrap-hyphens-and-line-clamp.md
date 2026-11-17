---
id: computing-software.web-development.tailwind-css.text-wrap-hyphens-and-line-clamp
name: text-wrap-hyphens-and-line-clamp
category: computing-software
field: web-development
product: tailwind-css
tags: [web-fonts, typography, text-wrap-balance, text-wrap-pretty, line-clamp, hyphens, overflow-wrap, truncation, text-overflow-ellipsis]
level: practitioner
status: verified
description: "Controlling text layout: text-wrap balance/pretty for headings and paragraphs, hyphens and overflow-wrap for long words, single and multi-line truncation with line-clamp."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/text-wrap
  - https://developer.mozilla.org/en-US/docs/Web/CSS/line-clamp
  - https://developer.mozilla.org/en-US/docs/Web/CSS/hyphens
  - https://developer.chrome.com/blog/css-text-wrap-pretty
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# text-wrap, hyphens and line clamp

**Goal:** headings without awkward single-word last lines, paragraphs without orphans, long words that don't overflow, and truncation that doesn't hide meaning.

## 1. text-wrap
```css
h1, h2, h3, blockquote { text-wrap: balance; }   /* evens out line lengths; limited to short blocks (six lines in Chromium, ten in Firefox per MDN) */
p, li { text-wrap: pretty; }                        /* avoids orphans/short last lines; slightly slower layout */
```
Both are progressive enhancements (balance: all current engines; pretty: Chromium and Safari 26). Don't use `balance` on long paragraphs (ignored or costly).

## 2. Long words and URLs
```css
.content { overflow-wrap: anywhere; }      /* or break-word: breaks long strings only when needed */
.content { hyphens: auto; }                /* needs lang attribute; quality varies by language */
```
- `overflow-wrap: anywhere` also affects min-content size (fixes flex/grid items blowing out with a long URL); `break-word` doesn't.
- `word-break: break-all` breaks everywhere - only for code/hashes.
- `&shy;` soft hyphens for specific words; `<wbr>` for break opportunities in URLs.

## 3. Truncation
Single line:
```css
.title { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; min-width: 0; }   /* min-width 0 inside flex items */
```
Multi-line:
```css
.excerpt { display: -webkit-box; -webkit-box-orient: vertical; -webkit-line-clamp: 3; line-clamp: 3; overflow: hidden; }
```
(Tailwind: `truncate`, `line-clamp-3`.) The prefixed form is the one that works across browsers today: in Chromium 156 `CSS.supports("line-clamp","3")` is false and `-webkit-line-clamp: 3` clamped a paragraph to exactly three 20px lines (60px). Tailwind 4.3.3 `line-clamp-3` emits `overflow: hidden; display: -webkit-box; -webkit-box-orient: vertical; -webkit-line-clamp: 3` and `truncate` emits the single-line trio. In a flex row, `overflow-wrap: anywhere` kept a 120-character URL at its 300px container while `break-word` let the item grow to about 989px (run).

## 4. Accessibility of truncation
Truncated text is still fully in the DOM (screen readers read it all - fine). Sighted users lose it: provide the full text via a link/expand control, not only a `title` tooltip (not keyboard/touch accessible). Never truncate critical info (prices, error messages). At 200% zoom/reflow, check truncation doesn't hide essentials.

## Verify
- [ ] Headings wrap evenly at various widths; no single-word orphans in body text.
- [ ] A 200-character URL doesn't cause horizontal scroll on mobile.
- [ ] Truncated content has an accessible way to read it in full.
