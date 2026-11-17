---
id: computing-software.qa-testing-engineering.playwright.waiting-for-requests-and-responses
name: waiting-for-requests-and-responses
category: computing-software
field: qa-testing-engineering
product: playwright
tags: [waitforresponse, waitforrequest, playwright-network, network-synchronization]
level: practitioner
status: docs-checked
description: "Synchronise Playwright tests on network traffic with waitForResponse/waitForRequest, assert on payloads, and avoid the race of starting the wait after the click."
sources:
  - https://playwright.dev/docs/network
  - https://playwright.dev/docs/api/class-page
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Waiting for requests and responses

**Goal:** wait for the exact backend call a UI action triggers and assert on it.

## Pattern: start waiting before acting
```ts
const responsePromise = page.waitForResponse(r =>
  r.url().includes('/api/orders') && r.request().method() === 'POST');
await page.getByRole('button', { name: 'Place order' }).click();
const response = await responsePromise;
expect(response.status()).toBe(201);
expect(await response.json()).toMatchObject({ status: 'pending' });
```
Create the promise before the click and await it afterwards; starting to wait only after the action can miss a response that has already arrived.

## Request assertions
```ts
const reqPromise = page.waitForRequest('**/api/search?**');
await page.getByRole('searchbox').fill('mug');
const req = await reqPromise;
expect(new URL(req.url()).searchParams.get('q')).toBe('mug');
expect(req.postDataJSON()).toEqual({ ... });     // for POST bodies
expect(await req.allHeaders()).toHaveProperty('authorization');
```

## Matchers
A glob string (`'**/api/orders'`), a RegExp, or a predicate function. In glob patterns `?` matches only a literal question mark (use `*` for any character) and `{}` matches a comma-separated list of options.

## Events for logging
`page.on('request')`, `page.on('response')`, `page.on('requestfinished')`, `page.on('requestfailed')`.

## Gotchas
- Prefer asserting the UI result; wait on network only when the UI gives no signal or the payload is the thing under test.
- `'networkidle'` (for `waitUntil` and `waitForLoadState`) is marked DISCOURAGED in the docs; do not use it for testing and rely on web assertions to assess readiness.
- If network events are missing, a service worker (for example Mock Service Worker) may be taking over requests; set `serviceWorkers: 'block'`.

## Verify
With the backend slowed (a `route` that delays the response) and without the delay, the test passes both times.

## Checked

2026-10-25: checked against the Playwright docs (microsoft/playwright main, docs/src, commit of 2026-10-24). Confirmed: waitForResponse and waitForRequest taking a glob, RegExp or predicate, creating the promise before the action, Request methods postDataJSON, allHeaders, method and url, the page events request, response, requestfinished and requestfailed, glob rules (? is literal, {} lists), networkidle being discouraged, and serviceWorkers block for missing network events. Removed: the claim about async predicates and the claim that glob behaviour changed in recent versions.

Method: documentation only; no commands were run.
