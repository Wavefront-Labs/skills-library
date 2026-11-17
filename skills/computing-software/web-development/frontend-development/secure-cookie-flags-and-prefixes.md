---
id: computing-software.web-development.frontend-development.secure-cookie-flags-and-prefixes
name: secure-cookie-flags-and-prefixes
category: computing-software
field: web-development
product: frontend-development
tags: [security-headers, http-security-headers, cookie-flags, cookie-prefixes, httponly, samesite, host-prefix, secure-cookie, session-cookie]
level: practitioner
status: docs-checked
description: "Setting session cookies right: Secure, HttpOnly, SameSite Lax/Strict/None, the __Host- prefix, Domain/Path scope, lifetime and partitioned cookies."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Set-Cookie
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Cookies
  - https://github.com/expressjs/session#readme
  - https://docs.djangoproject.com/en/stable/ref/settings/
  - https://guides.rubyonrails.org/configuring.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Secure cookie flags and prefixes

**Goal:** session cookies that scripts can't read, aren't sent cross-site unnecessarily, can't be overwritten from subdomains, and never travel over HTTP.

## 1. The session cookie
```
Set-Cookie: __Host-sid=<opaque-random>; Path=/; Secure; HttpOnly; SameSite=Lax; Max-Age=28800
```
| Attribute | Why |
|---|---|
| `Secure` | Only over HTTPS |
| `HttpOnly` | Not readable by JS (XSS can't exfiltrate it; it can still act as the user while on the page) |
| `SameSite=Lax` | Not sent on cross-site subrequests/POSTs; sent on top-level GET navigations (so links into your app stay logged in) |
| `__Host-` prefix | Browser enforces Secure, `Path=/` and **no Domain** - a compromised/evil subdomain can't set or shadow it |
| No `Domain` | Host-only; adding `Domain=example.com` shares it with every subdomain |

## 2. SameSite choice
- `Lax`: good default. Some browsers apply `Lax` when `SameSite` is omitted (MDN: check browser compatibility; Safari does not), so always set it explicitly.
- `Strict`: never sent from another site, even on link clicks (user appears logged out after following an email link). Use for a secondary "sensitive actions" cookie.
- `None` (requires `Secure`): needed for cross-site iframes/embeds and some SSO POST callbacks. Third-party cookies are blocked or partitioned in many browsers; add `Partitioned` (CHIPS) for embed state that's per-top-site (Chrome 114, Firefox 141, Safari 26.2 per MDN browser-compat data).

## 3. Lifetime
Session cookies (no `Max-Age` or `Expires`) are removed when the client shuts down, but browsers with session restore bring them back (MDN). Set explicit idle/absolute timeouts server-side; cookie `Max-Age` is a client hint, not enforcement.

## 4. Framework settings
- Express (`express-session`): `cookie: { secure: true, httpOnly: true, sameSite: 'lax', maxAge }` and `name: '__Host-sid'`; behind a TLS-terminating proxy set `app.set('trust proxy', 1)`, otherwise the library does not set `secure` cookies. The library's own cookie defaults are `{ path: '/', httpOnly: true, secure: false, maxAge: null }`, so set `secure` yourself.
- Django: `SESSION_COOKIE_SECURE`, `SESSION_COOKIE_HTTPONLY` (default `True`), `SESSION_COOKIE_SAMESITE`, `CSRF_COOKIE_SECURE`.
- Rails: `config.action_dispatch.cookies_same_site_protection` defaults to `:lax`; `config.session_store :cookie_store, key: '__Host-app_session'` sets the cookie name (the `__Host-` rules still require `Secure` and no `Domain`).

## 5. Gotchas
- Cookie names/values are visible in logs and proxies - no data in them, just an opaque id (or a signed/encrypted token).
- `Path` is not a security boundary: MDN says it does not protect against reading the cookie from another path.

## Verify
- [ ] DevTools > Application > Cookies shows Secure, HttpOnly, SameSite and the `__Host-` name.
- [ ] `document.cookie` in the console does not include the session.
- [ ] A cross-site form POST to your app arrives without the session cookie.

## Checked
Checked 2026-10-26 against MDN Set-Cookie and Cookies guide (prefix rules: `__Host-` needs Secure, Path=/ and no Domain; Lax default only in some browsers; session restore; Partitioned), MDN browser-compat data, the express-session README (defaults, sameSite option, trust proxy), the Django settings reference (SESSION_COOKIE_HTTPONLY default True, SAMESITE and SECURE settings) and the Rails configuration guide (cookies_same_site_protection default :lax). Removed the unconfirmed claim that cookie scope ignores ports and the Rails same_site/secure options on session_store.

Method: documentation only; no commands were run.
