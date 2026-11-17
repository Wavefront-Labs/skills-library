---
id: computing-software.web-development.frontend-development.ios-safari-and-webkit-quirks
name: ios-safari-and-webkit-quirks
category: computing-software
field: web-development
product: frontend-development
tags: [cross-browser, ios-safari-quirks, viewport-units, compatibility]
level: practitioner
status: docs-checked
description: "Handling mobile browser toolbars and device notches in CSS: svh, lvh and dvh viewport units, and env() safe-area insets that originated on iOS."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/length
  - https://developer.mozilla.org/en-US/docs/Web/CSS/env
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# iOS Safari and WebKit quirks

Scope of what the cited MDN pages confirm: viewport units under dynamic browser toolbars, and safe-area insets.

## 1. Viewport height under dynamic toolbars
- Browser interfaces expand and retract, so CSS defines four viewport sizes: small, large, dynamic and default.
- Units: `svh`/`svw` (small), `lvh`/`lvw` (large), `dvh`/`dvw` (dynamic). Plain `vh` is equivalent to `lvh`: all default viewport units currently equal their large counterparts.
- Large viewport: content fills the screen when browser interfaces retract, but may be hidden when they expand. A full-page `100vh` can therefore be obscured while the interface is expanded.
- Small viewport: fills the screen when interfaces are expanded, and may leave empty space when they retract.
- Dynamic viewport: fits exactly irrespective of dynamic interfaces, but its units are not stable even when the viewport is unchanged, so content can resize while the user scrolls, degrading the UI and costing performance.
```css
.hero { min-height: 100vh; min-height: 100svh; } /* svh: content never covered by expanded toolbars */
```

## 2. Safe areas
- `env(safe-area-inset-top|right|bottom|left)` was originally provided by the iOS browser so content is not obscured by notches or rounded corners; it was later extended to uses such as notifications covering UI.
- The second argument is a fallback used when the variable is unsupported or does not exist. Variable names are case-sensitive.
- Example from MDN for a sticky footer: `padding: 1em 1em calc(1em + env(safe-area-inset-bottom));`. On desktop the bottom inset is 0.
- `safe-area-max-inset-*` are the static maximums when all dynamic UI is retracted.

## Verify
Check full-height layouts and fixed bars on a real device with toolbars expanded and retracted.

## Checked
Method: docs-only read on 2026-11-09 of MDN CSS length (viewport-percentage lengths section) and CSS env() pages via text extraction. Dropped sources: webkit.org blog (landing page) and Apple Safari release notes (excluded domain). Removed as unstated on the pages: input zoom under 16px, virtual keyboard and visualViewport advice, date input notes, autoplay, hover stickiness, scroll lock, the viewport-fit=cover meta tag, ITP storage limits, and the tags webkit-quirks and mobile-safari.
