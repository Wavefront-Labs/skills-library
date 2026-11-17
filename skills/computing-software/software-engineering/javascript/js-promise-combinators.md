---
id: computing-software.software-engineering.javascript.js-promise-combinators
name: js-promise-combinators
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, promise-allsettled, js-promises]
level: practitioner
status: docs-checked
description: "Choose among Promise.all, allSettled, any and race; use withResolvers and AbortSignal where the Promise docs say so."
sources: ["https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Promise combinators

- `Promise.all()` fulfills when all inputs fulfill and rejects with the first rejection reason. `allSettled()` fulfills when all inputs settle, with an array of objects describing each outcome. `any()` fulfills with the first fulfillment and rejects with an `AggregateError` when all reject. `race()` settles when any input settles.
- `Promise.withResolvers()` returns an object containing a new promise and the functions that resolve or reject it, matching the executor's two parameters.
- These methods attach handlers with `then()` and never remove them, even after the result has settled early (such as in `race()`). Promises have no unsubscribe, so where possible cancel the underlying operation with an `AbortSignal` once the pending promise is no longer useful.
- JavaScript is single-threaded: concurrency here means interleaved tasks; parallel execution needs worker threads.
- Newer keyed variants, `Promise.allKeyed()` and `Promise.allSettledKeyed()`, take an object of promises and fulfill with an object of the same shape; check support before use.

## Checked

Date: 2026-11-03. Confirmed on MDN Global_Objects/Promise: the four combinators, withResolvers, handler accumulation and AbortSignal advice, single-threaded note, keyed variants. Removed as not stated there: "others keep running" detail, the ES2024 label, the timeout race recipe with `AbortSignal.timeout`, the concurrency-pool advice and the fetch flooding example, the `allSettled` self-check.

Method: documentation only; no commands were run.
