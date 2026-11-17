---
id: computing-software.web-development.node-express.cors-preflight-requests
name: cors-preflight-requests
category: computing-software
field: web-development
product: node-express
tags: [cors, cors-preflight, options-requests, access-control, express]
level: practitioner
status: verified
description: "Handling CORS preflight correctly: which requests trigger OPTIONS, Access-Control-Allow-Methods/Headers, Max-Age caching, and Express/proxy configuration pitfalls."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS
  - https://fetch.spec.whatwg.org/#http-cors-protocol
  - https://expressjs.com/en/resources/middleware/cors.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CORS preflight requests

## 1. When the browser preflights
A cross-origin request is "simple" (no preflight) only if: method GET/HEAD/POST, only CORS-safelisted headers (`Accept`, `Accept-Language`, `Content-Language`, `Range` with a single simple range, `Content-Type` limited to `application/x-www-form-urlencoded`, `multipart/form-data`, `text/plain`), no ReadableStream body, no upload listeners. Anything else - `PUT`/`DELETE`/`PATCH`, `Content-Type: application/json`, `Authorization`, custom `X-*` headers - sends an `OPTIONS` preflight first:
```
OPTIONS /api/items
Origin: https://app.example.com
Access-Control-Request-Method: PUT
Access-Control-Request-Headers: authorization, content-type
```

## 2. Correct response
```
HTTP/1.1 204 No Content
Access-Control-Allow-Origin: https://app.example.com
Access-Control-Allow-Methods: GET, POST, PUT, DELETE
Access-Control-Allow-Headers: authorization, content-type
Access-Control-Max-Age: 600
Vary: Origin
```
Then the actual response must **also** carry `Access-Control-Allow-Origin` (and `-Credentials` if used). `Access-Control-Expose-Headers: X-Total-Count, ETag` to let JS read non-safelisted response headers.

## 3. Express
```js
import cors from "cors";
const corsMw = cors({ origin: ["https://app.example.com"], methods: ["GET","POST","PUT","DELETE"],
  allowedHeaders: ["authorization","content-type"], maxAge: 600, credentials: true });
app.use("/api", corsMw);          // handles OPTIONS for all /api routes
```
The `cors` package answers a preflight with 204 and `Vary: Origin`, `Access-Control-Allow-Methods`, `-Headers` and `-Max-Age` as in section 2 (checked with supertest). Register CORS **before** auth middleware - preflights carry no cookies/Authorization and must not get 401. Return 2xx (204) for OPTIONS.

## 4. Pitfalls
- `Access-Control-Max-Age` defaults to 5 seconds and is capped: Chromium 2 h (7200, since v76; 10 min before), Firefox 24 h (86400) (MDN). Preflight caching is per URL+origin; many distinct URLs still preflight each.
- Reverse proxies/CDNs/API gateways that drop or answer OPTIONS themselves, or cache responses without `Vary: Origin`.
- A redirect answering a preflight fails (Chromium: `Redirect is not allowed for a preflight request.`; verified in Chromium 156); MDN also notes that redirects followed after a preflighted request are not supported by every browser.
- Wildcard `Access-Control-Allow-Headers: *` does not apply on credentialed requests (it is the literal name `*`), and the Fetch spec and MDN say it never covers `Authorization`, which must be listed. In a headless Chromium 156 run a request with `Authorization` still passed against `*`, so do not rely on either behaviour: list `authorization` explicitly.
- Avoid preflights for hot paths by keeping requests simple or serving the API same-origin (proxy `/api` through the app domain).

## Verify
`curl -i -X OPTIONS https://api.example.com/api/items -H "Origin: https://app.example.com" -H "Access-Control-Request-Method: PUT" -H "Access-Control-Request-Headers: authorization,content-type"` returns 204 with the headers above.
