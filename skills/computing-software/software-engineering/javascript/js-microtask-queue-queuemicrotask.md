---
id: computing-software.software-engineering.javascript.js-microtask-queue-queuemicrotask
name: js-microtask-queue-queuemicrotask
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, queuemicrotask, js-event-loop]
level: advanced
status: docs-checked
description: "How promise jobs and queueMicrotask use the HTML microtask queue, when microtask checkpoints run, and how to predict ordering against sync code."
sources:
  - https://html.spec.whatwg.org/multipage/webappapis.html#event-loops
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Microtask queue and queueMicrotask

- In browsers the HTML Standard defines the microtask queue. `queueMicrotask(callback)` is part of the global scope interface (`undefined queueMicrotask(VoidFunction callback)`).
- Promise jobs go on the same queue: the HostEnqueuePromiseJob implementation says "Queue a microtask" for the job from NewPromiseReactionJob or NewPromiseResolveThenableJob. So `.then` callbacks and `queueMicrotask` callbacks run in the order they were queued.
- A microtask checkpoint is performed after running a script when the JavaScript execution context stack is empty, so synchronous code on the stack always finishes before any queued microtask runs.
- Kept-alive WeakRef objects are cleared in the perform a microtask checkpoint algorithm, so a WeakRef target stays reachable for the rest of the current synchronous job and its microtasks.
- Use `queueMicrotask(fn)` for "after this synchronous block" work when you do not need a promise.

Self-check: run `Promise.resolve().then(()=>log(2)); queueMicrotask(()=>log(3)); log(1)` and confirm the order is 1, 2, 3.

## Checked

Checked 2026-11-08 against the HTML Standard webappapis page: queueMicrotask IDL line, HostEnqueuePromiseJob ("Queue a microtask"), the microtask checkpoint step after script execution, and the WeakRef note. Removed because the cited page did not give them in a form I could locate: the `await` claim, the MutationObserver claim, the timer clamping figure, the macrotask and rendering ordering, and the Node `process.nextTick` and `setImmediate` ordering.
Method: docs-only read of cited pages, 2026-11-08
