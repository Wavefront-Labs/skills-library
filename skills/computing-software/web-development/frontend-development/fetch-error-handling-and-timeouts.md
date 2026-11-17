---
id: computing-software.web-development.frontend-development.fetch-error-handling-and-timeouts
name: fetch-error-handling-and-timeouts
category: computing-software
field: web-development
product: frontend-development
tags: [fetch-api, browser-networking, fetch-error-handling, response-ok, abortsignal-timeout, http-errors, retries, fetch-timeout, fetch-retry]
level: practitioner
status: docs-checked
description: "Handling fetch correctly: it only rejects on network failure, checking response.ok, timeouts with AbortSignal.timeout, parsing errors and retry rules."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch
  - https://developer.mozilla.org/en-US/docs/Web/API/AbortSignal/timeout_static
  - https://www.rfc-editor.org/rfc/rfc9457
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Fetch error handling and timeouts

**Goal:** every request has a timeout, HTTP errors are surfaced as errors, and retries happen only when safe.

## 1. fetch resolves on HTTP errors
`fetch()` rejects only on network failure, CORS failure, or abort. A 404 or 500 **resolves** with `res.ok === false`. A wrapper:
```js
export class HttpError extends Error {
  constructor(res, body) { super(`${res.status} ${res.statusText}`); this.status = res.status; this.body = body; }
}
export async function api(path, { timeout = 10_000, signal, ...init } = {}) {
  const res = await fetch(path, {
    ...init,
    signal: signal ? AbortSignal.any([signal, AbortSignal.timeout(timeout)]) : AbortSignal.timeout(timeout),
    headers: { Accept: 'application/json', ...init.headers },
  });
  const type = res.headers.get('content-type') ?? '';
  const body = type.includes('json') ? await res.json().catch(() => null) : await res.text();
  if (!res.ok) throw new HttpError(res, body);
  return body;
}
```

## 2. Classify failures
| Error | Meaning | Action |
|---|---|---|
| `TypeError` (message varies by browser) | Network error, CORS failure, bad scheme | Offline UI; check console for CORS |
| `DOMException` name `TimeoutError` | `AbortSignal.timeout` fired | Retry if idempotent |
| `DOMException` name `AbortError` | You cancelled (navigation, unmount) | Ignore silently |
| `HttpError` 4xx | Client problem | Show message; don't retry (except 408/429) |
| `HttpError` 5xx / 429 | Server/overload | Retry with backoff, honour `Retry-After` |

## 3. Retry rules
Retry only idempotent methods (GET/PUT/DELETE) or POSTs carrying an idempotency key. Exponential backoff with jitter, cap attempts (3), stop on abort.

## 4. Gotchas
- An empty body (for example a 204) is not valid JSON, so `res.json()` rejects - check status/content-type first.
- A body can be read only once; call `res.clone()` before reading if two consumers need it.
- CORS errors are deliberately opaque to JS; the console shows the reason.
- `fetch()` has no timeout option of its own; add one with `AbortSignal.timeout()`.

## Verify
- [ ] Throttle to offline: user sees an offline message, not an unhandled rejection.
- [ ] Server returns 500 with a JSON problem body: UI shows a friendly error, console logs details.
- [ ] Slow endpoint aborts at the timeout.

## Checked

Checked 2026-10-26 against MDN Using Fetch, AbortSignal.timeout(), AbortSignal.any() (mdn/content main) and the RFC 9457 title (Problem Details for HTTP APIs, rfc-editor.org): fetch rejects on network errors but fulfils on 404/500, `TimeoutError` from `AbortSignal.timeout()`, `AbortError` on abort, `AbortSignal.any()` semantics, and one-time body reading with clone(). Removed the Chromium-specific 'Failed to fetch' wording and the unconfirmed 'browser may wait minutes' claim; the retry guidance is advice, not a documented figure.

Method: documentation only; no commands were run.
