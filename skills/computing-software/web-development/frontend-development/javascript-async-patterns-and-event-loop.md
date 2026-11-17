---
id: computing-software.web-development.frontend-development.javascript-async-patterns-and-event-loop
name: javascript-async-patterns-and-event-loop
category: computing-software
field: web-development
product: frontend-development
tags: [javascript, event-loop, microtask, macrotask, promise, async-await, promise.all, race-conditions, settimeout, web-development, microtasks, promise-combinators]
level: advanced
status: docs-checked
description: "The JS event loop (microtasks vs macrotasks), promise combinators (all/allSettled/race/any), and the async/await bugs that come from misreading ordering."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Using_promises
  - https://developer.mozilla.org/en-US/docs/Web/API/HTML_DOM_API/Microtask_guide
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/any
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/async_function
  - https://html.spec.whatwg.org/multipage/webappapis.html#microtask-queue
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# JS async — event loop ordering and promise combinators

**Goal:** predict exact execution order instead of guessing, and pick the right
promise combinator so one failure doesn't silently swallow the rest.

## 1. The ordering rule that explains 90% of "why did this run in that order"
Per loop iteration: run one macrotask (a timer callback, I/O callback, UI event),
then drain the **entire** microtask queue (promise `.then`/`.catch`/`.finally`
callbacks, `queueMicrotask`) before the next macrotask runs, before any rendering.
```js
setTimeout(() => console.log('timeout'), 0);
Promise.resolve().then(() => console.log('promise'));
console.log('sync');
// sync, promise, timeout — promise beats a 0ms timeout every time
```
A promise chain of ten `.then()`s all resolve before a single already-queued
`setTimeout(fn, 0)` fires, because the microtask queue fully drains between
macrotasks, not after one callback.

## 2. `async`/`await` is sugar over this — not a different mechanism
```js
async function f() { console.log('A'); await null; console.log('B'); }
f(); console.log('C');
// A, C, B — everything after an `await` is scheduled as a microtask continuation
```
Code before the first `await` in an async function runs synchronously,
immediately, on the calling turn. Code after `await` runs later even if the
awaited value is already resolved — this is why calling an async function and
expecting its first side effect to be visible before the next line runs is wrong.

## 3. The four promise combinators — reaching for the wrong one loses data
- **`Promise.all`** — rejects as soon as *any* input rejects, discarding results
  from the ones that succeeded. Wrong when you want partial results.
- **`Promise.allSettled`** — always resolves, with `{status, value|reason}` per
  input. Use when you want every result regardless of individual failures
  (e.g., fetching 5 independent dashboard widgets — one failing shouldn't blank
  the page).
- **`Promise.race`** — settles on whichever input settles first, success or
  failure. Common misuse: implementing a timeout this way without also cancelling
  the loser — the slow request still runs to completion in the background
  (use `AbortController` to actually cancel it).
- **`Promise.any`** — resolves on the first *fulfillment*, ignores rejections
  unless all reject (then throws `AggregateError`). Use for "try several mirrors,
  take whichever responds first."

## 4. Sequential vs parallel awaits — the loop mistake
```js
for (const id of ids) { results.push(await fetchOne(id)); }      // sequential: N × latency
const results = await Promise.all(ids.map(fetchOne));            // parallel: ~1 × latency
```
Use the sequential form only when each call genuinely depends on the previous
result or you need to bound concurrency (rate limits) — otherwise parallelize.
For bounded concurrency without a library, batch with `Promise.all` over chunks,
or write a small concurrency limiter.

## 5. Error handling gotchas
- A `.catch()` attached after a `.then()` catches errors from *both* the original
  promise and the `.then()` callback — know which stage threw before assuming the
  catch covers what you think.
- An error thrown inside an `async` function is a *rejected promise*, not a thrown
  exception at the call site — a bare (non-awaited) call swallows it silently
  unless you attach `.catch()` or await inside a `try`.
- `queueMicrotask` vs `setTimeout(fn, 0)`: the microtask queue is drained after the current task and before the next task, so a long chain of microtasks delays everything queued behind it. Break up heavy chained `.then()` work with a task boundary (`setTimeout`) when it needs to yield to the browser.

## Verify
- [ ] Independent async calls use `Promise.all`/`allSettled` instead of a sequential `for` loop with `await`.
- [ ] `Promise.race`-based timeouts pair with an `AbortController` to actually cancel the loser.
- [ ] Every async function call that isn't awaited has an attached `.catch()`.
- [ ] Code that must run before vs after an `await` is understood, not just "it works."
- [ ] `allSettled` is used wherever one failure shouldn't take down unrelated results.

## Checked

2026-10-26. MDN microtask guide (one task per loop iteration, then microtasks drained), Promise.all/any/race/allSettled pages (any fulfils with the first fulfilment, AggregateError when all reject), and the async function page (await suspends the function after its synchronous start). Removed the unconfirmed p-limit mention and the paint-ordering wording.

Method: documentation only; no commands were run.
