---
id: computing-software.qa-testing-engineering.playwright.full-page-screenshots-stylepath
name: full-page-screenshots-stylepath
category: computing-software
field: qa-testing-engineering
product: playwright
tags: [stylepath, full-page-screenshot, tohavescreenshot, element-screenshot]
level: practitioner
status: docs-checked
description: "Take full-page and element screenshots in Playwright visual tests, inject stylePath CSS to hide volatile UI, set clip and omitBackground, and name snapshots."
sources:
  - https://playwright.dev/docs/test-snapshots
  - https://playwright.dev/docs/api/class-pageassertions
  - https://playwright.dev/docs/api/class-testconfig#test-config-expect
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Full-page and element screenshots, stylePath and animations

## Full page vs viewport vs element
```ts
await expect(page).toHaveScreenshot('home.png', { fullPage: true });           // scrolls the whole document
await expect(page.getByRole('navigation')).toHaveScreenshot('nav.png');         // element only
await expect(page).toHaveScreenshot({ clip: { x: 0, y: 0, width: 800, height: 400 } });
```
Element screenshots cover a smaller area, so fewer unrelated changes can affect them.

## stylePath: hide volatile UI with CSS
```css
/* screenshot.css */
.ad-slot, .chat-widget, [data-volatile] { visibility: hidden !important; }
* { transition: none !important; }
```
```ts
expect: { toHaveScreenshot: { stylePath: path.join(__dirname, 'screenshot.css') } }
```
The stylesheet is applied while the screenshot is made and pierces the Shadow DOM and inner frames. `stylePath` accepts a string or an array of strings. `visibility: hidden` keeps the layout; `display: none` removes the element from it.

## Other options
- `omitBackground: true` hides the default white background for transparent captures (not for jpeg).
- `scale`: for `toHaveScreenshot` it defaults to `'css'` (one pixel per CSS pixel, small images on high-DPI devices); `'device'` gives one pixel per device pixel.
- `animations` defaults to `'disabled'` for `toHaveScreenshot` (finite animations fast-forward to completion, infinite ones reset to their initial state); `caret` defaults to `'hide'`.
- Snapshot names: default from test title + counter; pass explicit names to keep baselines stable when renaming tests. Path controlled by `snapshotPathTemplate`.

## Full-page note
`fullPage` captures the full scrollable page instead of the visible viewport (default `false`). Prefer element screenshots for very tall pages.

## Verify
Running the spec twice in a row produces no diffs, and a deliberate CSS change in one section produces a diff limited to that section.

## Checked

2026-10-25: checked against the Playwright docs (microsoft/playwright main, docs/src, commit of 2026-10-24). Confirmed: fullPage and clip options on toHaveScreenshot, stylePath (string or array, pierces Shadow DOM and inner frames) and its use under expect.toHaveScreenshot in the config, omitBackground, the scale default of css and the animations default of disabled for toHaveScreenshot, and snapshotPathTemplate for snapshot paths. Removed: the sticky-header and lazy-loading remarks and the claim that element screenshots are the most stable, which the docs do not state.

Method: documentation only; no commands were run.
