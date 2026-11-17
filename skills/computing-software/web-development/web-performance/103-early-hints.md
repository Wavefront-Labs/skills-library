---
id: computing-software.web-development.web-performance.103-early-hints
name: 103-early-hints
category: computing-software
field: web-development
product: web-performance
tags: [early-hints, http-103, link-preload-header, preconnect, ttfb, performance]
level: advanced
status: docs-checked
description: "Using HTTP 103 Early Hints to start preconnects and preloads during server think time: what browsers honour, Node support, what to hint, and measuring the gain."
sources:
  - https://developer.chrome.com/docs/web-platform/early-hints
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status/103
  - https://nodejs.org/api/http.html#responsewriteearlyhintshints-callback
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# 103 Early Hints

While the server is still building the HTML (database calls, SSR), it can send an interim `103` response telling the browser what to fetch:
```http
HTTP/1.1 103 Early Hints
Link: <https://cdn.example.com>; rel=preconnect
Link: </assets/app.css>; rel=preload; as=style

HTTP/1.1 200 OK
Content-Type: text/html
...
```

## 1. Support and limits
- Early Hints apply to the main resource of top-level navigations, and only `preconnect` and `preload` are supported (not `prefetch`). A cross-origin redirect on the final response makes browsers drop the hints. Check the Chrome and MDN pages for current browser support.
- Only useful when your server has think time before it can send the final response.

## 2. Sending them
- **Node**: `response.writeEarlyHints(hints[, callback])` sends the 103 (see the Node `http` docs for the `hints` object); then do the slow work and send the 200.
- **CDNs**: check your CDN's documentation for Early Hints support.
- Frameworks/servers: check that your proxy passes 1xx responses through.

## 3. What to hint
- `preconnect` to critical third-party/asset origins (fonts CDN, image CDN, API).
- `preload` the main CSS and the LCP image or font **if stable across the template**.
- Not page-specific resources that vary per request, and not too many (bandwidth contention with the HTML itself).
- Remember `crossorigin` on font preloads.

## 4. Measure
DevTools Network shows an Early Hints initiator for hinted resources (Chrome); compare LCP before and after enabling it.

## Verify
- [ ] DevTools shows the hinted resources fetched through Early Hints; LCP improves on slow-TTFB routes.

## Checked

2026-10-28. Confirmed from the Chrome Early Hints page (only `preconnect` and `preload`, main resource of top-level navigations, cross-origin redirect drops hints, DevTools Early Hints initiator), MDN 103 page and the Node `http` docs (`response.writeEarlyHints(hints[, callback])`). Removed (not found in the pages): the ~100 ms figure, per-browser and per-CDN support claims, `firstInterimResponseStart`, the curl check and the exact Node `hints` object shape.

Method: documentation only; no commands were run.
