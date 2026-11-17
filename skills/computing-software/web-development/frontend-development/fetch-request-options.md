---
id: computing-software.web-development.frontend-development.fetch-request-options
name: fetch-request-options
category: computing-software
field: web-development
product: frontend-development
tags: [fetch-request-options, fetch-cache-mode, fetch-credentials, fetch-priority, request-mode, fetch-api]
level: practitioner
status: docs-checked
description: "fetch() RequestInit options in practice: credentials, mode and opaque responses, cache modes, redirect, referrerPolicy, keepalive, priority, integrity and body reuse."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/RequestInit
  - https://developer.mozilla.org/en-US/docs/Web/API/Request/cache
  - https://fetch.spec.whatwg.org/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# fetch request options

## 1. The options that change behaviour
| Option | Values (default first) | Use |
|---|---|---|
| `credentials` | `same-origin`, `include`, `omit` | `include` sends cookies cross-origin (server must allow credentials) |
| `mode` | `cors`, `same-origin`, `no-cors` (`navigate` is for HTML navigations only) | `no-cors` returns an **opaque** response: status 0, unreadable headers and body |
| `cache` | `default`, `no-store`, `reload`, `no-cache`, `force-cache`, `only-if-cached` | control the HTTP cache per request |
| `redirect` | `follow`, `error`, `manual` | `error` rejects on a redirect; `manual` returns a response with almost all fields filtered out so a service worker can store and replay it |
| `referrerPolicy` | same values and semantics as the `Referrer-Policy` header | `no-referrer` for third-party calls |
| `keepalive` | `false` | keeps the request alive if the page unloads; body limited to 64 KiB |
| `priority` | `auto`, `high`, `low` | deprioritise prefetches, boost critical API calls |
| `signal` | - | `AbortSignal.timeout(8000)`, `AbortSignal.any([a, b])` |
| `integrity` | - | Subresource Integrity hash (`<hash-algo>-<base64>`) checked on the response |

## 2. Cache modes
- `no-store`: bypass and do not store.
- `reload`: bypass, then update cache.
- `no-cache`: if there is a match, fresh or stale, make a conditional request and use the cached copy only if the server says it is unchanged.
- `force-cache`: use any cached copy, even stale.
- `only-if-cached`: only with `mode: "same-origin"`, else TypeError.
These act on the browser HTTP cache only (MDN: the `cache` property controls how the request interacts with the browser's HTTP cache).

## 3. Bodies
```js
await fetch("/api", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data) });
await fetch("/upload", { method: "POST", body: formData });   // do NOT set Content-Type: boundary is added for you
```
A body stream can be read once: `res.json()` twice throws "body used"; `res.clone()` before reading if two consumers need it. Streaming request bodies need `duplex: "half"` (the only permitted value).

## 4. Headers you cannot set
Many headers are set by the browser and scripts cannot set them (MDN glossary: forbidden request headers). With `mode: "no-cors"` only CORS-safelisted request headers may be set, and the method must be HEAD, GET or POST. A cross-origin request with an `Authorization` header triggers a CORS preflight.

## Gotchas
- `credentials: "include"` with `Access-Control-Allow-Origin: *` fails; the server must echo the origin.
- `no-cors` is not a CORS fix: you get nothing readable.
- `keepalive` bodies are limited to 64 KiB; `navigator.sendBeacon` is the alternative for small analytics POSTs.

## Verify
- [ ] Network panel shows the expected `Sec-Fetch-Mode`, cookies and cache status ("disk cache", "304") for each call.

## Checked

Checked 2026-10-26 against MDN RequestInit, Request.cache, Request.credentials, Request.mode, Request.redirect, Request.duplex and the CORS guide (mdn/content main): defaults (`same-origin`, `cors`, `follow`, `auto`, `false`), cache-mode semantics, `only-if-cached` needing `same-origin`, opaque no-cors responses with status 0, the 64 KiB keepalive body limit, priority values, `duplex: "half"`, and the wildcard-origin restriction with credentials. Removed the Next.js remark, the Chromium-only duplex claim, the forbidden-header list and the keepalive TypeError claim, which no checked page states.

Method: documentation only; no commands were run.
