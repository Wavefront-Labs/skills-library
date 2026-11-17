---
id: computing-software.qa-testing-engineering.playwright.downloads-dialogs-and-popups
name: downloads-dialogs-and-popups
category: computing-software
field: qa-testing-engineering
product: playwright
tags: [playwright-downloads, playwright-dialogs, popups, new-page, file-download-testing]
level: practitioner
status: verified
description: "Handle downloads, alert/confirm/prompt dialogs, popups and new tabs in Playwright: waitForEvent patterns, saving files, asserting content and dialog auto-dismissal."
sources:
  - https://playwright.dev/docs/downloads
  - https://playwright.dev/docs/dialogs
  - https://playwright.dev/docs/pages#handling-popups
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Downloads, dialogs and popups

## Downloads
```ts
const downloadPromise = page.waitForEvent('download');
await page.getByRole('link', { name: 'Export CSV' }).click();
const download = await downloadPromise;
expect(download.suggestedFilename()).toMatch(/^orders-\d{4}-\d{2}-\d{2}\.csv$/);
const file = testInfo.outputPath(download.suggestedFilename());
await download.saveAs(file);
const csv = await fs.promises.readFile(file, 'utf8');
expect(csv.split('\n')[0]).toBe('id,date,total');
```
`download.failure()` returns an error string for failed downloads (`null` on success, as seen here). Files are deleted when the context closes unless saved.

## Dialogs
By default Playwright **auto-dismisses** dialogs (run here: a `confirm()` returned `false` with no listener, `true` after `d.accept()`) (alert/confirm/prompt -> dismiss). Register a handler before the action:
```ts
page.once('dialog', async d => {
  expect(d.type()).toBe('confirm');
  expect(d.message()).toContain('Delete');
  await d.accept();           // d.accept('text') for prompt
});
await page.getByRole('button', { name: 'Delete' }).click();
```
`beforeunload` dialogs are handled with a `dialog` listener too (`dialog.type()` is `'beforeunload'`); `page.close({ runBeforeUnload: true })` is the documented way to run unload handlers on close (the only case where `close` may not wait for the page to close). Run here: a `page.reload()` on a page with a `beforeunload` handler (after a click on the page) also raised a `beforeunload` dialog, so register the handler before such navigations.

## Popups and new tabs
```ts
const popupPromise = page.waitForEvent('popup');
await page.getByRole('link', { name: 'Open invoice' }).click();
const popup = await popupPromise;
await popup.waitForLoadState();
await expect(popup).toHaveURL(/invoice/);
```
Any new page in the context: `context.waitForEvent('page')`.

## Gotchas
- `page.on('dialog')` handlers that never accept/dismiss make the page hang.
- `acceptDownloads` defaults to `true`. A response without `Content-Disposition: attachment` (for example a PDF the browser can display) may not raise a `download` event; assert on the response then (not tested here).
- `target=_blank` links: assert `href` instead of opening, when the destination is external.

## Verify
Downloaded file content assertions pass in CI (headless) as well as locally.
