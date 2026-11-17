---
id: computing-software.cybersecurity-defensive.application-security.x-content-type-options
name: x-content-type-options
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [x-content-type-options, nosniff, mime-sniffing, content-type, security-headers, user-uploads]
level: practitioner
status: docs-checked
description: "Stop MIME sniffing attacks: send X-Content-Type-Options nosniff with correct Content-Type on every response, especially user uploads and JSON APIs, and verify."
sources: ["https://fetch.spec.whatwg.org/#x-content-type-options-header", "https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Content-Type-Options", "https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# X-Content-Type-Options and MIME sniffing

Browsers historically "sniffed" response bodies to guess the type when `Content-Type` was missing or seemed
wrong. An attacker who uploads a file that looks like HTML or JavaScript, served as `text/plain` or
`image/jpeg`, could get it executed in your origin (stored XSS via uploads, or a JSON response executed as a
script).

## Header
```
X-Content-Type-Options: nosniff
```
Effects (MDN): the browser blocks a request destined for a `script` if the MIME type is not a
JavaScript type, and for a `style` if it is not `text/css`. It also enables Cross-Origin Read Blocking
protections for HTML/JSON/XML responses. Only the `nosniff` value exists.

## Must go with correct Content-Type
- Set accurate `Content-Type` with charset on every response: `text/html; charset=utf-8`,
  `application/json`, `text/javascript`.
- User uploads: decide the type server-side from an allowlist of extensions and content checks, never from
  the client-provided type; serve with `Content-Disposition: attachment` unless inline display is needed;
  ideally from a separate sandbox domain (e.g. a dedicated user-content domain).
- Unknown types: `application/octet-stream` plus `attachment`.

## Where to set
Globally at the reverse proxy/CDN, or in framework middleware.

## Gotchas
- With nosniff on, a script served with a wrong type (e.g. `text/plain` from a misconfigured static server)
  stops working; fix the type rather than removing the header.
- Error responses (404/500) from the proxy also need the header.

## Verify
`curl -sI https://site/uploads/test.txt` and an API endpoint both show `X-Content-Type-Options: nosniff` and the
expected `Content-Type`; an uploaded HTML-content file named `.jpg` downloads or renders as an image, never
as HTML.

## Checked
2026-10-28. Confirmed against official pages: nosniff blocks script and style requests with the wrong MIME type (MDN X-Content-Type-Options); Content-Disposition use for uploads.
Removed or rewritten: nginx, Apache, Helmet, Spring and Django configuration details (not in the fetched pages).
Method: documentation only; no commands were run.
