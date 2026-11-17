---
id: computing-software.qa-testing-engineering.playwright.framelocator-and-iframes
name: framelocator-and-iframes
category: computing-software
field: qa-testing-engineering
product: playwright
tags: [framelocator, iframes, content-frame, playwright-locators]
level: practitioner
status: verified
description: "Locate and assert inside iframes with Playwright frameLocator and contentFrame, including nested frames, payment widgets and cross-origin frames."
sources:
  - https://playwright.dev/docs/api/class-framelocator
  - https://playwright.dev/docs/frames
  - https://playwright.dev/docs/api/class-locator#locator-content-frame
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# frameLocator and iframes

**Goal:** interact with embedded content (payment fields, rich editors, third-party widgets) reliably.

## frameLocator (auto-waiting, preferred)
```ts
const card = page.frameLocator('iframe[title="Secure card payment input frame"]');
await card.getByPlaceholder('Card number').fill('4242424242424242');
await card.getByPlaceholder('MM / YY').fill('12/34');
```
Nested: `page.frameLocator('#outer').frameLocator('#inner').getByRole('button')`.

From an existing locator (newer API):
```ts
const frame = page.getByTitle('Editor').contentFrame();
await frame.getByRole('textbox').fill('Hello');
```
And back: `frame.owner()` (a `FrameLocator` method) returns the `<iframe>` element locator (run here: count 1; assert size/visibility). `locator.contentFrame()` needs v1.43+.

## Frame objects (non-auto-waiting)
```ts
const f = page.frame({ url: /stripe\.com/ });  // or { name: 'checkout' }
for (const fr of page.frames()) console.log(fr.url());
```
Use for evaluating scripts in a frame; prefer locators for interactions.

## Cross-origin
Playwright handles cross-origin iframes natively (no `chromeWebSecurity` style flags). Run here: a page on `localhost` embedding an iframe from `127.0.0.1` was filled and asserted through `frameLocator`, and a `page.route` fulfil applied to a fetch made inside that iframe.

## Gotchas
- Pick iframes by stable `title` or `name`; `iframe >> nth=0` breaks when ads or chat widgets load.
- Strictness applies: two matching iframes throw when you act inside them (run here: `strict mode violation: locator('iframe[title="Editor"]') resolved to 2 elements`).
- Payment providers rotate selectors and may block automation in live mode: use their test mode keys and documented test cards.
- `page.frames()` returns the frames at the moment of the call; call it again after navigation inside a frame.

## Verify
Trace viewer shows actions targeting the frame; assertions inside the frame (`toHaveValue`) pass.
