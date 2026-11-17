---
id: computing-software.web-development.htmx.htmx-request-headers-and-caching
name: htmx-request-headers-and-caching
category: computing-software
field: web-development
product: htmx
tags: [htmx, request-headers, hx-request, caching, vary, etag, cors]
level: practitioner
status: docs-checked
description: "Read htmx request headers server-side (HX-Request, HX-Target, HX-Boosted...), serve fragments vs full pages safely with Vary, ETag and CORS."
sources:
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/docs.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/reference.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: let the server tell htmx requests apart, and avoid cache mix-ups between fragments and full pages.

Request headers htmx sends:
- `HX-Request` - always "true". `htmx.config.historyRestoreAsHxRequest` (default `true`) decides whether history cache-miss full-page reloads are treated as HX-Requests.
- `HX-Boosted` - request came from an `hx-boost` element.
- `HX-Current-URL` - the browser's current URL.
- `HX-History-Restore-Request` - "true" for history restoration after a local cache miss.
- `HX-Prompt` - the user's answer to `hx-prompt`.
- `HX-Target` - `id` of the target element, if it has one.
- `HX-Trigger` - `id` of the triggered element, if any.
- `HX-Trigger-Name` - `name` of the triggered element, if any.

Caching:
- Standard HTTP caching works; `Last-Modified` leads the browser to send `If-Modified-Since`.
- When the same URL renders differently depending on `HX-Request`, add `Vary: HX-Request` so caches key on it. Always disable `historyRestoreAsHxRequest` so history full-page fetches are not cached with partial responses.
- If you cannot use `Vary`, set `htmx.config.getCacheBusterParam = true`: GET requests then include `org.htmx.cache-buster=<targetElementId>`.
- `ETag` works, but the server must produce a different ETag for each representation.

CORS: for cross-origin use, set `Access-Control-Allow-Headers` (so request headers pass) and `Access-Control-Expose-Headers` (so response headers like `HX-Trigger` are readable). `htmx.config.selfRequestsOnly` defaults to `true`, blocking cross-domain AJAX; `withCredentials` (default `false`) allows cookies.

Post/Redirect/Get is unnecessary: return the new fragment from the POST with a 200 rather than 302.

## Checked

2026-11-07. Confirmed against the htmx reference (request header table, `historyRestoreAsHxRequest`, `getCacheBusterParam`, `selfRequestsOnly`, `withCredentials`) and the docs (Caching, CORS, Post/Redirect/Get sections). Removed an unsourced "typical server logic" rule that combined two headers, rewrote the `HX-Request` line to match the reference, and removed the invented Verify step.
Method: documentation only; no commands were run.
