---
id: computing-software.software-engineering.javascript.js-event-loop-and-microtasks
name: js-event-loop-and-microtasks
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, js-event-loop, microtasks, macrotasks, queuemicrotask, task-ordering]
level: advanced
status: docs-checked
description: "Predict execution order across the call stack, microtask queue and task queue."
sources: ["https://tc39.es/ecma262/", "https://developer.mozilla.org/en-US/docs/Web/JavaScript"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Event loop and microtasks

- One thread runs the call stack to empty; then queued microtasks (promise reactions, `queueMicrotask`) run before control returns to the event loop; then the next task (timers, I/O, UI events).
- Order example: sync code, then `Promise.resolve().then` / `await` continuations, then `setTimeout(fn, 0)`.
- `await x` schedules the continuation as a microtask; MDN warns that abusing microtasks leads to performance problems.
- `setTimeout` is a minimum delay: browsers enforce at least 4 ms once a timer has been nested 5 times, and inactive tabs are throttled further (browser-dependent). Use `requestAnimationFrame` for visual work and `requestIdleCallback` or `scheduler.postTask` for low-priority work where supported (feature-detect).
- Never block with a long synchronous loop: break work into chunks, yield with `await new Promise(r => setTimeout(r))` or `scheduler.yield()` where supported (feature-detect), or move it to a Worker.
- In Node the loop has phases (timers, poll, check, among others). `process.nextTick` is not part of the loop: its queue is drained after the current operation, before the loop continues, and recursive calls can starve I/O. `setImmediate` vs `setTimeout(0)` order is non-deterministic from the main module but `setImmediate` always runs first inside an I/O callback.

Verify: write the log-order puzzle (sync, timeout, promise, nextTick) and predict before running.

## Checked

2026-11-02. Checked against the MDN Event loop, Microtask guide, Using promises, Window.setTimeout, Scheduler.postTask and Scheduler.yield pages and the Node.js event loop, timers and nextTick guide (phases, nextTick queue, setImmediate vs setTimeout ordering, 4 ms clamp after 5 nested timers). Removed: MutationObserver as a microtask, the rendering step in the loop description, the claim that an endless microtask chain starves rendering, and the claim that nextTick runs before promise microtasks (none stated in those pages).

Method: documentation only; no commands were run.
