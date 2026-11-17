---
id: computing-software.web-development.responsive-design.testing-responsive-layouts
name: testing-responsive-layouts
category: computing-software
field: web-development
product: responsive-design
tags: [responsive-components, responsive-testing, device-mode, zoom-testing, real-device-testing]
level: practitioner
status: gated
description: "Testing responsive layouts: DevTools device mode limits, testing by width ranges not devices, zoom and text-size checks, real devices, and automated screenshot checks."
sources:
  - https://developer.chrome.com/docs/devtools/device-mode
  - https://www.w3.org/WAI/WCAG22/Understanding/reflow.html
  - https://playwright.dev/docs/emulation
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Testing responsive layouts

## 1. Test ranges, not device names
Drag the viewport continuously from 320px to 2560px in DevTools responsive mode; layouts break **between** breakpoints. Check: 320, 375, 414 (phones), 600-900 (small tablets, split-screen), 1024, 1280, 1440, 1920+.

## 2. What DevTools device mode does and doesn't do
Does: viewport size, DPR, UA string, touch events, `hover/pointer` media features (run with Playwright touch emulation: `(hover: hover)` false, `(pointer: coarse)` true). Doesn't: real mobile browser UI (dynamic toolbars, `100vh`), virtual keyboard, iOS font rendering and form controls, real CPU/GPU, Safari bugs (gated: unconfirmed, source is paywalled or blocked). Treat it as a first pass.

## 3. Zoom and text size
- Browser zoom 200% and 400% at 1280px wide (400% = 320 CSS px, the WCAG 1.4.10 reflow check, per the Understanding page's Note 1): no horizontal scrolling for text content, nothing clipped or overlapping.
- Text-only zoom: Firefox "Zoom text only", Safari/iOS Dynamic Type with `-apple-system-body` or user font size settings, Android font scale 200% - find fixed-height containers that clip text (gated: unconfirmed, source is paywalled or blocked).
- Text spacing bookmarklet (WCAG 1.4.12).

## 4. Real devices
At minimum one current iPhone (Safari), one mid/low-end Android (Chrome), one tablet in both orientations. Use a device cloud otherwise. Check orientation changes, virtual keyboard over forms, safe areas, tap targets.

## 5. Input modes
Touch-only (no hover), keyboard-only, mouse on a touchscreen laptop, stylus. Test `@media (hover: hover)` paths.

## 6. Automate
- Playwright projects per viewport + visual snapshots of key pages at 3 widths.
- A horizontal-overflow assertion: `expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true)`.
- Lighthouse's `meta-viewport` audit (the old "Tap targets" audit file no longer exists on Lighthouse main).

## Verify
Checklist completed per release for key templates; overflow test passes at 320px; zoom 400% walkthrough documented.
