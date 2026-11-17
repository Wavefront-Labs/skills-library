---
id: computing-software.software-engineering.nim.httpclient-requests
name: httpclient-requests
category: computing-software
field: software-engineering
product: nim
tags: [httpclient-requests, stdlib-net-httpclient, httpclient, http-get, http-post, newhttpclient, headers, ssl, timeout, multipart, nim]
level: practitioner
status: docs-checked
description: "Make synchronous HTTP requests with HttpClient, send JSON and forms, set headers and timeouts, and enable TLS."
sources:
  - https://nim-lang.org/docs/httpclient.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# httpclient: GET, POST, headers and timeouts

Goal: call HTTP APIs.

```nim
import std/[httpclient, json]
let c = newHttpClient(timeout = 5000)
c.headers = newHttpHeaders({"Content-Type": "application/json"})
let r = c.post("https://example.com/api", $(%*{"a": 1}))
echo r.code, r.body
c.close()
```
- `c.getContent(url)` returns the body and raises `HttpRequestError` when the server returns an error; `c.get`/`c.request` return a `Response` with `.status` (string), `.headers`, `code()` and `body()`.
- HTTPS needs the OpenSSL library and compiling with `-d:ssl`; the client uses SSL automatically for `https` URLs.
- Multipart: `newMultipartData` with `.add`/`addFiles`; downloads: `downloadFile`.
- Proxy: `newHttpClient(proxy = newProxy("http://host:port"))`; redirects: `maxRedirects`.

Gotchas:
- `timeout` is in milliseconds and only synchronous calls support it; it applies to individual socket calls, so a whole request can take longer. A stalled read raises `TimeoutError`.

Verify: GET of a known endpoint returns code 200.

## Checked

2026-11-03. Confirmed against the httpclient page: newHttpClient(timeout, maxRedirects, proxy, headers), newHttpHeaders, post, getContent and HttpRequestError, Response status/code, newMultipartData, addFiles, downloadFile, newProxy, OpenSSL and -d:ssl, timeout semantics. Removed: libssl/libcrypto names, the thread-safety claim and the 'error on https without -d:ssl' wording (not on the page).

Method: documentation only; no commands were run.
