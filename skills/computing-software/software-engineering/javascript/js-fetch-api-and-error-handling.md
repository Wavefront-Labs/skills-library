---
id: computing-software.software-engineering.javascript.js-fetch-api-and-error-handling
name: js-fetch-api-and-error-handling
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, js-fetch, fetch-api, response-ok, request-headers, http-errors]
level: practitioner
status: docs-checked
description: "Use fetch correctly: check response.ok, read bodies once or clone, send JSON, set credentials, cancel with AbortSignal.timeout and stream bodies."
sources: ["https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch", "https://developer.mozilla.org/en-US/docs/Web/API/Window/fetch", "https://developer.mozilla.org/en-US/docs/Web/API/Response/ok", "https://developer.mozilla.org/en-US/docs/Web/API/Response/clone", "https://developer.mozilla.org/en-US/docs/Web/API/AbortSignal/timeout_static", "https://developer.mozilla.org/en-US/docs/Web/API/Streams_API/Using_readable_streams"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# fetch

- The `fetch()` promise rejects on a network error or a badly formed request, not on an HTTP error status: 404 and 504 still resolve. Check `response.ok` (status 200-299) or `response.status` and throw yourself, for example `if (!res.ok) throw new Error("HTTP " + res.status)`.
- A body can be consumed once (a second read fails with "Body has already been consumed"). `response.clone()` makes a second copy, and throws a `TypeError` if the body was already used, so clone before reading. Readers: `json()`, `text()`, `blob()`, `arrayBuffer()`, `formData()`.
- Send JSON: `fetch(url, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data) })`.
- Credentials (cookies, TLS client certificates, auth headers) are sent only to same-origin requests by default (`credentials: "same-origin"`). `credentials: "include"` sends them cross-origin, but the server must also reply with `Access-Control-Allow-Credentials` and name the client's origin explicitly in `Access-Control-Allow-Origin` (`*` is not allowed).
- Default `mode` is `cors`: a non-simple cross-origin request is preceded by a preflight request, and the real request is sent only if the server answers with the right CORS headers.
- Timeouts and cancellation: `fetch(url, { signal: AbortSignal.timeout(5000) })` aborts with a `TimeoutError`; an `AbortController` `abort()` rejects with `AbortError`.
- Streaming: `response.body` is a `ReadableStream` and an async iterable, so `for await (const chunk of response.body)` works where supported; otherwise use `response.body.getReader()`.

## Checked

2026-11-03. Confirmed on MDN: Using Fetch and Window.fetch (rejection rules, JSON POST, mode, preflight, credentials and CORS headers, consumed body, AbortError), Response.ok (200-299), Response.clone (TypeError if used), AbortSignal.timeout (TimeoutError), Using readable streams (for await over response.body). Removed: FormData boundary note, the query-string `URL`/`URLSearchParams` advice (covered by the URL skills), and the ECMAScript and MDN JavaScript root sources, which do not cover fetch.
Method: documentation only; no commands were run.
