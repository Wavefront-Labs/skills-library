---
id: computing-software.qa-testing-engineering.playwright.chrome-extension-testing
name: chrome-extension-testing
category: computing-software
field: qa-testing-engineering
product: playwright
tags: [chrome-extension-testing, persistent-context, launchpersistentcontext, manifest-v3]
level: practitioner
status: docs-checked
description: "Test Chrome (Manifest V3) extensions with Playwright via launchPersistentContext, load-extension args, finding the extension id from the service worker and opening popup pages."
sources:
  - https://playwright.dev/docs/chrome-extensions
  - https://playwright.dev/docs/api/class-browsertype
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Testing Chrome extensions with a persistent context

**Goal:** load an unpacked extension in Chromium and test its popup, options page and content scripts.

## Fixture
```ts
import { test as base, chromium, type BrowserContext } from '@playwright/test';
import path from 'path';

export const test = base.extend<{ context: BrowserContext; extensionId: string }>({
  context: async ({}, use) => {
    const pathToExtension = path.join(__dirname, '../dist');
    const context = await chromium.launchPersistentContext('', {
      channel: 'chromium',
      args: [`--disable-extensions-except=${pathToExtension}`, `--load-extension=${pathToExtension}`],
    });
    await use(context);
    await context.close();
  },
  extensionId: async ({ context }, use) => {
    let [sw] = context.serviceWorkers();
    if (!sw) sw = await context.waitForEvent('serviceworker');
    await use(sw.url().split('/')[2]);
  },
});
```

## Tests
```ts
test('popup', async ({ page, extensionId }) => {
  await page.goto(`chrome-extension://${extensionId}/popup.html`);
  await expect(page.getByRole('heading')).toHaveText('My Extension');
});
test('content script', async ({ page }) => {
  await page.goto('https://example.com');
  await expect(page.locator('#my-ext-banner')).toBeVisible();
});
```

## Notes
- Extensions need Chromium (`channel: 'chromium'` supports headless with extensions); Google Chrome / Edge branded builds removed side-loading flags.
- An empty string as `userDataDir` creates a temporary directory.
- Open the popup page by its `chrome-extension://<id>/popup.html` URL in a normal page, as the docs do.
- Background code: test the service worker like any other worker with `sw.evaluate(...)`.

## Gotchas
- Build the extension before tests (`globalSetup` or npm script); stale `dist/` gives confusing results.
- MV3 service workers are suspended after about 30 seconds of inactivity and restarted on demand; the docs say Playwright keeps the same Worker object, emits no new `serviceworker` event, and stalls `evaluate()` calls issued during the restart until it is ready.

## Verify
`extensionId` resolves and the popup page renders under test.

## Checked

2026-10-25: checked against the Playwright docs (microsoft/playwright main, docs/src, commit of 2026-10-24). Confirmed: extensions load only in Chromium with a persistent context, the chromium channel allowing headless runs, Chrome and Edge having removed the side-loading flags, the --disable-extensions-except and --load-extension args, the service worker lookup with waitForEvent, the extension-id fixture and chrome-extension URL for popup pages, an empty userDataDir giving a temporary directory, and the MV3 idle suspension behaviour. Removed: the toolbar popup claim.

Method: documentation only; no commands were run.
