---
id: computing-software.web-development.angular.http-errors-and-fetch-options
name: http-errors-and-fetch-options
category: computing-software
field: web-development
product: angular
tags: [angular, http, httperrorresponse, timeout, fetch, credentials, referrerpolicy, integrity, ssr]
level: advanced
status: docs-checked
description: "Angular HttpClient failures and fetch options: HttpErrorResponse, retry, timeout, keepalive, cache, priority, mode, redirect, credentials, referrer, integrity, SSR cautions."
sources:
  - https://angular.dev/guide/http/making-requests
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Failures: a network error, a timeout (when `timeout` is set), or an error response from the backend. All arrive as an `HttpErrorResponse` on the Observable's error channel. Network and timeout errors have `status` `0`; for timeouts `error` is a `DOMException` named `TimeoutError`; for network errors it is the error thrown by `fetch` (a `ProgressEvent` with `withXhr()`). Backend errors carry the failing `status` and the error response as `error`. Use RxJS `catchError` to turn errors into UI values and `retry()` to re-subscribe a number of times for transient failures.

Timeout: `http.get('/api/config', {timeout: 3000})` aborts and emits an error if the backend request does not finish. It applies only to the backend request, not the whole handling chain, so interceptor delays do not count.

Fetch backend options (default backend):
- `keepalive: true`: request can outlive the page, e.g. analytics posts.
- `cache`: `'force-cache'`, `'no-cache'` (always network), `'only-if-cached'` (fail if not cached).
- `priority`: `'high'`, `'low'`, `'auto'` (default). Use high for requests affecting LCP and low for ones that do not.
- `mode`: `'same-origin'`, `'cors'` (default), `'no-cors'` (opaque response). On Node.js SSR, Undici does not enforce browser CORS checks, so `mode: 'same-origin'` does not restrict server-side requests; validate user-influenced URLs against an allowlist.
- `redirect`: `'follow'` (default), `'error'`, `'manual'`.
- `credentials`: `'omit'`, `'same-origin'` (default), `'include'`. `withCredentials: true` takes precedence and forces `'include'`; avoid mixing the two. During Node.js SSR, `credentials: 'include'` does not forward cookies from the incoming browser request and does not remove `Cookie` or `Authorization` headers you add explicitly; only forward credential headers to trusted origins.
- `referrer`: a URL string, `''` (no referrer) or `'about:client'` (default current page).
- `referrerPolicy`: `'no-referrer'`, `'no-referrer-when-downgrade'`, `'origin'`, `'origin-when-cross-origin'`, `'same-origin'`, `'strict-origin'`, `'strict-origin-when-cross-origin'` (default browser behaviour), `'unsafe-url'` (can expose sensitive data). Prefer conservative values for privacy-sensitive requests.
- `integrity: 'sha256-...'`: the response must exactly match the hash or the request fails with a network error. During SSR the Fetch implementation reads the whole body to verify integrity before returning, and `maxResponseBodySize` is enforced only after Fetch returns, so it does not constrain data buffered during verification.

```ts
http.post('/api/analytics', analyticsData, {keepalive: true}).subscribe();
http.get('/api/live-data', {cache: 'no-cache', priority: 'high'}).subscribe();
```

## Checked

Date: 2026-11-07

Read in full: https://angular.dev/guide/http/making-requests (source Markdown from the angular/angular repository, adev/src/content/guide, plus the live page text where the fetch returned content). Inline code snippets were read; no separate example files were opened.
No corrections needed; every claim was confirmed against the page.

Method: documentation only; no commands were run.
