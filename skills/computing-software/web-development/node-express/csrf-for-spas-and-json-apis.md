---
id: computing-software.web-development.node-express.csrf-for-spas-and-json-apis
name: csrf-for-spas-and-json-apis
category: computing-software
field: web-development
product: node-express
tags: [csrf-json-api, csrf-custom-header, x-csrf-token, cookie-authenticated-api, csrf, security]
level: practitioner
status: verified
description: "CSRF protection for SPAs calling cookie-authenticated JSON APIs: strict Content-Type, custom request headers, token endpoints, axios/Angular XSRF cookies and CORS interplay."
sources:
  - https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html#employing-custom-request-headers-for-ajaxapi
  - https://angular.dev/best-practices/security#httpclient-xsrf-csrf-security
  - https://developer.mozilla.org/en-US/docs/Glossary/CORS-safelisted_request_header
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CSRF for SPAs and JSON APIs

## 1. Who is at risk
- Cookie/session-authenticated APIs: **vulnerable** (browser attaches cookies cross-site unless SameSite blocks it).
- `Authorization: Bearer` token APIs where the token is in memory/JS: not CSRF-able (attacker pages cannot add the header), but tokens are exposed to XSS.

## 2. Layered defence for cookie APIs
1. `SameSite=Lax` (or `Strict`) session cookie: blocks cross-site POSTs in modern browsers, but not same-site attacks from sibling subdomains.
2. **Require a custom header** on every state-changing request. Cross-origin requests with custom headers need a CORS preflight, which your CORS policy refuses for foreign origins:
```js
app.use("/api", (req, res, next) => {
  if (["GET", "HEAD", "OPTIONS"].includes(req.method)) return next();
  if (!req.is("application/json")) return res.status(415).end();   // forms can send text/plain JSON-looking bodies
  if (req.get("X-Requested-With") !== "fetch" && !validToken(req)) return res.sendStatus(403);
  next();
});
```
(Ran on express 5.3.0: a `text/plain` POST got 415, an `application/json` POST without the header got 403, with `X-Requested-With: fetch` got 200.)
3. Better still: a real token. Double-submit cookie (signed, bound to the session) read by JS and echoed in a header:
   - Angular: cookie `XSRF-TOKEN` -> header `X-XSRF-TOKEN` automatically.
   - axios: `xsrfCookieName`, `xsrfHeaderName` (same-origin only by default; `withXSRFToken` for cross-origin).
   - Django: `csrftoken` cookie -> `X-CSRFToken` header; Rails: `<meta name="csrf-token">` -> `X-CSRF-Token`.
4. Fetch Metadata: reject `Sec-Fetch-Site: cross-site` on non-GET API routes.

## 3. Pitfalls
- Parsing JSON regardless of Content-Type (`express.json({ type: "*/*" })`) lets a cross-site `<form enctype="text/plain">` deliver a valid JSON body. Enforce `application/json`.
- CORS with `credentials: true` and a reflected Origin turns every defence above off: the attacker origin can read the token and send the header.
- GET endpoints that change state are CSRF-able through `<img>`; never mutate on GET.
- Websocket endpoints: check `Origin` on upgrade.

## Verify
- [ ] From another origin: form POST (urlencoded, text/plain) and `fetch` without the header both fail; the SPA works.
