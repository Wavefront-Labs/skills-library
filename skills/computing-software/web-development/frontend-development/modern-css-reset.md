---
id: computing-software.web-development.frontend-development.modern-css-reset
name: modern-css-reset
category: computing-software
field: web-development
product: frontend-development
tags: [modern-css-reset, normalize-css, css-reset, box-sizing, base-styles, css]
level: practitioner
status: docs-checked
description: "A modern CSS reset: what to include (box-sizing, margins, media, form fonts, overflow-wrap), keeping it zero-specificity in a layer, and pitfalls like list semantics in Safari."
sources:
  - https://tailwindcss.com/docs/preflight
  - https://github.com/necolas/normalize.css
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Modern CSS reset

## 1. A sane base
```css
@layer reset {
  *, *::before, *::after { box-sizing: border-box; }
  * { margin: 0; }
  body { min-block-size: 100dvh; line-height: 1.5; }
  img, picture, video, canvas, svg { display: block; max-inline-size: 100%; }
  input, button, textarea, select { font: inherit; color: inherit; }
  p, h1, h2, h3, h4, h5, h6 { overflow-wrap: break-word; }
  h1, h2, h3 { line-height: 1.1; text-wrap: balance; }
  p { text-wrap: pretty; }
  :where(ul, ol)[role="list"] { list-style: none; padding: 0; }
  #root, #__next { isolation: isolate; }
  @media (prefers-reduced-motion: reduce) {
    *, *::before, *::after { animation-duration: .01ms !important; animation-iteration-count: 1 !important;
      transition-duration: .01ms !important; scroll-behavior: auto !important; }
  }
}
@layer reset, base, components, utilities;
```
- Put it in the lowest cascade layer (or use `:where()`), so any later rule overrides it without specificity fights.
- `font: inherit` on controls makes them use the surrounding font instead of the browser default control font.
- `text-wrap: balance` is supported in Chrome 130, Firefox 124 and Safari 17.5; `text-wrap: pretty` in Chrome 130 and Safari 26 (not Firefox), so treat both as progressive enhancement.

## 2. Reset vs normalize
- normalize.css keeps useful defaults and smooths cross-browser inconsistencies.
- A reset removes opinionated defaults so the design system defines them. Tailwind Preflight is a set of base styles built on modern-normalize.

## 3. Pitfalls
- Only remove bullets on lists you mark `role="list"` (as above), not on every list.
- Do not reset `:focus` outlines away.
- `img { display: block }` changes inline images in prose; scope if you have inline icons in text.

## Verify
- [ ] Inputs use the body font; lists marked `role="list"` keep their bullets removed and other lists keep theirs.

## Checked
2026-10-26. Tailwind Preflight docs source, browser-compat-data and MDN pages (main, 2026-10-26): confirmed Preflight is base styles built on modern-normalize, text-wrap balance and pretty support versions, and dvh support (Chrome 108, Firefox 101, Safari 15.4). text-size-adjust is Chromium-only and experimental in browser-compat-data, so the line and its iOS remark were removed, along with the unconfirmed list-semantics, iOS zoom and normalize obsolescence claims. The cascade layer and logical property usage follows the MDN grammar.
Method: documentation only; no commands were run.
