---
id: computing-software.web-development.node-express.signed-double-submit-cookie
name: signed-double-submit-cookie
category: computing-software
field: web-development
product: node-express
tags: [csrf, double-submit-cookie, stateless-csrf, hmac, security]
level: practitioner
status: verified
description: "Implementing the signed double-submit cookie CSRF pattern for stateless backends: HMAC binding to the session, __Host- cookies, header submission and naive-variant flaws."
sources:
  - https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html#signed-double-submit-cookie-recommended
  - https://github.com/Psifi-Solutions/csrf-csrf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Signed double-submit cookie

For backends without server-side session storage (JWT-in-cookie, edge functions). The token lives in a cookie **and** is sent in a header/body; an attacker site can make the browser send the cookie but cannot read it to copy into the header.

## 1. Naive version is broken
Plain random value in cookie == header can be defeated if the attacker can **write** cookies for your domain (subdomain takeover, any HTTP subdomain, cookie tossing) - they set both to a known value. So bind the token to the session cryptographically.

## 2. Signed token
```js
import crypto from "node:crypto";
const SECRET = process.env.CSRF_SECRET;               // 32+ random bytes, rotate with overlap
function issue(sessionId) {
  const rand = crypto.randomBytes(16).toString("base64url");
  const mac = crypto.createHmac("sha256", SECRET).update(`${sessionId}!${rand}`).digest("base64url");
  return `${mac}.${rand}`;
}
function verify(token, sessionId) {
  const parts = String(token).split(".");
  if (parts.length !== 2) return false;               // split() alone would accept 'mac.rand.junk'
  const [mac, rand] = parts;
  if (!mac || !rand) return false;
  const expect = crypto.createHmac("sha256", SECRET).update(`${sessionId}!${rand}`).digest("base64url");
  return mac.length === expect.length && crypto.timingSafeEqual(Buffer.from(mac), Buffer.from(expect));
}
// set: res.cookie("__Host-csrf", issue(sid), { secure: true, sameSite: "strict", path: "/" });  (not HttpOnly: JS must read it)
// check unsafe methods: header X-CSRF-Token === cookie value AND verify(header, sid)
```
- `sessionId` must be something the attacker cannot set: the session ID or a stable claim from the authenticated JWT.
- `__Host-` prefix forces `Secure`, `Path=/`, no `Domain` - subdomains cannot overwrite it.
- The client reads the cookie (`document.cookie`) and copies it into the header on each mutating request (axios `xsrfCookieName`/`xsrfHeaderName`, Angular `HttpClientXsrfModule` do this).

## 3. Libraries
`csrf-csrf` (Express, implements this), Angular/axios client support, Django uses a masked double-submit variant with its secret cookie.

## 4. Pitfalls
- Comparing cookie and header only (no HMAC check) = naive version.
- Token not rotated on login -> login CSRF/fixation.
- CORS misconfiguration allowing credentialed cross-origin reads defeats any CSRF scheme.

## Verify
Tests: header missing -> 403; header equals cookie but cookie forged with a different session -> 403; valid pair -> 2xx.

## Checked
Run on Windows with Node 20.20.2 and Express 4.22.3 (real requests): `GET /token` sets `__Host-csrf=<mac>.<rand>; Path=/; Secure; SameSite=Strict`; a valid cookie+header pair for the session gets 200; missing header, missing cookie, header different from cookie, a validly signed token issued for another session placed in both cookie and header, an attacker-chosen plain `AAAA.BBBB` in both, a token without a dot, and a token reused under a different session id all get 403; with the original `split` a token with an appended `.x` in both places was accepted (harmless but sloppy, hence the length check). Not run: `csrf-csrf`, axios/Angular client conventions, the `__Host-` prefix enforcement in a browser, secret rotation with overlap, CORS interactions, a real JWT session.
