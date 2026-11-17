---
id: computing-software.software-engineering.javascript.js-for-await-concurrency
name: js-for-await-concurrency
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, for-await-pattern, js-async-iteration]
level: advanced
status: docs-checked
description: "Consume async and sync iterables with for await...of: sequential awaits, early exit cleanup, and where concurrency must come from elsewhere."
sources: ["https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/for-await...of"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# for await with concurrency control

- `for await (variable of iterable)` gets `[Symbol.asyncIterator]()`; if absent it falls back to `[Symbol.iterator]()` and wraps the sync iterator in an async one. It then repeatedly calls `next()` and awaits the returned promise, so items are processed one at a time, in order. Parallelism has to come from something else you build around the loop.
- It can only be used where `await` can be used: inside an async function body or in a module.
- Over a sync iterable that yields promises, it produces the resolved values, where `for...of` would produce the promises. Even for sync iterables the loop awaits each step, which is slower because of repeated promise unwrapping.
- Because the loop pulls the next value only after the body finishes, a slow body naturally slows the producer. That is backpressure by construction; any pool of in-flight tasks you add must itself stop pulling when full.
- Early exit (`break`, or a thrown error) calls the iterator's `return()` method for cleanup, and the returned promise is awaited before the loop exits. Put cleanup in the iterator's `return()` or in a `finally` of an async generator.
- If a sync generator yields a rejected promise, the loop calls the generator's `return()` before throwing the rejection, so its `finally` blocks run.
- Async generators (`async function*`) conform to the async iterable protocol, so they can be looped directly; MDN's example wraps a `ReadableStream` reader this way.
- `break` and `continue` work as in other loops.

Self-check: with a hand-built pool of concurrency 4, never more than 4 jobs run at once.

## Checked

2026-11-08. Confirmed on MDN for await...of: iterator lookup and fallback, awaiting `next()`, usage context, sync-iterable differences, `return()` cleanup on early exit, rejected-promise handling, async generators. Removed the `Promise.all`/`Promise.race` batching recipe, the claim that Node streams are async iterable, and the `Array.fromAsync` note, which the page does not cover.

Method: docs-only read of cited pages, 2026-11-08
