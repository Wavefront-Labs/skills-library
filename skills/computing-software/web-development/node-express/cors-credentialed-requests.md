---
id: computing-software.web-development.node-express.cors-credentialed-requests
name: cors-credentialed-requests
category: computing-software
field: web-development
product: node-express
tags: [cors, cors-credentials, cookies, fetch-credentials, security]
level: practitioner
status: verified
description: "Making credentialed cross-origin requests work and stay safe: credentials include, Allow-Credentials, why wildcard origins are rejected, and third-party cookie limits."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#requests_with_credentials
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Access-Control-Allow-Credentials
  - https://fetch.spec.whatwg.org/#cors-protocol-and-credentials
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Credentialed CORS requests

## 1. Client
```js
fetch("https://api.example.com/me", { credentials: "include" });   // send cookies / HTTP auth cross-origin
// axios: withCredentials: true   XHR: xhr.withCredentials = true
```
Default `credentials: "same-origin"` does not send cookies cross-origin.

## 2. Server must reply with all of
```
Access-Control-Allow-Origin: https://app.example.com     (exact origin, never *)
Access-Control-Allow-Credentials: true
Vary: Origin
```
With credentials, the browser rejects `*` in `Allow-Origin`, `Allow-Headers`, `Allow-Methods` and `Expose-Headers` - each must be explicit. Missing `Allow-Credentials: true` -> response blocked (the request still reached the server and side effects happened).

## 3. Cookies across sites
- The cookie must be `SameSite=None; Secure` to be sent from a different **site** (tested in Chromium 156: a `Lax` cookie was rejected on a cross-site response and a `SameSite=None` cookie without `Secure` was rejected everywhere; `Lax` cookies were sent with `credentials: "include"` between `localhost:4001` and `localhost:4002`, same-site but cross-origin). Between subdomains of one site (`app.example.com` -> `api.example.com`) `Lax` works because it is same-site.
- Third-party cookie blocking differs by browser (MDN): Safari blocks by default, Firefox puts them in a per-top-level-site partition, Chrome blocks only in Incognito or by user setting. Durable fix: put the API on a subdomain of the app's site or proxy it same-origin. Token auth (`Authorization: Bearer`) avoids cookies but needs XSS-safe storage.

## 4. Security
- Credentialed CORS with a reflected origin = any site can read authenticated responses. Allowlist exact origins.
- Never combine `Allow-Credentials: true` with `Allow-Origin: null`.
- CORS does not protect against CSRF: simple cross-origin POSTs are still sent with cookies; CORS only blocks reading the response.

## 5. Debug signals
Chromium console (v156): "The value of the 'Access-Control-Allow-Origin' header in the response must not be the wildcard '*' when the request's credentials mode is 'include'." or "The value of the 'Access-Control-Allow-Credentials' header in the response is '' which must be 'true' when the request's credentials mode is 'include'." A preflight that fails the same check is prefixed "Response to preflight request doesn't pass access control check:". Network panel > Cookies tab shows blocked cookies with reasons (SameSite, third-party).

## Verify
From the app origin the request carries `Cookie` and JS reads the body; from an unlisted origin the browser blocks the read.
