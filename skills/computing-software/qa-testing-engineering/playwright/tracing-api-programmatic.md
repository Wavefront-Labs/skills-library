---
id: computing-software.qa-testing-engineering.playwright.tracing-api-programmatic
name: tracing-api-programmatic
category: computing-software
field: qa-testing-engineering
product: playwright
tags: [context-tracing, trace-viewer, tracing-chunks, library-mode]
level: practitioner
status: docs-checked
description: "Record Playwright traces programmatically with context.tracing start/stop and chunks (library mode, long tests, Python), and open them in trace.playwright.dev."
sources:
  - https://playwright.dev/docs/api/class-tracing
  - https://playwright.dev/docs/trace-viewer
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Recording traces programmatically

**Goal:** traces where the test runner's `trace` option does not reach: library-mode scripts, Python without pytest-playwright, or only part of a long test.

## Start/stop
```ts
const context = await browser.newContext();
await context.tracing.start({ screenshots: true, snapshots: true, sources: true, title: 'checkout' });   // title is shown in the viewer
const page = await context.newPage();
// ... steps
await context.tracing.stop({ path: 'traces/checkout.zip' });
```
Python:
```python
context.tracing.start(screenshots=True, snapshots=True, sources=True)
...
context.tracing.stop(path="trace.zip")
```

## Chunks: one trace per phase
```ts
await context.tracing.start({ screenshots: true, snapshots: true });
await context.tracing.startChunk({ title: 'login' });
// login
await context.tracing.stopChunk({ path: 'login.zip' });
await context.tracing.startChunk({ title: 'pay' });
// pay
await context.tracing.stopChunk({ path: 'pay.zip' });
await context.tracing.stop();
```
Calling `stopChunk()` without a path discards the chunk (as does disposing the object returned by `startChunk()`), so you can keep only failing chunks.

## Groups
`await context.tracing.group('Add to cart'); ... await context.tracing.groupEnd();` groups the actions between the two calls under a label in the trace.

## Viewing
`npx playwright show-trace trace.zip` or drop it on https://trace.playwright.dev, which loads the trace entirely in your browser and does not transmit data externally.

## Gotchas
- `snapshots` captures complete DOM snapshots for each action, so traces grow with the number of actions; for long scripts split them into chunks.
- `sources: true` includes source files in the trace; do not share traces of private code publicly.
- Tracing is started per browser context (`context.tracing`); a new context needs its own `start()`.
- Traces record page content and network activity: treat them as sensitive artifacts.

## Verify
The zip opens with actions, network, console and source tabs populated.

## Checked

2026-10-25: checked against the Playwright docs (microsoft/playwright main, docs/src, commit of 2026-10-24). Confirmed: tracing.start options screenshots, snapshots, sources and title, stop with a path, startChunk and stopChunk with and without a path, group and groupEnd, the Python start and stop signatures, and trace.playwright.dev loading traces in the browser without transmitting data. Reworded the trace-size note to match the snapshots description.

Method: documentation only; no commands were run.
