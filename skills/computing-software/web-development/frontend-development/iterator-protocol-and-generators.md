---
id: computing-software.web-development.frontend-development.iterator-protocol-and-generators
name: iterator-protocol-and-generators
category: computing-software
field: web-development
product: frontend-development
tags: [iterators-generators, iterator-protocol, generators, symbol-iterator, iterator-helpers, javascript]
level: practitioner
status: docs-checked
description: "Implementing the iterator protocol and generators: Symbol.iterator, lazy pipelines, return() cleanup on early exit, iterator helpers, and spreading pitfalls."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Iteration_protocols
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/function*
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Iterator
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Iterator protocol and custom iterables

## 1. The protocol
- **Iterable**: has `[Symbol.iterator]()` returning an iterator.
- **Iterator**: has `next()` returning `{ value, done }`; optionally `return()` (called on early exit) and `throw()`.
Consumers include `for...of`, spread, destructuring, `Array.from`, `Promise.all`, `new Map(iterable)` and `yield*`.

## 2. Write it with a generator
```js
class Range {
  constructor(start, end, step = 1) { Object.assign(this, { start, end, step }); }
  *[Symbol.iterator]() { for (let i = this.start; i < this.end; i += this.step) yield i; }
}
[...new Range(0, 5)]; // [0,1,2,3,4]

function* lines(text) { let i = 0, j; while ((j = text.indexOf("\n", i)) !== -1) { yield text.slice(i, j); i = j + 1; } yield text.slice(i); }
```
Generators are lazy: work happens only when the consumer pulls.

## 3. Cleanup on early exit
`break`, `return`, or a thrown error in `for...of` calls the iterator's `return()`; in a generator that runs `finally` blocks:
```js
function* rows(db) { const cur = db.open(); try { let r; while ((r = cur.next())) yield r; } finally { cur.close(); } }
```

## 4. Iterator helpers (Baseline 2025)
```js
naturals().filter(n => n % 2).map(n => n * n).take(5).toArray();
Iterator.from(someIterable).drop(10);
```
Lazy like generators; methods live on `Iterator.prototype`, so they work on built-in iterators (`map.keys()`, `arr.values()`) and generator objects. Newly available in all major engines with Chrome 122, Firefox 131 and Safari 18.4.

## 5. Pitfalls
- Most iterators are single-use: a generator object is exhausted after one loop. Make the class iterable (fresh iterator per call) rather than storing one generator.
- Spreading an infinite generator hangs - use `take`.
- `for...in` iterates keys of objects, not iterable values. Plain objects are not iterable - use `Object.entries(o)`.

## Verify
Test early-exit: break after the first item and assert the resource's close/finally ran.

## Checked

2026-10-26. MDN iteration protocols (`next()` returns `{ value, done }`; optional `return()` and `throw()`) and `Iterator` reference, plus mdn/browser-compat-data for iterator helpers (Chrome 122, Firefox 131, Safari 18.4, so Baseline 2025). Removed the unmeasured performance claim and the core-js pointer.

Method: documentation only; no commands were run.
