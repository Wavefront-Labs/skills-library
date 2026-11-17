---
id: computing-software.web-development.node-express.csrf-synchronizer-tokens
name: csrf-synchronizer-tokens
category: computing-software
field: web-development
product: node-express
tags: [csrf, csrf-token, synchronizer-token, express, spa, security]
level: practitioner
status: verified
description: "Protecting state-changing requests with synchronizer CSRF tokens in server-rendered forms and SPAs: generation, storage in session, header submission, and rotation."
sources:
  - https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html
  - https://owasp.org/www-community/attacks/csrf
  - https://github.com/Psifi-Solutions/csrf-csrf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CSRF synchroniser tokens

CSRF works when the browser automatically attaches credentials (cookies, HTTP auth) to a cross-site request. Token-based APIs using `Authorization: Bearer` headers from JS are not CSRF-prone; cookie sessions are.

## 1. Pattern
1. On session creation, generate a random token (`crypto.randomBytes(32).toString("base64url")`), store it in the server-side session.
2. Embed it in every form / expose it to the SPA.
3. On every state-changing request (POST/PUT/PATCH/DELETE), compare the submitted token with the session copy using a constant-time compare. Reject with 403 on mismatch or absence.

```js
import crypto from "node:crypto";
app.use((req, res, next) => {
  req.session.csrf ??= crypto.randomBytes(32).toString("base64url");
  res.locals.csrfToken = req.session.csrf;
  next();
});
const SAFE = new Set(["GET", "HEAD", "OPTIONS"]);
app.use((req, res, next) => {
  if (SAFE.has(req.method)) return next();
  const sent = req.get("x-csrf-token") ?? req.body?._csrf ?? "";
  const a = Buffer.from(String(sent)), b = Buffer.from(req.session.csrf);
  const ok = a.length === b.length && crypto.timingSafeEqual(a, b);   // compare BYTE lengths: timingSafeEqual throws RangeError otherwise
  ok ? next() : res.status(403).json({ error: "invalid csrf token" });
});
```
A string-length check is not enough: a 43-character `_csrf` form value made of multibyte characters passed `sent.length === csrf.length` and then made `timingSafeEqual` throw `RangeError: Input buffers must have the same byte length` (a 500 instead of 403; reproduced with express-session). The version above ran: no token 403, `X-CSRF-Token` header 200, `_csrf` form field 200, wrong token 403.
Form: `<input type="hidden" name="_csrf" value="<%= csrfToken %>">`. SPA: render the token in a `<meta name="csrf-token">` or serve it from `GET /api/csrf`, then send as `X-CSRF-Token` header.

## 2. Rules
- **GET must never change state** - tokens are only checked on unsafe methods.
- Regenerate the token on login (alongside session ID rotation).
- Do not put tokens in URLs (leak via Referer/logs).
- Per-session tokens are fine; per-request tokens break back button and multiple tabs for little gain.
- `csurf` is deprecated (npm: "This package is archived and no longer maintained"); use `csrf-csrf`, `csrf-sync`, or framework built-ins (Django `CsrfViewMiddleware`, Rails `protect_from_forgery`, Laravel, Spring Security).
- XSS defeats any CSRF defence - the attacker's script reads the token.

## Verify
Submit the form from a page on another origin (or curl with the session cookie but no token): 403. Normal form and SPA requests: 2xx. Automated: OWASP ZAP CSRF scan rule.
