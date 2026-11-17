---
id: computing-software.qa-testing-engineering.playwright.console-and-page-error-capture
name: console-and-page-error-capture
category: computing-software
field: qa-testing-engineering
product: playwright
tags: [page-console-events, pageerror, requestfailed, playwright-debugging, test-attachments]
level: practitioner
status: verified
description: "Capture browser console messages, uncaught page errors and failed requests in Playwright, attach them to the report and optionally fail tests on them."
sources:
  - https://playwright.dev/docs/api/class-page#page-event-console
  - https://playwright.dev/docs/api/class-page#page-event-page-error
  - https://playwright.dev/docs/api/class-testinfo#test-info-attach
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Capturing console messages, page errors and network logs

**Goal:** front-end errors visible in test output, not lost in a browser nobody watched.

## Listeners
```ts
page.on('console', msg => { if (msg.type() === 'error') console.log(`[console] ${msg.text()} @ ${msg.location().url}`); });
page.on('pageerror', err => console.log(`[pageerror] ${err.message}\n${err.stack}`));
page.on('requestfailed', req => console.log(`[requestfailed] ${req.method()} ${req.url()} ${req.failure()?.errorText}`));
page.on('response', res => { if (res.status() >= 500) console.log(`[5xx] ${res.status()} ${res.url()}`); });
```
Newer API to read history without pre-registering: `page.consoleMessages()`, `page.pageErrors()` (added in v1.56; run here on 1.64 they returned 4 messages and 1 error for the test page).

## Attach to the report
```ts
test.afterEach(async ({}, testInfo) => {
  if (logs.length) await testInfo.attach('browser-log', { body: logs.join('\n'), contentType: 'text/plain' });
});
```
Better as an auto fixture so every test gets it.

## Waiting for a specific message
```ts
const msgPromise = page.waitForEvent('console', m => m.text().includes('ready'));
await page.goto('/');
await msgPromise;
```

## Failing on errors (policy)
Fail on `pageerror` (uncaught exceptions are almost always bugs). For `console.error`, keep an allowlist of known noise (third-party scripts, React dev warnings) and fail on the rest.

## Gotchas
- Register listeners **before** `goto`, or early errors are missed.
- Run here: a failing `fetch` and a 404 each produced a `requestfailed`/`response` event and also a `console` error (`Failed to load resource: ...`), so a `console.error` policy sees network noise; `net::ERR_UNSAFE_PORT` was the failure text for port 1.
- `msg.args()` are JSHandles; `msg.text()` is usually enough.
- Service worker and worker console output arrive via `context.on('console')` / `worker.on('console')`.
- The trace viewer Console tab already shows these; listeners help when traces are off.

## Verify
Inject `setTimeout(() => { throw new Error('boom') })` in a test page; the test log/report shows it (and fails if the policy is on).
