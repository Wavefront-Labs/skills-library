---
id: computing-software.software-engineering.typescript.iterators-and-generators
name: iterators-and-generators
category: computing-software
field: software-engineering
product: typescript
tags: [javascript, js-generators, async-iterators, iteration-protocol, for-await-of, symbol-iterator, lazy-evaluation, iterator-helpers, pagination]
level: practitioner
status: docs-checked
description: "Use the JS iteration protocols: custom iterables, generators for lazy sequences, async generators for paginated APIs and streams, cleanup with return(), iterator helpers."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Iteration_protocols
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/function*
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/for-await...of
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Iterator
  - https://nodejs.org/api/readline.html#rlsymbolasynciterator
  - https://github.com/mdn/browser-compat-data/blob/main/javascript/builtins/Iterator.json
  - https://www.typescriptlang.org/docs/handbook/release-notes/typescript-6-0.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Iterators and generators

**Goal:** process large or remote sequences lazily (one item at a time) with plain
`for...of`, instead of loading everything into arrays.

## Generators
```ts
function* range(start: number, end: number, step = 1): Generator<number> {
  for (let i = start; i < end; i += step) yield i;
}
for (const n of range(0, 1e9)) { if (n > 10) break; }   // lazy; only 11 values computed
```
Making a class iterable: implement `[Symbol.iterator]() { return this.items.values(); }`
or a generator method `*[Symbol.iterator]() { ... }`.

## Async generators for paginated APIs
```ts
async function* listAll(client: Api): AsyncGenerator<Item> {
  let cursor: string | undefined;
  do {
    const page = await client.list({ cursor, limit: 100 });
    yield* page.items;
    cursor = page.nextCursor;
  } while (cursor);
}
for await (const item of listAll(api)) {
  if (done(item)) break;     // stops fetching further pages
}
```
Consumers get backpressure for free: the next page is fetched only when needed.
Node readable streams and `readline` interfaces are async iterables too:
`for await (const line of rl) {...}`.

## Cleanup
`break`, `return` or a thrown error inside `for...of` calls the iterator's `return()`,
which runs the generator's `finally` block. Put resource release there:
```ts
async function* rows(db) { const cur = await db.cursor(); try { for await (const r of cur) yield r; } finally { await cur.close(); } }
```

## Iterator helpers (ES2025)
`range(0, 100).filter(isPrime).map(n => n * 2).take(5).toArray()` - lazy helpers on
`Iterator.prototype` (Node 22+ per the MDN compatibility data).

## Gotchas
- Generators are single-use; iterating twice gives nothing the second time. Return a
  fresh generator from a function or implement `[Symbol.iterator]`.
- Spreading an infinite generator (`[...gen()]`) hangs.
- `for await` over an array of promises awaits them sequentially; use `Promise.all` for concurrency.
- TypeScript: `downlevelIteration` and `target: es5` are deprecated in TypeScript 6.0, so target a runtime with native generators and set `target`/`lib` to match.

## Verify
- [ ] Breaking out of a loop over an async generator closes the underlying resource (log in `finally`).
- [ ] Memory stays flat when iterating a very large source.

## Checked
Checked 2026-10-25 against the MDN content repository, MDN browser-compat-data (Iterator.json), the Node.js readline and stream docs and the TypeScript 6.0 release notes. Confirmed: the iterator protocol `return()` cleanup on early exit; `for await...of`; Iterator helper methods (map, filter, take, drop, toArray, and others) shipping in Node 22; readline interfaces and streams being async iterables; downlevelIteration and target es5 deprecated in TypeScript 6.0. Removed the unconfirmed claim about async iterator helpers.
Method: documentation only; no commands were run.
