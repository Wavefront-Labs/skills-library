---
id: computing-software.web-development.frontend-development.limiting-concurrency-and-retry-backoff
name: limiting-concurrency-and-retry-backoff
category: computing-software
field: web-development
product: frontend-development
tags: [promises, concurrency-limit, retry-backoff, exponential-backoff, javascript, fetch]
level: practitioner
status: verified
description: "Running many async tasks with a concurrency cap and retrying failures with exponential backoff and jitter, honouring Retry-After and AbortSignal, without libraries."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise
  - https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Retry-After
  - https://www.rfc-editor.org/rfc/rfc9110#name-idempotent-methods
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Concurrency limits and retry with backoff

## 1. Pool
`Promise.all(items.map(fetchOne))` fires everything at once - 5,000 requests will hit rate limits, exhaust sockets, or OOM.
```js
async function mapPool(items, limit, fn) {
  const results = new Array(items.length);
  let next = 0;
  async function worker() {
    while (next < items.length) { const i = next++; results[i] = await fn(items[i], i); }
  }
  await Promise.all(Array.from({ length: Math.min(limit, items.length) }, worker));
  return results;
}
const pages = await mapPool(urls, 6, u => fetchJson(u));
```
`next++` is safe: JS is single-threaded between awaits. Libraries: `p-limit`, `p-map` (adds `stopOnError: false`). For streams of work, Node `stream.Readable.from(items).map(fn, { concurrency: 6 })`.

## 2. Retry with exponential backoff and full jitter
```js
async function retry(fn, { tries = 5, base = 300, cap = 10_000, signal } = {}) {
  for (let attempt = 0; ; attempt++) {
    try { return await fn(attempt); }
    catch (err) {
      if (attempt + 1 >= tries || !isRetryable(err) || signal?.aborted) throw err;
      const retryAfter = err.retryAfterMs;                 // parsed from Retry-After header
      const delay = retryAfter ?? Math.random() * Math.min(cap, base * 2 ** attempt);
      await new Promise((r, j) => { const t = setTimeout(r, delay); signal?.addEventListener("abort", () => { clearTimeout(t); j(signal.reason); }, { once: true }); });
    }
  }
}
const isRetryable = e => e.name === "TypeError" /* network */ || [408, 429, 500, 502, 503, 504].includes(e.status);
```

## 3. Rules
- Retry only idempotent operations (GET, PUT, DELETE) or POSTs carrying an idempotency key.
- Never retry 4xx except 408/429. Honour `Retry-After` (seconds or HTTP date).
- Jitter is required: without it, clients that failed together retry together (thundering herd).
- Put a timeout on each attempt (`AbortSignal.timeout(5000)` combined via `AbortSignal.any([signal, timeout])`) and an overall deadline.
- Retries multiply load in layered systems (3 layers x 3 retries = 27x) - retry at one layer only.

Run in Node 20: `mapPool` over 50 items with `limit` 6 peaked at 6 in flight and kept result order, an empty list returned `[]`, `Readable.from(items).map(fn, { concurrency: 6 })` peaked at 6, while `Promise.all` over 500 tasks peaked at 500. `retry` returned `"ok"` on the 3rd attempt for a 503, stopped after 1 attempt for a 404, made exactly `tries` (4) attempts for persistent 500s, and rejected with `signal.reason` when aborted mid-wait. `AbortSignal.timeout(10)` aborted with a `TimeoutError`; `AbortSignal.any` exists in Node 20 (MDN compat: Chrome 116, Firefox 124, Safari 17.4). `p-map`'s README lists `stopOnError`.

## Verify
Tests with fake timers: assert max N in-flight (counter in mocked fn) and that delays grow and stop after `tries`.
