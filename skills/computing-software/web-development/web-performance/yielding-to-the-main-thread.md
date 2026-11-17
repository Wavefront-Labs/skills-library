---
id: computing-software.web-development.web-performance.yielding-to-the-main-thread
name: yielding-to-the-main-thread
category: computing-software
field: web-development
product: web-performance
tags: [scheduler-yield, yield-to-main, scheduler-posttask, long-tasks, inp, performance]
level: practitioner
status: verified
description: "Breaking up long tasks for INP: scheduler.yield with fallbacks, chunking loops with a time budget, postTask priorities, and ordering work so the next paint comes first."
sources:
  - https://web.dev/articles/optimize-long-tasks
  - https://developer.mozilla.org/en-US/docs/Web/API/Scheduler/yield
  - https://developer.mozilla.org/en-US/docs/Web/API/Scheduler/postTask
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Yielding to the main thread

A task over 50 ms blocks input handling and painting. Split work and yield so the browser can respond and paint between chunks.

## 1. Yield helper
```js
function yieldToMain() {
  if (globalThis.scheduler?.yield) return scheduler.yield();   // continuation keeps priority
  return new Promise(resolve => setTimeout(resolve, 0));
}
```
`scheduler.yield()` puts the rest of your function at the front of the queue after pending input/paint, instead of the back (where `setTimeout` puts it behind other scripts' tasks). Run in Chromium with a `setTimeout(0)` task already queued: the `scheduler.yield()` continuation ran first, the `setTimeout` continuation ran after it. MDN compat data: `scheduler.yield()` and `scheduler.postTask()` ship in Chrome (129 and 94) and Firefox 142, not Safari, so keep the fallback.

## 2. Paint first, then the rest
```js
button.addEventListener("click", async () => {
  button.classList.add("is-loading");     // cheap visual feedback
  await yieldToMain();                    // let the browser paint it (INP measures to next paint)
  const result = expensiveFilter(data);   // heavy work after the paint
  render(result);
  queueAnalytics();                       // non-urgent last, or in idle time
});
```

## 3. Chunk loops with a budget
```js
async function processAll(items, fn) {
  let deadline = performance.now() + 40;
  for (const item of items) {
    fn(item);
    if (performance.now() > deadline) { await yieldToMain(); deadline = performance.now() + 40; }
  }
}
```
Yielding after every item adds overhead; a ~40-50 ms budget per chunk balances throughput and responsiveness (run: 50 items of 10 ms each with the 40 ms budget yielded 10 times and took about 501 ms, so the overhead is small).

## 4. Priorities
```js
scheduler.postTask(() => sendBeacon(), { priority: "background" });
scheduler.postTask(() => hydrateWidget(), { priority: "user-visible" });
```
`user-blocking` > `user-visible` (default) > `background` (run: tasks queued together ran user-blocking, user-visible, default, background). Feature-detect `scheduler.postTask`; fall back to `setTimeout` / `requestIdleCallback`.

## 5. When yielding is not enough
Move pure computation to a Web Worker; reduce work (memoise, virtualise lists); in React, `startTransition` lets rendering yield.

## Verify
- [ ] Performance panel shows the interaction's long task split into < 50 ms chunks with a frame painted after the first; field INP p75 < 200 ms.
