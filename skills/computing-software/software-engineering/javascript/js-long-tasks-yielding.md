---
id: computing-software.software-engineering.javascript.js-long-tasks-yielding
name: js-long-tasks-yielding
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, scheduler-yield, js-event-loop]
level: advanced
status: docs-checked
description: "Break up long main-thread tasks (over 50 ms) by yielding with scheduler.yield and a setTimeout fallback, batching work by a time deadline."
sources: ["https://web.dev/articles/optimize-long-tasks"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Long tasks and yielding to the main thread

- A task is a discrete piece of browser work (rendering, parsing, running JavaScript). The main thread runs one task at a time; any task over 50 ms is a long task, and the time beyond 50 ms is its blocking period. Interactions wait while a task runs, so long tasks make the UI feel unresponsive and score badly on Interaction to Next Paint (INP). Chrome's performance profiler marks long tasks with a red triangle.
- JavaScript uses run-to-completion: a function that calls five functions runs them all in one task. Breaking code into functions does not break up the task; yielding does.
- `setTimeout(fn, 0)` defers work to a separate task, but the deferred task goes to the end of the queue (other waiting tasks run first), and after five nested `setTimeout`s the browser imposes a minimum 5 ms delay each.
- `await scheduler.yield()` pauses the function and schedules the rest (the continuation) in a new task; layout and paint can run between. Its advantage is a prioritised continuation: it runs before other queued tasks of the same kind, so third-party tasks do not jump ahead. It only schedules; the `await` is what pauses, and `Array.prototype.forEach` does not wait for async callbacks.
- `scheduler.yield()` is not supported in all browsers. Fallback from the article: `if (globalThis.scheduler?.yield) return scheduler.yield(); return new Promise(r => setTimeout(r, 0));` (check both `scheduler` and `yield`). A polyfill (scheduler-polyfill) is another option. As progressive enhancement: `await globalThis.scheduler?.yield?.();`.
- Do not yield after every call: let critical UI updates run together, then yield before less critical or background work. Yielding has overhead, so for many short jobs yield only when a deadline has passed (the article uses `performance.now() - lastYield > 50`, adjustable between responsiveness and completion time).
- The article no longer recommends `isInputPending()` (it can wrongly return false, input is not the only reason to yield, and `scheduler.postTask()` / `scheduler.yield()` supersede it).
- Web workers are the exception to main-thread execution, so CPU work can move there.

Self-check: a performance trace after adding yields shows the work split into several tasks, none with a blocking period.

## Checked

Confirmed on the web.dev "Optimize long tasks" article (updated December 2024): all points above. Removed: `PerformanceObserver({ type: "longtask" })`, `requestIdleCallback` (and its Safari support), `scheduler.postTask(fn, { priority })` usage details and the "Chromium only" label; the browser support table in the page is partial, so no versions are given.

Method: docs-only read of cited pages, 2026-11-08
