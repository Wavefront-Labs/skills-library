---
id: computing-software.web-development.frontend-development.async-iterators-and-for-await
name: async-iterators-and-for-await
category: computing-software
field: web-development
product: frontend-development
tags: [iterators-generators, async-iterators, for-await, async-generators, streams, javascript]
level: practitioner
status: docs-checked
description: "Consuming and producing async iterables: for await over streams and paginated APIs, async generators, cancellation with return(), and avoiding sequential bottlenecks."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/for-await...of
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/async_function*
  - https://developer.mozilla.org/en-US/docs/Web/API/ReadableStream
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/fromAsync
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Async iterators and `for await`

## 1. Producing: paginate an API lazily
```js
async function* fetchAll(url, { signal } = {}) {
  while (url) {
    const res = await fetch(url, { signal });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const { items, next } = await res.json();
    yield* items;          // one item at a time to the consumer
    url = next;
  }
}
for await (const user of fetchAll("/api/users?limit=100")) {
  if (user.id === target) break;   // stops fetching further pages
}
```

## 2. Consuming built-ins
- Node readable streams are async iterable (`Readable[Symbol.asyncIterator]()`): `for await (const chunk of fs.createReadStream(f))`.
- Web `ReadableStream` implements the async iterable protocol: Chrome 124, Firefox 110, Deno; Safari 27 per MDN browser-compat-data. Fall back to `getReader()` loops on older engines.

## 3. Semantics
- `for await` awaits each `next()` - strictly sequential. It also accepts sync iterables of promises, awaiting each in order.
- `break`/`throw` calls `return()` on the iterator, which runs the generator's `finally` (close sockets, cancel readers).
- Errors thrown inside the generator surface at the `for await` line.

## 4. Pitfalls
- **Accidental serialisation**: `for await (const x of ids.map(fetchOne))` starts all requests at once (the map) then awaits in order - fine; but `for (const id of ids) await fetchOne(id)` is fully sequential. Choose deliberately; cap parallelism with a pool when needed.
- Iterating an array of already-started promises with `for await` awaits them in order; a rejection of a later promise is not observed until the loop reaches it. Use `Promise.allSettled` for batches.
- Async generators cannot be consumed by plain `for...of` or spread; collect with `Array.fromAsync`.
- Always wire an `AbortSignal` into fetches inside generators so early exit also cancels the in-flight request.

## Verify
Test: break after first item and assert only one page was fetched (mock fetch call count).

## Checked

2026-10-26. MDN `for await...of` (sync and async iterables, `return()` called on early exit and awaited, only where `await` is allowed), `ReadableStream` async iteration, `Array.fromAsync` and mdn/browser-compat-data (Array.fromAsync: Chrome 121, Firefox 115, Safari 16.4; ReadableStream async iterator: Chrome 124, Firefox 110, Safari 27). Removed the unconfirmed Node `readline` and `events.on` bullets and the unconfirmed claim that Node reports an unhandled rejection in that case.

Method: documentation only; no commands were run.
