---
id: computing-software.software-engineering.javascript.js-aggregateerror-handling
name: js-aggregateerror-handling
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, aggregateerror, js-error-cause]
level: practitioner
status: docs-checked
description: "Read AggregateError.errors from Promise.any rejections and construct your own AggregateError."
sources: ["https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/AggregateError", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AggregateError and Promise.any failures

- `AggregateError` is a subclass of `Error` representing a list of unrelated errors; the `errors` array holds the aggregated errors.
- `Promise.any` rejects with an `AggregateError` containing an array of rejection reasons when all inputs reject (including an empty iterable).
- Catching it: `e instanceof AggregateError` is true, `e.name` is `"AggregateError"`, `e.errors` is the array, and `e.message` is `"All Promises rejected"` in MDN's example.
- Create your own: `throw new AggregateError([new Error("some error")], "Hello")`, then read `e.message` and `e.errors`.
- `Promise.allSettled` fulfills with an array of objects describing each outcome, so failures can be collected without short-circuiting.

Self-check: MDN's `Promise.any([Promise.reject(new Error("some error"))]).catch(e => e.errors)` yields `[Error: "some error"]`.

## Checked

Date: 2026-11-03. Confirmed on MDN Global_Objects/AggregateError (examples, errors property, subclass of Error) and Global_Objects/Promise (any and allSettled). Removed as not stated there: input-order guarantee for errors, the `{ cause }` constructor option, ES2021 and Node 15 support, the older-runtime logging remark, and the `r.status === "rejected"` filter.

Method: documentation only; no commands were run.
