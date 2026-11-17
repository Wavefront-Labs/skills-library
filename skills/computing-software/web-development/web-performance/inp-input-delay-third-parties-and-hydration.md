---
id: computing-software.web-development.web-performance.inp-input-delay-third-parties-and-hydration
name: inp-input-delay-third-parties-and-hydration
category: computing-software
field: web-development
product: web-performance
tags: [inp, input-delay, hydration, third-party-scripts, long-tasks, core-web-vitals, partytown]
level: practitioner
status: docs-checked
description: "Reducing INP input delay: finding main-thread work that blocks interactions, taming third-party scripts and tag managers, and breaking up long tasks."
sources:
  - https://web.dev/articles/optimize-input-delay
  - https://web.dev/articles/inp
  - https://web.dev/articles/optimize-long-tasks
  - https://partytown.qwik.dev/
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# INP input delay

INP = input delay + processing duration + presentation delay. **Input delay** is the time an interaction waits because the main thread is busy with something else.

## 1. Find what's blocking
- Field: measure INP with the `web-vitals` library (web.dev).
- Lab: use the Performance panel, interact during load, and look for long tasks overlapping the interaction.

## 2. Usual culprits
- **Third-party scripts**: tag managers, A/B tests, chat widgets, session replay, ad scripts.
  - Load non-critical third-party scripts later, with `defer`/`async` or after first interaction.
  - Partytown can relocate resource-intensive scripts into a web worker, off the main thread (test carefully).
- **Timers and polling** running heavy work every N ms.

## 3. Break up long tasks
```js
async function processAll(items) {
  for (const [i, item] of items.entries()) {
    process(item);
    if (i % 50 === 0) await (globalThis.scheduler?.yield?.() ?? new Promise(r => setTimeout(r)));
  }
}
```
`scheduler.yield()` is an API designed for yielding to the main thread (web.dev lists support from Chrome 129 and Firefox 142; feature-detect elsewhere, as the code does).

## Verify
Field INP improves; Performance trace shows no long task overlapping first interactions after load.

## Checked

2026-10-28. Confirmed from web.dev (INP: input delay occurs before event handlers run, long tasks as a cause; optimize input delay: timers and `scheduler.yield`; optimize long tasks: `scheduler.yield()` browser support 129/129/142; web-vitals library measures INP) and the Partytown site (relocates resource-intensive scripts into a web worker). Removed (not found): attribution field names, 4x CPU throttle, the hydration bullet and framework claims, Lighthouse audit names, `requestIdleCallback` and facade advice, the 50 ms and 200 ms figures, large-JSON bullet.

Method: documentation only; no commands were run.
