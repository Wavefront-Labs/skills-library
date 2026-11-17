---
id: computing-software.web-development.frontend-development.generator-functions-and-delegation
name: generator-functions-and-delegation
category: computing-software
field: web-development
product: frontend-development
tags: [generator-functions, yield-delegation, generators, lazy-sequences, javascript]
level: practitioner
status: docs-checked
description: "Writing generator functions: lazy sequences, yield* delegation, two-way next(value), return/throw cleanup with finally, and async generators for paginated APIs."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/function*
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/yield*
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/async_function*
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Generator functions and delegation

## 1. Lazy sequences
```js
function* naturals(start = 0) { for (let n = start; ; n++) yield n; }
function* take(it, k) { for (const x of it) { if (k-- <= 0) return; yield x; } }
[...take(naturals(1), 3)];   // [1, 2, 3]  infinite source, finite consumption
```
Nothing runs until the first `next()`; each `yield` pauses with the stack intact.

## 2. yield* delegation
```js
function* walk(node) {
  yield node;
  for (const child of node.children) yield* walk(child);   // recursive tree traversal
}
```
`yield*` forwards every value of the inner iterable (arrays, strings, other generators) and evaluates to the inner generator's `return` value.

## 3. Two-way communication
```js
function* dialog() { const name = yield "name?"; const age = yield `hi ${name}, age?`; return { name, age }; }
const g = dialog();
g.next();          // { value: "name?", done: false }  first next() argument is ignored
g.next("Ada");     // { value: "hi Ada, age?" }
g.next(36);        // { value: { name: "Ada", age: 36 }, done: true }
```

## 4. Cleanup
`break` out of `for...of`, or `g.return(v)`, resumes the generator at a `return` point so `finally` runs:
```js
function* lines(handle) { try { while (true) yield handle.readLine(); } finally { handle.close(); } }
```
`g.throw(err)` raises inside the generator at the paused `yield`.

## 5. Async generators for paging
```js
async function* allPages(url) {
  while (url) {
    const res = await fetch(url); const body = await res.json();
    yield* body.items;
    url = body.next;
  }
}
for await (const item of allPages("/api/items")) { if (done(item)) break; }   // stops fetching early
```

## Gotchas
- A generator object is single-use; iterate twice and the second loop is empty. Make the class iterable (`[Symbol.iterator]() { return gen(); }`) for re-iteration.
- Arrow functions cannot be generators.
- `[...infinite()]` hangs; always bound with `take`/iterator helpers.

## Verify
- [ ] Early `break` closes underlying resources (test `finally` runs).

## Checked

2026-10-26. MDN `function*` (no arrow-function counterpart; `throw()` acts as a throw at the suspended position; `return` ends the generator), `yield*` (evaluates to the inner iterator's return value; forwards `throw()` and `return()`) and async generator reference read from the mdn/content repository. Examples unchanged.

Method: documentation only; no commands were run.
