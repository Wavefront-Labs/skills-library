---
id: computing-software.software-engineering.api-design.cors-for-apis
name: cors-for-apis
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, cors-for-apis, cors, preflight, access-control-allow-origin, owasp-api-top-10, security-misconfiguration]
level: practitioner
status: docs-checked
description: "Configure CORS for APIs safely: origin allow-lists, preflight caching, credentials rules and Vary: Origin, without reflecting arbitrary origins."
sources: ["https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS", "https://owasp.org/API-Security/editions/2023/en/0xa8-security-misconfiguration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CORS for APIs

CORS relaxes the browser same-origin policy; it is not authentication and does nothing for non-browser clients.

## Rules
- Allow-list exact origins; do not echo the request `Origin` back blindly, and never combine `Access-Control-Allow-Origin: *` with credentials (browsers reject it).
- When the allowed origin varies per request, send `Vary: Origin` so caches do not serve one origin's headers to another.
- Preflight (`OPTIONS`) is triggered by non-simple methods or headers such as `Authorization`, and by JSON `Content-Type`. Answer it without auth:
```http
OPTIONS /v1/orders HTTP/1.1
Origin: https://app.example.test
Access-Control-Request-Method: POST
Access-Control-Request-Headers: authorization, content-type

HTTP/1.1 204 No Content
Access-Control-Allow-Origin: https://app.example.test
Access-Control-Allow-Methods: GET, POST
Access-Control-Allow-Headers: authorization, content-type
Access-Control-Max-Age: 600
Vary: Origin
```
- Expose custom response headers the client must read with `Access-Control-Expose-Headers` (for example `Link`, `ETag`, `RateLimit-*`).
- Cookie-authenticated APIs also need `Access-Control-Allow-Credentials: true` and CSRF protection.

## Gotchas
- `Access-Control-Max-Age` defaults to 5 seconds when absent, and each browser has its own internal maximum that wins over a larger value; do not rely on large values.
- With credentials, `*` is not allowed in `Access-Control-Allow-Origin`, `Access-Control-Allow-Headers`, `Access-Control-Allow-Methods` or `Access-Control-Expose-Headers`; list explicit values. A `Set-Cookie` in a response with `Access-Control-Allow-Origin: *` is not honoured.
- Preflight requests never carry credentials; the preflight response must carry `Access-Control-Allow-Credentials: true` for the real request to be sent with them.

Verify: `curl -i -X OPTIONS -H 'Origin: https://evil.example' -H 'Access-Control-Request-Method: GET' <url>` must not return an allow-origin header for the evil origin.

## Checked
2026-11-08. Confirmed in the MDN CORS guide (read by targeted search): simple-request and safelisted header rules, preflight with OPTIONS, `Vary: Origin` when the origin varies, credentialed-request wildcard rules, `Access-Control-Max-Age` default of 5 seconds and browser caps, preflight carries no credentials. The OWASP API8 page confirms a missing or improper CORS policy is a misconfiguration. The Fetch standard section returned no text, so it was not read. Removed unconfirmed: per-browser Max-Age figures (Chromium 2 hours, Firefox 24 hours) and the `null` origin claim.
Method: documentation only; no commands were run.
