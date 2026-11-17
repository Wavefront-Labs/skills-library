---
id: computing-software.qa-testing-engineering.test-case-design.responsive-and-mobile-web-testing
name: responsive-and-mobile-web-testing
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [responsive-testing, mobile-web-testing, compatibility-testing, viewport-testing, device-emulation, touch-events]
level: practitioner
status: docs-checked
description: "Test responsive layouts and mobile web: breakpoint coverage, device emulation vs real devices, touch, orientation, virtual keyboard and mobile network conditions."
sources:
  - https://playwright.dev/docs/emulation
  - https://developer.chrome.com/docs/devtools/device-mode
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Responsive and mobile web testing

**Goal:** layouts and interactions work across viewport sizes and mobile browsers.

## Breakpoint coverage
- Test at each CSS breakpoint and **one pixel either side** (e.g. 767/768/769 if breakpoint is 768): boundary value analysis for layout.
- Plus the common device widths in your own analytics.
- Check: navigation collapse/expand, overflowing tables, text truncation, images scaling, sticky headers covering content, modals fitting the viewport.

## Emulation
```ts
// Playwright
import { devices } from '@playwright/test'
projects: [{ name: 'Mobile Safari', use: { ...devices['iPhone 13'] } }]
```
A Playwright device descriptor sets user agent, screen size, viewport and whether touch is enabled. Chrome DevTools device mode simulates a mobile viewport and throttles CPU and network for manual checks.

## Real-device checks (emulation misses these)
Virtual keyboard covering inputs, browser toolbar changes altering the viewport height, touch precision on small targets (check platform and WCAG target-size guidance), pinch zoom not disabled, orientation change mid-form, OS font scaling.

## Gotchas
- Hover-only interactions are unreachable on touch devices.

## Verify
Screenshot sets at each breakpoint reviewed (or visual regression baselines), and a real-device pass on the tier 1 mobile browsers each release.

## Checked

- Date: 2026-10-28
- Confirmed: Playwright device descriptors (userAgent, screen size, viewport, hasTouch) and the devices['iPhone 13'] project form; Chrome DevTools device mode simulates a mobile viewport and throttles CPU and network.
- Removed: the list of device widths, iPhone 15 and Pixel 7 descriptors, deviceScaleFactor and isMobile remarks, the Firefox isMobile claim, 100vh/100dvh, 44x44 and 24x24 target sizes.

Method: documentation only; no commands were run.
