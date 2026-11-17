---
id: computing-software.software-engineering.typescript.promises-and-async-combinators
name: promises-and-async-combinators
category: computing-software
field: software-engineering
product: typescript
tags: [javascript, promises, promise-all, promise-allsettled, promise-race, promise-any, async-await, concurrency-limit, floating-promises, microtasks]
level: practitioner
status: docs-checked
description: "Use JS promises correctly: sequential vs concurrent awaits, all/allSettled/race/any semantics, bounded concurrency, floating promises and microtask ordering."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/all
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/allSettled
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/race
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/any
  - https://developer.mozilla.org/en-US/docs/Web/API/AbortSignal/timeout_static
  - https://nodejs.org/api/cli.html#--unhandled-rejectionsmode
  - https://typescript-eslint.io/rules/no-floating-promises/
  - https://typescript-eslint.io/rules/no-misused-promises/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Promises and async combinators

**Goal:** run independent async work concurrently, handle partial failure on purpose,
and never lose an error in an un-awaited promise.

## Sequential by accident
```ts
const a = await getUser(id);       // waits
const b = await getOrders(id);     // only starts after a resolves
// concurrent:
const [user, orders] = await Promise.all([getUser(id), getOrders(id)]);
```
`await` inside a `for` loop serialises; `array.forEach(async ...)` fires everything and
awaits nothing (forEach ignores returned promises). Use `for...of` with await for
sequential, `Promise.all(items.map(...))` for concurrent.

## Combinator semantics
| Combinator | Resolves when | Rejects when |
|---|---|---|
| `Promise.all` | all fulfil (array in input order) | first rejection (others keep running!) |
| `Promise.allSettled` | all settle; `{status, value/reason}` each | never |
| `Promise.race` | first settles (either way) | first settles with rejection |
| `Promise.any` | first fulfils | all reject (`AggregateError`) |
`Promise.all` rejecting does not cancel the other operations; pair with AbortController
if they should stop.

## Bounded concurrency
`Promise.all` over 10,000 URLs opens 10,000 requests. Limit it:
```ts
for (let i = 0; i < urls.length; i += 8) {
  await Promise.all(urls.slice(i, i + 8).map(fetchJson));   // at most 8 in flight
}
```
Or use a small worker pool.

## Timeouts
`await Promise.race([work, timeout(5000)])` leaves `work` running; prefer APIs that take
`AbortSignal.timeout(5000)`.

## Floating promises
A promise neither awaited nor `.catch`-ed loses its error (unhandled rejection; in Node
15+ that crashes the process). Enable `@typescript-eslint/no-floating-promises` and
`no-misused-promises`. Intentional fire-and-forget: `void doThing().catch(log)`.

## Ordering
`await` and `.then` callbacks run as microtasks, before timers (`setTimeout`) and I/O
callbacks.

## Error handling
`try { await x() } catch {}` catches; `return x()` inside try without await does NOT
catch x's rejection in that function. Use `return await` inside try blocks.

## Verify
- [ ] Lint rules for floating/misused promises enabled and clean.
- [ ] Independent awaits in hot paths are concurrent (check a trace or timing).

## Checked
Checked 2026-10-25 against the MDN content repository, the Node.js CLI docs and the typescript-eslint rule docs. Confirmed: Promise.all rejects immediately with the first rejection (it does not cancel other work); allSettled never rejects; race settles with the first settled promise; any rejects with an AggregateError; `AbortSignal.timeout()`; `--unhandled-rejections` defaults to throw; the no-floating-promises rule supports `void`; the no-misused-promises rule exists. Replaced the p-limit example with a chunking loop and removed the unconfirmed microtask starvation claim.
Method: documentation only; no commands were run.
