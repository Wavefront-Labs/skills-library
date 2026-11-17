---
id: computing-software.software-engineering.javascript.js-fetch-streaming-retry
name: js-fetch-streaming-retry
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, fetch-retry-backoff, js-fetch]
level: advanced
status: docs-checked
description: "Add retry-with-backoff logic, AbortSignal.timeout and incremental body reading with getReader to fetch."
sources: ["https://developer.mozilla.org/en-US/docs/Web/API/Response/body", "https://developer.mozilla.org/en-US/docs/Web/API/AbortSignal/timeout_static", "https://developer.mozilla.org/en-US/docs/Web/API/Streams_API/Using_readable_streams", "https://developer.mozilla.org/en-US/docs/Web/API/Response/clone"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fetch retries, timeouts and response streaming

- `fetch()` rejects on a network error but resolves on HTTP error statuses, so decide retry from both: a rejected promise, or a status you choose to treat as transient after checking `response.ok`.
- Retry policy is your own code, not a fetch feature. Retry only idempotent requests (or ones that carry an idempotency key), cap the attempts, and add exponential delay with jitter, for example `delay = Math.min(cap, base * 2 ** attempt) * (0.5 + Math.random() / 2)`. If the response carries a `Retry-After` header, prefer it.
- Timeout per attempt: `fetch(url, { signal: AbortSignal.timeout(5000) })`; the signal aborts with a `TimeoutError`, while a manual `AbortController.abort()` gives `AbortError`. Create a new signal for every attempt.
- Stream the body: `const reader = res.body.getReader(); for (;;) { const { done, value } = await reader.read(); if (done) break; }`, or iterate `for await (const chunk of res.body)`.
- A body can be consumed once; `res.clone()` before reading twice (it throws a `TypeError` once the body has been used).

Self-check: a stub that returns 503 twice then 200 produces three attempts with growing waits.

## Checked

2026-11-03. Confirmed on MDN: Response.body and Using readable streams (getReader loop, `done`, async iteration of `response.body`), AbortSignal.timeout (`TimeoutError`), Using Fetch (AbortError, no rejection on HTTP errors), Response.clone. The backoff formula and retry rules are the skill's own design, not documented behaviour, and are labelled as such. Removed: the status list (429/502/503/504) as a documented fact and the `TextDecoderStream` NDJSON/SSE decoding advice, neither of which was on a page read.
Method: documentation only; no commands were run.
