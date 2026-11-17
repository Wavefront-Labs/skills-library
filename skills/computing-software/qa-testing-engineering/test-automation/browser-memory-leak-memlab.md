---
id: computing-software.qa-testing-engineering.test-automation.browser-memory-leak-memlab
name: browser-memory-leak-memlab
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [memlab, browser-memory-leak, dynamic-analysis, heap-snapshot, detached-dom, chrome-devtools, spa-testing]
level: practitioner
status: draft
description: "Find memory leaks in single-page apps with Chrome DevTools heap snapshots and Meta's memlab: detached DOM nodes, retained listeners and growth per navigation."
sources:
  - https://facebook.github.io/memlab/
  - https://developer.chrome.com/docs/devtools/memory-problems
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Browser memory leak testing (DevTools, memlab)

**Goal:** single-page apps do not grow memory with every navigation or open/close cycle.

## Manual (Chrome DevTools)
1. Memory panel, take heap snapshot (baseline).
2. Perform the action cycle several times (open modal and close it, navigate to page and back).
3. Click the garbage icon (force GC), take another snapshot.
4. Comparison view: look for growing counts of `Detached HTMLDivElement`, your component classes, closures, event listeners. Retainers panel shows what keeps them alive.
Performance monitor: JS heap size and DOM node count over a 5-minute repetition should plateau.

## Automated (memlab)
```js
// scenario.js
module.exports = {
  url: () => 'http://localhost:3000/',
  action: async (page) => { await page.click('[data-testid=open-report]') },
  back:   async (page) => { await page.click('[data-testid=close-report]') },
}
```
```bash
npx memlab run --scenario scenario.js     # baseline -> action -> back snapshots
npx memlab analyze unbound-object         # objects growing across snapshots
```
memlab reports leak traces (retainer paths) for detached DOM and unreleased objects.

## Typical causes
Global event listeners or `setInterval` not removed on unmount, subscriptions (RxJS, stores) not unsubscribed, caches keyed by DOM nodes, third-party widgets.

## Gotchas
- DevTools open itself holds references (console logging objects); clear console.
- Dev builds (React StrictMode double mounts) behave differently from prod builds; test the prod build.

## Verify
memlab run in CI on key flows reports zero leaks, and heap after 20 cycles is within a few % of after 2 cycles.
